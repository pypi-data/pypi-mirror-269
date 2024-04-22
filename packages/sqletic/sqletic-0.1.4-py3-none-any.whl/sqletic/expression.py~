from sqlton.ast import Alias, Operation, Column
from tinydb_sql.scope import lookup
import datetime
import operator

def not_implemented(a, b):
    raise NotImplementedError()

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

    operators = {('EQUAL',): operator.eq,
                 ('DIFFERENCE',): operator.ne,
                 ('LESS_OR_EQUAL',): operator.le,
                 ('MORE_OR_EQUAL',): operator.ge,
                 ('LESS',): operator.lt,
                 ('MORE',): operator.gt,
                 ('MULTIPLICATION',): operator.mul,
                 ('DIVISION',): operator.truediv,
                 ('PLUS',): operator.add,
                 ('MINUS',): operator.sub,
                 ('AND',): operator.and_,
                 ('OR',): operator.or_,
                 ('IN',): operator.contains,
                 ('LIKE',): lambda a, b: re.match('^' + sub('_', '.', sub(r'\?', '.*', b)) + '$',
                                                  a) is not None,
                 ('GLOB',): not_implemented,
                 ('REGEXP',): lambda a, b: re.match(b, a),
                 ('MATCH',): not_implemented,
                 ('NOT', any): not_implemented}
    
