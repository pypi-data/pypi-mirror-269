from sqlton.ast import All, Alias, Index, Operation, Column, Create, Drop, Select, SelectCore, Values, Insert, Update, Delete, Table
from sqlton import parse
from sqletic.scope import lookup, Scope, Entry
from sqletic.expression import Evaluator

def keep_recursive_set(name, expression):
    def in_collection(collection):
        if isinstance(collection, Values):
            return False
        elif isinstance(collection, Alias):
            return in_collection(collection.original)
        elif isinstance(collection, Index):
            return in_collection(collection.table)
        elif isinstance(collection, Table):
            return collection.name == name
        elif isinstance(collection, SelectCore):
            for _collection in collection.table_list:
                if in_collection(_collection):
                    return True
        elif isinstance(collection, Operation) and collection.operator[0] == 'JOIN':
            return in_collection(_collection.a) or in_collection(_collection.b)
    
    if isinstance(expression, Operation):
        if expression.operator[0] in ('UNION', 'INTERSECT', 'EXCEPT'):
            in_a = in_collection(expression.a)
            in_b = in_collection(expression.b)
            
            if in_a and in_b:
                return expression
            elif not in_a:
                return keep_recursive_set(name, expression.b)
            elif not in_b:
                return keep_recursive_set(name, expression.a)
            else:
                raise Exception("CT shall have been refered in one of the branch")
        else:
            return expression
    else:
        return expression
                
class CommonTable:
    def __init__(self, engine, name, columns, select, scope, entries=None):
        if (entries is None and
            not (isinstance(select, Operation) and
                 select.operator[0] in ('UNION', 'INTERSECT', 'EXCEPT'))):
            raise ValueError('Root expression shall be set operation of values and/or select expression')
        
        self.engine = Engine(engine.tables | {name: entries if entries else []})
        self.name = name
        self.columns = columns
        self.select = select

    def __iter__(self):
        entries = []
        
        for _, _scope in self.engine.iterate(scope, self.select):
            entry = dict(zip(self.columns, _scope[None].values())) 
            entries.append(entry)
            yield entry

        if entries:
            select = keep_recursive_set(self.name, self.select)
            yield from CommonTable(self.engine,
                                   self.name,
                                   self.columns,
                                   select,
                                   scope,
                                   entries)

class Engine:
    def __init__(self, tables):
        self.tables = tables
        self.iterator = None
        self.description = ()
        self.rowcount = 0


    def __iter__(self):
        if self.iterator:
            while entry := self.fetchone():
                yield entry
            self.iterator = None
        else:
            raise StopIteration()
        
    def execute(self, statement):
        self.iterator = None
        statement, = parse(statement)

        if isinstance(statement, Create):
            self.execute_create(statement)
        elif isinstance(statement, Drop):
            self.execute_drop(statement)
        elif isinstance(statement, Select): 
            self.iterator = self.iterate({}, statement)
        elif isinstance(statement, Insert):
            self.execute_insert(statement)
        elif isinstance(statement, Update):
            self.execute_update(statement)
        elif isinstance(statement, Delete):
            self.execute_delete(statement)
        else:
            raise NotImplementedError(f'Statement {statement}')

    def execute_create(self, statement):
        self.tables[statement.table.name] = []

    def execute_drop(self, statement):
        del self.tables[statement.table.name]
        
    def execute_insert(self, statement):
        entries = (self.scope_to_entry((All(),), scope)
                   for _, scope
                   in self.iterate({}, statement.values))

        if not (len(statement.columns) == 1 and isinstance(statement.columns[0], All)):
            entries = (dict(zip(statement.columns, entry.values())) for entry in entries)
        
        self.tables[statement.target.name].extend(entries)

    def execute_update(self, statement):
        if isinstance(statement.target, Alias):
            table = statement.target.original.name
            alias = statement.target.replacement
        else:
            table = statement.target.name
            alias = statement.target.name

        for entry in self.tables[table]:
            scope = {alias:entry}
            
            if statement.tables:
                tables = self.iterate_table_list(scope, statement.tables)
            else:
                tables = ((None, scope),)

            for _, scope in tables:
                if statement.where:
                    evaluation = Evaluator(scope)(statement.where)
                else:
                    evaluation = True

                if evaluation:
                    for columns, expression in statement.assignments:
                        value = Evaluator(scope)(expression)

                        for column in columns:
                            entry[column] = value

                elif statement.alternative:
                    raise NotImplementedError("Alternative feature was not yet implemented !")

    def execute_delete(self, statement):
        if isinstance(statement.target, Alias):
            table = statement.target.original.name
            alias = statement.target.replacement
        else:
            table = statement.target.name
            alias = statement.target.name

        to_remove = []
            
        for entry in self.tables[table]:
            scope = {alias:entry}
            
            tables = ((None, scope),)

            for _, scope in tables:
                if statement.where:
                    evaluation = Evaluator(scope)(statement.where)
                else:
                    evaluation = True

                if evaluation:
                    to_remove.append(entry)
                    
        for entry in to_remove:
            self.tables[table].remove(entry)
                    
    def fetchone(self):
        if not self.iterator:
            self.description = ()
            self.rowcount = 0
            return None
        
        try:
            name, scope = next(self.iterator)
        except StopIteration:
            return None
        
        entry = self.scope_to_entry((All(),), scope)
        
        self.description = tuple((key, type(value), None, None, None, None, None)
                                 for key, value
                                 in entry.items())
        self.rowcount = len(self.description)
        
        return tuple(entry.values())

    def fetchmany(self, size):
        for _ in range(size):
            yield self.fetchone()

    def fetchall(self):
        return [entry for entry in self]
        
    def scope_to_entry(self, columns, scope:Scope) -> Entry:
        entry = {}
        evaluator = Evaluator(scope)
        
        for index, column in enumerate(columns):
            if isinstance(column, Alias):
                entry[column.replacement] = evaluator(column.original)
            elif isinstance(column, Column):
                entry[column.name] = evaluator(column)
            elif isinstance(column, All):
                if column.table is None:
                    tables = scope.values()
                else:
                    tables = (scope[column.table],)
                
                for table in tables:
                    if table == CommonTable:
                        continue
                    
                    for key, value in table.items():
                        if key not in entry:
                            entry[key] = evaluator(value)            
            else:
                entry[index] = evaluator(column)

        return entry

    def iterate_select(self, scope, select:Select):
        if hasattr(select, 'with_clause'):
            scope[CommonTable] = {cte.name: CommonTable(self,
                                                        cte.name,
                                                        cte.columns,
                                                        cte.select,
                                                        scope)
                                  for cte in select.with_clause.ctes}
            
        yield from self.iterate(scope, select.select_core)


    def iterate_values(self, scope, values:Values):
        for columns in values.values:
            yield None, scope | {None:self.scope_to_entry(columns, scope)}
        
    def iterate_selectcore(self, scope, core:SelectCore):
        hashes = set()

        distinct = hasattr(core, 'reduction') and core.reduction == 'DISTINCT'
        
        for _name, _scope in self.iterate_selectcore_scope(scope, core):
            entry = self.scope_to_entry(core.result_column_list, _scope)
            
            if distinct:
                hsh = hash(frozenset(entry.items()))
                
                if not hsh in hashes:
                    yield None, {None:entry}
                    hashes.add(hsh)
            else:
                yield None, {None:entry}

    def iterate_selectcore_scope(self, scope, core:SelectCore):
        for _, _scope in self.iterate_table_list(scope, core.table_list):
            if hasattr(core, 'where'):
                if Evaluator(_scope)(core.where):
                    yield None, _scope
            else:
                yield None, _scope


    def iterate_table_list(self, scope, table_list:list[Table|Alias|Operation]):
        head, *remainder = table_list

        for name, scope in self.iterate(scope, head):
            if len(remainder):
                yield from self.iterate_table_list(scope, remainder)
            else:
                yield name, scope
                

    def iterate(self, scope, element):
        yield from getattr(self, f"iterate_{type(element).__name__}".lower())(scope, element)

    def iterate_alias(self, scope, alias: Alias):
        name = alias.replacement
        for _name, _scope in self.iterate(scope, alias.original):
            yield name, {name: _scope[_name]} | scope

    def iterate_table(self, scope, table: Table):
        if table.name in self.tables:
            collection = self.tables[table.name]
        elif CommonTable in scope and table.name in scope[CommonTable]:
            collection = scope[CommonTable][table.name]
        else:
            raise KeyError(f'Found no such {table.name} table neither in common tables ({scope[CommonTable].keys()}) nor tables {self.tables.keys()}')
        
        for entry in collection:
            yield table.name, scope | {table.name:entry}

    def iterate_operation(self, scope, operation):
        for index in range(len(operation.operator), 0, -1):
            method_name = 'iterate_operation_' + '_'.join(part
                                                          for part in operation.operator[:index]
                                                          if isinstance(part, str)).lower()
            if hasattr(self, method_name):
                yield from getattr(self, method_name)(scope, operation.operator, operation.a, operation.b)
                return
        
        raise NotImplementedError(f"no method found for operator: {operation.operator}")
    
    def iterate_operation_join(self, scope, operator, a, b):
        for name_a, scope_a in self.iterate(scope, a):
            for name_b, scope_b in self.iterate(scope_a, b):
                method, constraint = operator[-1]

                if operator == ('JOIN',) or 'CROSS' in operator:
                    yield name_b, scope_b
                    continue

                if method == 'ON':
                    evaluation = Evaluator(scope_b)(constraint)
                elif method == 'USING':
                    evaluation = True
                    
                    for column in constraint:
                        if lookup(scope_a, (name_a, column)) != lookup(scope_b, (name_b, column)):
                            break
                    else:
                        evaluation = False
                else:
                    raise NotImplementedError(f"No such {method} method for inner join ")

                if evaluation:
                    yield name_b, scope_b
                else:
                    if 'LEFT' in operator:
                        yield name_b, scope_a | {name_b: None}
                    elif 'RIGHT' in operator:
                        yield name_b, scope | {name_a: None} | {name_b: scope_b[name_b]}
                    elif 'FULL' in operator and 'OUTER' in operator:
                        yield name_b, scope | {name_a: None} | {name_b: None}

    def iterate_operation_union_all(self, scope, operator, a, b):
        yield from self.iterate(scope, a)
        yield from self.iterate(scope, b)

    def iterate_operation_union(self, scope, operator, a, b):
        hashes = set()
        
        for name, scope in self.iterate_operation_union_all(scope, None, a, b):
            entry = hash(frozenset(scope[name].items()))
            if not entry in hashes:
                yield None, scope
                hashes.add(entry)

    def iterate_operation_intersect(self, scope, operator, a, b):
        hashes = set()
        
        for name_a, scope_a in self.iterate(scope, a):
            hash_a = hash(frozenset(scope_a[name_a].items()))
            for name_b, scope_b in self.iterate(scope_a, b):
                hash_b = hash(frozenset(scope_b[name_b].items()))
                
                if hash_a == hash_b and hash_a not in hashes:
                    yield None, scope_b
                    
                    hashes.add(hash_a)
