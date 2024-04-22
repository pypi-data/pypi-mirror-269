from sqlton.ast import Alias, Operation, Column
from sqletic.scope import lookup
import datetime
import operator
from re import sub, match
from functools import partial

def not_implemented(a, b):
    raise NotImplementedError()

def like(a, b):
    for rule, replacement in ((r'\.', r'\.'),
                              (r'%', '.*'),
                              (r'_', '.')):
        b = sub(rule, replacement, b)
    _match = match('^' + b + '$', a)
    return  _match is not None

class Evaluator:
    functions = {'concat':lambda *args:''.join((arg
                                                if isinstance(arg, str)
                                                else repr(arg))
                                               for arg in args)}

    def __init__(self, scope):
        self.scope = scope

    def __call__(self, expression):
        if isinstance(expression, Operation):
            return self.operation(expression.operator,
                                  expression.a, expression.b)
        elif isinstance(expression, Column):
            return lookup(self.scope,
                          (expression.table.name, expression.name)
                          if expression.table
                          else expression.name)
        else:
            return expression

    def operation(self, operator, a, b):
        method_name = '_'.join(('operator', *operator)).lower()

        if hasattr(self, method_name):
            return getattr(self, method_name)(self(a), self(b))
        else:
            return self.operators[operator](self(a), self(b))


    def operator_call(self, identifier, parameter):
        arguments = []
        for argument in parameter['arguments']:
            arguments.append(self(argument))

        return self.functions[identifier](*arguments)

    kinds = {'BINARY':bin,
             'CHAR':str,
             'DATE':datetime.date.fromisoformat,
             'DATETIME':datetime.datetime.fromisoformat,
             'DECIMAL':float,
             'DOUBLE':float,
             'INTERGER':int,
             'SIGNED':int,
             'UNSIGNED':lambda value: abs(int(value)),
             'TIME':datetime.time.fromisoformat,
             'VARCHAR':str}

    def operator_cast(self, value, kind):
        return kinds[kind](self(value))

    operators = {('=',): operator.eq,
                 ('<>',): operator.ne,
                 ('!=',): operator.ne,
                 ('<=',): operator.le,
                 ('>=',): operator.ge,
                 ('<',): operator.lt,
                 ('>',): operator.gt,
                 ('*',): operator.mul,
                 ('/',): operator.truediv,
                 ('+',): operator.add,
                 ('-',): operator.sub,
                 ('AND',): operator.and_,
                 ('OR',): operator.or_,
                 ('IN',): operator.contains,
                 ('LIKE',): like,
                 ('GLOB',): not_implemented,
                 ('REGEXP',): lambda a, b: match(b, a) is not None,
                 ('MATCH',): not_implemented,
                 ('NOT', any): not_implemented}
    
