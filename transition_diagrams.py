from scanner import Scanner
from anytree import Node, RenderTree


class Parser:
    def __init__(scanner, terminals, non_terminals, first_sets, follow_sets):
        self.scanner = scanner
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.first_sets = first_sets
        self.follow_sets = follow_sets
        self.errors = []
        self.tree = None

    def match_token(expected_token):
        if self.scanner.get_current_token()[0] == expected_token:
            Scanner.get_next_token()
            return True
        else:
            return False

    def error(message):
        self.errors.append((self.scanner.get_line_number(), message))

    def transition_diagram_program():
        # for this rule: Program -> Declaration-list

        # add root node
        program_node = Node("Program")

        token = self.scanner.get_current_token()
        if token in self.first_sets["Declaration_list"]:
            transition_diagram_declaration_list(parent=program_node)
        elif token in self.follow_sets["Program"]:
            # remove root node
            program_node = None
            if "Epsilon" in self.first_sets["Program"]:
                return
            else:
                error(f"Missing Program")
        else:
            error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove root node
            program_node = None
            transition_diagram_program()

    def transition_diagram_declaration_list(parent):
        # for this rule: Declaration-list -> Declaration Declaration-list | Epsilon

        # add node to self.tree
        declaration_list_node = Node("Declaration_list", parent=parent)

        token = self.scanner.get_current_token()
        if token in self.first_sets["Declaration"]:
            transition_diagram_declaration(parent=declaration_list_node)
            transition_diagram_declaration_list(parent=declaration_list_node)
        elif token in self.follow_sets["Declaration_list"]:
            # remove node from tree
            declaration_list_node.parent = None
            if "Epsilon" in self.first_sets["Declaration_list"]:
                return
            else:
                error(f"Missing Declaration_list")
        else:
            error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            declaration_list_node.parent = None
            transition_diagram_declaration_list()

    def transition_diagram_declaration(parent):
        # for this rule: Declaration -> Declaration-initial Declaration-prime
        declaration_node = Node("Declaration", parent=parent)

        token = self.scanner.get_current_token()
        if token in self.first_sets["Declaration_initial"]:
            transition_diagram_declaration_initial()
            transition_diagram_declaration_prime()
        elif token in self.follow_sets["Declaration"]:
            if "Epsilon" in self.first_sets["Declaration"]:
                # remove node from tree
                declaration_node.parent = None
                return
            else:
                error(f"Missing Declaration")
        else:
            error(f"Illegal {token}")
            self.scanner.get_next_token()
            transition_diagram_declaration()

    def transition_diagram_declaration_initial():
        # for this rule: Declaration-initial -> Type-specifier ID
        token = self.scanner.get_current_token()
        if token in self.first_sets["Type_specifier"]:
            transition_diagram_type_specifier()
            matched = match_token("ID")
            if not matched:
                error(f"Missing ID")
        elif token in self.follow_sets["Declaration_initial"]:
            if "Epsilon" in self.first_sets["Declaration_initial"]:
                return
            else:
                error(f"Missing Declaration_initial")
        else:
            error(f"Illegal {token}")
            self.scanner.get_next_token()
            transition_diagram_declaration_initial()

    def transition_diagram_declaration_prime():
        # for this rule: Declaration-prime -> Fun-declaration-prime | Var-declaration-prime
        token = self.scanner.get_current_token()
        if token in self.first_sets["Fun_declaration_prime"]:
            transition_diagram_fun_declaration_prime()
        elif token in self.first_sets["Var_declaration_prime"]:
            transition_diagram_var_declaration_prime()
        elif token in self.follow_sets["Declaration_prime"]:
            if "Epsilon" in self.first_sets["Declaration_prime"]:
                return
            else:
                error(f"Missing Declaration_prime")
        else:
            error(f"Illegal {token}")
            self.scanner.get_next_token()
            transition_diagram_declaration_prime()

    def transition_diagram_var_declaration_prime():
        # for this rule: Var-declaration-prime -> ; | [ NUM ] ;
        token = self.scanner.get_current_token()
        if token == ";":
            match_token(";")
        elif token == "[":
            match_token("[")
            match_tokened = match_token("NUM")
            if not match_tokened:
                error(f"Missing NUM")
            match_token("]")
            match_token(";")
        elif token in self.follow_sets["Var_declaration_prime"]:
            if "Epsilon" in self.first_sets["Var_declaration_prime"]:
                return
            else:
                error(f"Missing Var_declaration_prime")
        else:
            error(f"Illegal {token}")
            self.scanner.get_next_token()
            transition_diagram_var_declaration_prime()

    def transition_diagram_fun_declaration_prime():
        # for this rule: Fun-declaration-prime -> ( Params ) Compound-stmt
        token = self.scanner.get_current_token()
        if token == "(":
            match_token("(")
            transition_diagram_params()
            match_token(")")
            transition_diagram_compound_stmt()
        elif token in self.follow_sets["Fun_declaration_prime"]:
            if "Epsilon" in self.first_sets["Fun_declaration_prime"]:
                return
            else:
                error(f"Missing Fun_declaration_prime")
        else:
            error(f"Illegal {token}")
            self.scanner.get_next_token()
            transition_diagram_fun_declaration_prime()

    def transition_diagram_type_specifier():
        # for this rule: Type-specifier -> int | void
        token = self.scanner.get_current_token()
        if token == "int":
            match_token("int")
        elif token == "void":
            match_token("void")
        elif token in self.follow_sets["Type_specifier"]:
            if "Epsilon" in self.first_sets["Type_specifier"]:
                return
            else:
                error(f"Missing Type_specifier")
        else:
            error(f"Illegal {token}")
            self.scanner.get_next_token()
            transition_diagram_type_specifier()

    def transition_diagram_params():
        # for this rule: Params -> int ID Param-prime Param-list | void
        token = self.scanner.get_current_token()
        if token == "int":
            match_token("int")
            match_token("ID")
            transition_diagram_param_prime()
            transition_diagram_param_list()
        elif token == "void":
            match_token("void")
        elif token in self.follow_sets["Params"]:
            if "Epsilon" in self.first_sets["Params"]:
                return
            else:
                error(f"Missing Params")
        else:
            error(f"Illegal {token}")
            self.scanner.get_next_token()
            transition_diagram_params()

    def transition_diagram_param_list():
        # for this rule: Param-list -> , Param Param-list | Epsilon
        token = self.scanner.get_current_token()
        if token == ",":
            match_token(",")
            transition_diagram_param()
            transition_diagram_param_list()
        elif token in self.follow_sets["Param_list"]:
            if "Epsilon" in self.first_sets["Param_list"]:
                return
            else:
                error(f"Missing Param_list")
        else:
            error(f"Illegal {token}")
            self.scanner.get_next_token()
            transition_diagram_param_list()

    def transition_diagram_param():
        # for this rule: Param -> Declaration-initial Param-prime
        token = self.scanner.get_current_token()
        if token in self.first_sets["Declaration_initial"]:
            transition_diagram_declaration_initial()
            transition_diagram_param_prime()
        elif token in self.follow_sets["Param"]:
            if "Epsilon" in self.first_sets["Param"]:
                return
            else:
                error(f"Missing Param")
        else:
            error(f"Illegal {token}")
            self.scanner.get_next_token()
            transition_diagram_param()

    def transition_diagram_param_prime():
        # for this rule: Param-prime -> [ ] | Epsilon
        token = self.scanner.get_current_token()
        if token == "[":
            match_token("[")
            match_token("]")
        elif token in self.follow_sets["Param_prime"]:
            if "Epsilon" in self.first_sets["Param_prime"]:
                return
            else:
                error(f"Missing Param_prime")
        else:
            error(f"Illegal {token}")
            self.scanner.get_next_token()
            transition_diagram_param_prime()

    def transition_diagram_compound_stmt():
        # for this rule: Compound-stmt -> { Declaration-list Statement-list }
        token = self.scanner.get_current_token()
        if token == "{":
            match_token("{")
            transition_diagram_declaration_list()
            transition_diagram_statement_list()
            match_token("}")
        elif token in self.follow_sets["Compound_stmt"]:
            if "Epsilon" in self.first_sets["Compound_stmt"]:
                return
            else:
                error(f"Missing Compound_stmt")
        else:
            error(f"Illegal {token}")
            self.scanner.get_next_token()
            transition_diagram_compound_stmt()

    def transition_diagram_statement_list():
        # for this rule: Statement-list -> Statement Statement-list | Epsilon
        token = self.scanner.get_current_token()
        if token in self.first_sets["Statement"]:
            transition_diagram_statement()
            transition_diagram_statement_list()
        elif token in self.follow_sets["Statement_list"]:
            if "Epsilon" in self.first_sets["Statement_list"]:
                return
            else:
                error(f"Missing Statement_list")
        else:
            error(f"Illegal {token}")
            self.scanner.get_next_token()
            transition_diagram_statement_list()

    def transition_diagram_statement():
        # for this rule: Statement -> Expression-stmt | Compound-stmt | Selection-stmt | Iteration-stmt | Return-stmt
        token = self.scanner.get_current_token()
        if token in self.first_sets["Expression_stmt"]:
            transition_diagram_expression_stmt()
        elif token in self.first_sets["Compound_stmt"]:
            transition_diagram_compound_stmt()
        elif token in self.first_sets["Selection_stmt"]:
            transition_diagram_selection_stmt()
        elif token in self.first_sets["Iteration_stmt"]:
            transition_diagram_iteration_stmt()
        elif token in self.first_sets["Return_stmt"]:
            transition_diagram_return_stmt()
        elif token in self.follow_sets["Statement"]:
            if "Epsilon" in self.first_sets["Statement"]:
                return
            else:
                error(f"Missing Statement")
        else:
            error(f"Illegal {token}")
            self.scanner.get_next_token()
            transition_diagram_statement()

    def transition_diagram_expression_stmt():
        # for this rule: Expression-stmt -> Expression ; | break ; | ;
        token = self.scanner.get_current_token()
        if token in self.first_sets["Expression"]:
            transition_diagram_expression()
            match_token(";")
        elif token == "break":
            match_token("break")
            match_token(";")
        elif token == ";":
            match_token(";")
        elif token in self.follow_sets["Expression_stmt"]:
            if "Epsilon" in self.first_sets["Expression_stmt"]:
                return
            else:
                error(f"Missing Expression_stmt")
        else:
            error(f"Illegal {token}")
            self.scanner.get_next_token()
            transition_diagram_expression_stmt()

    def transition_diagram_b():
        # for this rule: B -> = Expression | [ Expression ] H | Simple-expression-prime
        token = self.scanner.get_current_token()
        if token == "=":
            match_token("=")
            transition_diagram_expression()
        elif token == "[":
            match_token("[")
            transition_diagram_expression()
            match_token("]")
            transition_diagram_h()
        elif token in self.first_sets["Simple_expression_prime"]:
            transition_diagram_simple_expression_prime()
        elif token in self.follow_sets["B"]:
            if "Epsilon" in self.first_sets["B"]:
                return
            else:
                error(f"Missing B")
        else:
            error(f"Illegal {token}")
            self.scanner.get_next_token()
            transition_diagram_b()

    def transition_diagram_factor_prime():
        # for this rule: Factor-prime -> ( Args ) | Var-prime
        token = self.scanner.get_current_token()
        if token == "(":
            match_token("(")
            transition_diagram_args()
            match_token(")")
        elif token in self.first_sets["Var_prime"]:
            transition_diagram_var_prime()
        elif token in self.follow_sets["Factor_prime"]:
            if "Epsilon" in self.first_sets["Factor_prime"]:
                return
            else:
                error(f"Missing Factor_prime")
        else:
            error(f"Illegal {token}")
            self.scanner.get_next_token()
            transition_diagram_factor_prime()

    def transition_diagram_factor_zegond():
        # for this rule: Factor-zegond -> ( Expression ) | NUM
        token = self.scanner.get_current_token()
        if token == "(":
            match_token("(")
            transition_diagram_expression()
            match_token(")")
        elif token == "NUM":
            match_token("NUM")
        elif token in self.follow_sets["Factor_zegond"]:
            if "Epsilon" in self.first_sets["Factor_zegond"]:
                return
            else:
                error(f"Missing Factor_zegond")
        else:
            error(f"Illegal {token}")
            self.scanner.get_next_token()
            transition_diagram_factor_zegond()

    def transition_diagram_args():
        # for this rule: Args -> Arg-list | Epsilon
        token = self.scanner.get_current_token()
        if token in self.first_sets["Arg_list"]:
            transition_diagram_arg_list()
        elif token in self.follow_sets["Args"]:
            if "Epsilon" in self.first_sets["Args"]:
                return
            else:
                error(f"Missing Args")
        else:
            error(f"Illegal {token}")
            self.scanner.get_next_token()
            transition_diagram_args()

    def transition_diagram_arg_list():
        # for this rule: Arg-list -> Expression Arg-list-prime
        token = self.scanner.get_current_token()
        if token in self.first_sets["Expression"]:
            transition_diagram_expression()
            transition_diagram_arg_list_prime()
        elif token in self.follow_sets["Arg_list"]:
            if "Epsilon" in self.first_sets["Arg_list"]:
                return
            else:
                error(f"Missing Arg_list")
        else:
            error(f"Illegal {token}")
            self.scanner.get_next_token()
            transition_diagram_arg_list()

    def transition_diagram_arg_list_prime():
        # for this rule: Arg-list-prime -> , Expression Arg-list-prime | Epsilon
        token = self.scanner.get_current_token()
        if token == ",":
            match_token(",")
            transition_diagram_expression()
            transition_diagram_arg_list_prime()
        elif token in self.follow_sets["Arg_list_prime"]:
            if "Epsilon" in self.first_sets["Arg_list_prime"]:
                return
            else:
                error(f"Missing Arg_list_prime")
        else:
            error(f"Illegal {token}")
            self.scanner.get_next_token()
            transition_diagram_arg_list_prime()

    def transition_diagram_h():
        token = self.scanner.get_current_token()[0]
        if token in self.first_sets["Expression"]:
            transition_diagram_expression()
        elif token in self.first_sets["G"]:
            transition_diagram_g()
            transition_diagram_d()
            transition_diagram_c()
        elif token in self.follow_sets["H"]:
            if "Epsilon" in self.first_sets["H"]:
                return
            else:
                error(f"Missing H")
        else:
            error(f"Illegal {token}")
            transition_diagram_h()

    def transition_diagram_simple_expression_zegond():
        token = self.scanner.get_current_token()[0]
        if token in self.first_sets["Additive_expression_zegond"]:
            transition_diagram_additive_expression_zegond()
            transition_diagram_c()
        elif token in self.follow_sets["Simple_expression_zegond"]:
            if "Epsilon" in self.first_sets["Simple_expression_zegond"]:
                return
            else:
                error(f"Missing H")
        else:
            error(f"Illegal {token}")
            transition_diagram_simple_expression_zegond()

    def transition_diagram_simple_expression_prime():
        token = self.scanner.get_current_token()[0]
        if token in self.first_sets["Additive_expression_prime"]:
            transition_diagram_additive_expression_prime()
            transition_diagram_c()
        elif token in self.follow_sets["Simple_expression_prime"]:
            if "Epsilon" in self.first_sets["Simple_expression_prime"]:
                return
            else:
                error(f"Missing Simple_expression_prime")
        else:
            error(f"Illegal {token}")
            transition_diagram_simple_expression_prime()

    def transition_diagram_c():
        token = self.scanner.get_current_token()[0]
        if token in self.first_sets["Relop"]:
            transition_diagram_relop()
            transition_diagram_additive_expression()
        elif token in self.follow_sets["C"]:
            if "Epsilon" in self.first_sets["C"]:
                return
            else:
                error(f"Missing c")
        else:
            error(f"Illegal {token}")
            transition_diagram_c()

    def transition_diagram_relop():
        token = self.scanner.get_current_token()
        if match_token("SYMBOL"):
            if token[1] == "<":
                pass
            if token[1] == "==":
                pass
            else:
                error("Illegal {token[1]}")
        else:
            error(f"Illegal {token[0]}")
            transition_diagram_relop()

    def transition_diagram_additive_expression():
        token = self.scanner.get_current_token()[0]
        if token in self.first_sets["Term"]:
            transition_diagram_term()
            transition_diagram_d()
        elif token in self.follow_sets["Additive_expression"]:
            if "Epsilon" in self.first_sets["Additive_expression"]:
                return
            else:
                error(f"Missing Additive_expression")
        else:
            error(f"Illegal {token}")
            transition_diagram_additive_expression()

    def transition_diagram_additive_expression_prime():
        token = self.scanner.get_current_token()[0]
        if token in self.first_sets["Term_prime"]:
            transition_diagram_term_prime()
            transition_diagram_d()
        elif token in self.follow_sets["Additive_expression_prime"]:
            if "Epsilon" in self.first_sets["Additive_expression_prime"]:
                return
            else:
                error(f"Missing Additive_expression_prime")
        else:
            error(f"Illegal {token}")
            transition_diagram_additive_expression_prime()

    def transition_diagram_additive_expression_zegond():
        token = self.scanner.get_current_token()[0]
        if token in self.first_sets["Term_zegond"]:
            transition_diagram_term_zegond()
            transition_diagram_d()
        elif token in self.follow_sets["Additive_expression_zegond"]:
            if "Epsilon" in self.first_sets["Additive_expression_zegond"]:
                return
            else:
                error(f"Missing Additive_expression_zegond")
        else:
            error(f"Illegal {token}")
            transition_diagram_additive_expression_zegond()

    def transition_diagram_d():
        token = self.scanner.get_current_token()[0]
        if token in self.first_sets["Addop"]:
            transition_diagram_addop()
            transition_diagram_term()
            transition_diagram_d()
        elif token in self.follow_sets["D"]:
            if "Epsilon" in self.first_sets["D"]:
                return
            else:
                error(f"Missing D")
        else:
            error(f"Illegal {token}")
            transition_diagram_d()

    def transition_diagram_addop():
        token = self.scanner.get_current_token()
        if match_token("SYMBOL"):
            if token[1] == "+":
                pass
            if token[1] == "-":
                pass
            else:
                error("Illegal {token[1]}")
        else:
            error(f"Illegal {token[0]}")
            transition_diagram_addop()

    def transition_diagram_term():
        token = self.scanner.get_current_token()[0]
        if token in self.first_sets["Factor"]:
            transition_diagram_factor()
            transition_diagram_g()
        elif token in self.follow_sets["Term"]:
            if "Epsilon" in self.first_sets["Term"]:
                return
            else:
                error(f"Missing Term")
        else:
            error(f"Illegal {token}")
            transition_diagram_term()

    def transition_diagram_term_prime():
        token = self.scanner.get_current_token()[0]
        if token in self.first_sets["Factor_prime"]:
            transition_diagram_factor_prime()
            transition_diagram_g()
        elif token in self.follow_sets["Term_prime"]:
            if "Epsilon" in self.first_sets["Term_prime"]:
                return
            else:
                error(f"Missing Term_prime")
        else:
            error(f"Illegal {token}")
            transition_diagram_term_prime()

    def transition_diagram_term_zegond():
        token = self.scanner.get_current_token()[0]
        if token in self.first_sets["Factor_zegond"]:
            transition_diagram_factor_zegond()
            transition_diagram_g()
        elif token in self.follow_sets["Term_zegond"]:
            if "Epsilon" in self.first_sets["Term_zegond"]:
                return
            else:
                error(f"Missing Term_zegond")
        else:
            error(f"Illegal {token}")
            transition_diagram_term_zegond()

    def transition_diagram_g():
        token = self.scanner.get_current_token()
        if token[1] == "*":
            match_token("SYMBOL")
            transition_diagram_factor()
            transition_diagram_g()
        elif token in self.follow_sets["G"]:
            if "Epsilon" in self.first_sets["G"]:
                return
            else:
                error(f"Missing G")
        else:
            error(f"Illegal {token[0]}")
            transition_diagram_g()

    def transition_diagram_factor():
        token = self.scanner.get_current_token()
        if token[1] == "(":
            match_token("SYMBOL")
            transition_diagram_expression()
            if self.scanner.get_current_token()[1] == ")":
                match_token("SYMBOL")
        elif token[0] == "ID":
            match_token("ID")
            transition_diagram_var_call_prime()
        elif token[0] == "NUM":
            match_token("NUM")
        elif token in self.follow_sets["Factor"]:
            if "Epsilon" in self.first_sets["Factor"]:
                return
            else:
                error(f"Missing Factor")
        else:
            error(f"Illegal {token[0]}")
            transition_diagram_factor()

    def transition_diagram_var_call_prime():
        token = self.scanner.get_current_token()
        if token[1] == "(":
            match_token("SYMBOL")
            transition_diagram_args()
            if self.scanner.get_current_token()[1] == ")":
                match_token("SYMBOL")
        elif token in self.first_sets["Var_prime"]:
            transition_diagram_var_prime()
        elif token in self.follow_sets["Var_call_prime"]:
            if "Epsilon" in self.first_sets["Var_call_prime"]:
                return
            else:
                error(f"Missing Var_call_prime")
        else:
            error(f"Illegal {token[0]}")
            transition_diagram_var_call_prime()

    def transition_diagram_var_prime():
        token = self.scanner.get_current_token()
        if token[1] == "[":
            match_token("SYMBOL")
            transition_diagram_expression()
            if self.scanner.get_current_token()[1] == "]":
                match_token("SYMBOL")
        elif token in self.follow_sets["Var_prime"]:
            if "Epsilon" in self.first_sets["Var_prime"]:
                return
            else:
                error(f"Missing Var_prime")
        else:
            error(f"Illegal {token[0]}")
            transition_diagram_var_prime()
