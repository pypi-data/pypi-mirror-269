from typing import Any

Entry = dict[str, Any]

class Scope(dict[str, Entry]):
    def __init__(self, *args, ctes=None):
        super().__init__(*args, **kwargs)

        if ctes is None:
            ctes = {}
            
        if len(args) == 0 and isinstance(args[0], Scope):
            ctes = ctes | args[0].ctes
            
        self.ctes = ctes


def lookup(scope: Scope, reference:str | tuple[str, str]):
    if isinstance(reference, str):
        for entry in scope.values():
            if reference in entry:
                return entry[reference]
        else:
            raise KeyError(f'No such column found {reference} !')
    else:
        table, column = reference

        if not table in scope:
            raise KeyError(f"No such table {table} in current scope {scope.keys()}")
        
        if scope[table] is None:
            return None
        
        if not column in scope[table] :
            raise KeyError(f"No such column {column} in {table} table {scope[table].keys()}")
        
        return scope[table][column]
