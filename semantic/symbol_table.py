from typing import Optional

class SymbolTable:
    instance: Optional["SymbolTable"] = None

    @staticmethod
    def get_instance():
        if SymbolTable.instance is None:
            SymbolTable.instance = SymbolTable()
        return SymbolTable.instance

    def __init__(self):
        self.records = []
        self.insert(0, "int", "kw", "kw", 0)
        self.insert(0, "void", "kw", "kw", 0)
        self.insert(0, "break", "kw", "kw", 0)
        self.insert(0, "if", "kw", "kw", 0)
        self.insert(0, "else", "kw", "kw", 0)
        self.insert(0, "repeat", "kw", "kw", 0)
        self.insert(0, "until", "kw", "kw", 0)
        self.insert(0, "return", "kw", "kw", 0)
        self.insert(0, "output", "void", "FUNC", 0, 1, ["int"])

    def insert(self, lineno, lexeme, vtype, mode, scope, argcnt=None, typelist=None, index=None):
        temp = {"lineno": lineno, "lexeme": lexeme, "type": vtype, "scope": scope, "mode": mode}
        if not (argcnt is None):
            temp["argcnt"] = argcnt

        if not (typelist is None):
            temp["typelist"] = typelist

        if index is None:
            self.records.append(temp)
        else:
            self.records[index] = temp

    def tail(self):
        return len(self.records) - 1

    def purge(self, stop):
        self.records = self.records[:stop]

    def skip(self):
        self.records.append(None)

    def get_symbol(self, sym):
        for k in reversed(self.records):
            if k["lexeme"] == sym :
                return k
        return None

    def symbol_exists(self, sym):
        return not (self.get_symbol(sym) is None)

    def get_identity(self, record):
        if record["mode"] == "var":
            return record["type"]
        return record["mode"]


