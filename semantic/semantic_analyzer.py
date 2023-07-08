from typing import Optional
from codegen.stack import Stack
from .symbol_table import SymbolTable

class SemanticAnalyzer:
    instance: Optional["SemanticAnalyzer"] = None

    @staticmethod
    def get_instance():
        if SemanticAnalyzer.instance is None:
            SemanticAnalyzer.instance = SemanticAnalyzer()
        return SemanticAnalyzer.instance

    def __init__(self):
        self.symbol_table = SymbolTable.get_instance()
        self.scope_stack = Stack()
        self.scope_stack.push(0)
        self.semantic_stack = Stack()
        self.errors = []
        self.iter_level = 0
        self.toss = False
        
        # temoorary storages
        self.ftl = []

    def reset_temps(self):
        self.ftl = []

    def scope(self):
        return self.scope_stack.peek()

    def scope_up(self):
        last = self.symbol_table.tail()
        self.scope_stack.push(last + 1)

    def scope_down(self):
        last = self.scope_stack.pop()
        self.symbol_table.purge(last)

    def haserror(self):
        return self.toss or len(self.errors) != 0
    
    def run_routine(self, routine_name, params):
        func_to_call = getattr(self, routine_name)
        if func_to_call is not None and callable(func_to_call):
            func_to_call(*params)
        else:
            raise Exception("Semantic routine not found")

    def pop(self):
        self.semantic_stack.pop()

    def save_type(self, token):
        self.semantic_stack.push(token)

    def save_lexeme(self, token):
        self.semantic_stack.push(token)

    def decl_var(self, lin):
        lexeme = self.semantic_stack.pop()
        vtype = self.semantic_stack.pop()
        if vtype == "void":
            self.throw_void_type(lin, lexeme)
        self.symbol_table.insert(lin, lexeme, vtype, "var", self.scope())

    def save_array_argcnt(self, num):
        self.semantic_stack.push(num)

    def decl_arr(self, lin):
        argcnt = self.semantic_stack.pop()
        lexeme = self.semantic_stack.pop()
        vtype = self.semantic_stack.pop()
        if vtype == "void":
            self.throw_void_type(lin, lexeme)
        self.symbol_table.insert(lin, lexeme, vtype, "array", self.scope(), argcnt)

    def skip_func(self):
        i = self.symbol_table.tail()
        self.semantic_stack.push(i+1)
        self.reset_temps()
        self.symbol_table.skip()

    def decl_func(self, lin):
        i = self.semantic_stack.pop()
        lex = self.semantic_stack.pop()
        vtype = self.semantic_stack.pop()
        temp = self.scope_stack.pop()
        scope = self.scope_stack.peek()
        self.scope_stack.push(temp)
        self.symbol_table.insert(lin, lex, vtype, "FUNC", scope, len(self.ftl), self.ftl, i)
        if lex != "main":
            self.toss = True
        self.reset_temps()

    def decl_arg_arr(self, lin):
        lex = self.semantic_stack.pop()
        vtype = self.semantic_stack.pop()
        self.symbol_table.insert(lin, lex, vtype, "array", self.scope(), -1)
        if vtype == "void":
            self.throw_void_type(lin, lexeme)
        self.ftl.append("array")

    def decl_arg_var(self, lin):
        lex = self.semantic_stack.pop()
        vtype = self.semantic_stack.pop()
        self.symbol_table.insert(lin, lex, vtype, "var", self.scope())
        if vtype == "void":
            self.throw_void_type(lin, lexeme)
        self.ftl.append(vtype)

    def scope_check(self, token, lin):
        sym = self.symbol_table.get_symbol(token)
        if sym is None:
            self.throw_scoping(lin, token)
            self.semantic_stack.push("int")
        else:
            self.semantic_stack.push(self.symbol_table.get_identity(sym))

    def assert_same_type(self, lin):
        t1 = self.semantic_stack.pop()
        t2 = self.semantic_stack.pop()
        self.semantic_stack.push("int")
        if t1 == t2:
            return
        if t1 == "int":
            self.throw_type_mismatch(lin, t2)
        else:
            self.throw_type_mismatch(lin, t1)

    def assert_type_array(self, lin):
        if self.semantic_stack.pop() != "array":
            self.throw_type_arr(lin, self.semantic_stack.peek())

    def assert_type_int(self, lin):
        vtype = self.semantic_stack.pop()
        if vtype != "int":
            self.throw_type_mismatch(lin, vtype)
        self.semantic_stack.push("int")

    def push_type_int(self):
        self.semantic_stack.push("int")

    def scope_check_func(self, lin):
        token = self.semantic_stack.peek()
        sym = self.symbol_table.get_symbol(token)
        if sym is None:
            self.throw_scoping(lin, token)
            self.semantic_stack.push("int")
        elif sym.get_identity() != "FUNC":
            self.throw_type_mismatch_func(lin, sym.get_identity())

    def type_check_func(self, lin):
        iden = self.semantic_stack.pop()
        if iden != "FUNC":
            self.throw_type_mismatch_func(lin, iden)

    def arg_check_begin(self):
        token = self.semantic_stack.peek()
        self.semantic_stack.push(f"arg_check")

    def correct(self):
        t1 = self.semantic_stack.pop()
        self.semantic_stack.pop()
        self.semantic_stack.push(t1)

    def arg_check_end(self, lin):
        arg_list = []
        while self.semantic_stack.peek() != "arg_check":
            arg_list.append(self.semantic_stack.pop())

        self.semantic_stack.pop() # remove the arg_check

        token = self.semantic_stack.pop()

        sym = self.symbol_table.get_symbol(token)
        ftl = sym["typelist"]

        if len(arg_list) != len(ftl):
            self.throw_number_mismatch(lin, token)

        for i in range(len(arg_list)):
            got = arg_list[len(arg_list) - i -1] 
            if i >= len(ftl): break
            if got != ftl[i]:
                self.throw_arg_mismatch(lin, token, i, got, ftl[i])

        self.semantic_stack.push(sym["type"])

    def iter_up(self):
        self.iter_level += 1

    def iter_down(self):
        self.iter_level -= 1
    
    def iter_check(self, lin):
        if self.iter_level <= 0:
            self.throw_break(lin)

    def finish_func(self):
        pass

    def throw_scoping(self, lin, token):
        self.errors.append(f"#{lin}: Semantic Error! '{token}' is not defined.")

    def throw_void_type(self, lin, token):
        self.errors.append(f"#{lin}: Semantic Error! Illegal type of void for '{token}'.")

    def throw_type_arr(self, lin, token):
        pass

    def throw_number_mismatch(self, lin, token):
        self.errors.append(f"#{lin}: Semantic Error! Mismatch in numbers of arguments of '{token}'.")

    def throw_type_mismatch(self, lin, vtype):
        self.errors.append(f"#{lin}: Semantic Error! Type mismatch in operands, Got {vtype} instead of int.")

    def throw_type_mismatch_func(self, lin , vtype):
        self.errors.append(f"#{lin}: Semantic Error! Type mismatch in operands, Got {vtype} instead of func.")

    def throw_break(self, lin):
        self.errors.append(f"#{lin}: Semantic Error! No 'repeat ... until' found for 'break'.")

    def throw_arg_mismatch(self, lin, token, i, a, b):
        self.errors.append(f"#{lin}: Semantic Error! Mismatch in type of argument {i+1} of '{token}'. Expected '{b}' but got '{a}' instead.")

