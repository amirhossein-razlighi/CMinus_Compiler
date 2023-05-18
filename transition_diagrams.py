from scanner import Scanner
from anytree import Node, RenderTree
import sys


class Parser:
    def __init__(self, scanner, terminals, non_terminals, first_sets, follow_sets):
        self.scanner = scanner
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.first_sets = first_sets
        self.follow_sets = follow_sets
        self.errors = []
        self.tree = None

    def parse(self):
        # call get next token for the first time
        self.scanner.get_next_token()
        rl = sys.getrecursionlimit()
        print(rl)
        sys.setrecursionlimit(3000)
        res = self.transition_diagram_program()
        sys.setrecursionlimit(rl)
        return res


    def match_token(self, expected_token, parent):
        if self.scanner.get_current_token()[0] == expected_token:

            # add node to tree
            token_node = Node(expected_token, parent=parent)

            self.scanner.get_next_token()
            return True
        else:
            return False

    def error(self, message):
        self.errors.append((self.scanner.get_line_number(), message))

    def transition_diagram_program(self):
        # for this rule: Program -> Declaration-list

        # add root node
        program_node = Node("Program")
        self.tree = program_node

        token = self.scanner.get_current_token()[0]
        if token in self.first_sets["Declaration_list"]:
            self.transition_diagram_declaration_list(parent=program_node)
        elif token in self.follow_sets["Program"]:
            # remove root node
            program_node = None
            self.tree = None
            if "epsilon" in self.first_sets["Program"]:
                return
            else:
                self.error(f"Missing Program")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove root node
            program_node = None
            self.tree = None
            self.transition_diagram_program()

    def transition_diagram_declaration_list(self, parent):
        # for this rule: Declaration-list -> Declaration Declaration-list | epsilon

        # add node to tree
        declaration_list_node = Node("Declaration_list", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token in self.first_sets["Declaration"]:
            self.transition_diagram_declaration(parent=declaration_list_node)
            self.transition_diagram_declaration_list(parent=declaration_list_node)
        elif token in self.follow_sets["Declaration_list"]:
            # remove node from tree
            declaration_list_node.parent = None
            if "epsilon" in self.first_sets["Declaration_list"]:
                return
            else:
                self.error(f"Missing Declaration_list")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            declaration_list_node.parent = None
            self.transition_diagram_declaration_list(parent)

    def transition_diagram_declaration(self, parent):
        # for this rule: Declaration -> Declaration-initial Declaration-prime

        # add node to tree
        declaration_node = Node("Declaration", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token in self.first_sets["Declaration_initial"]:
            self.transition_diagram_declaration_initial(parent=declaration_node)
            self.transition_diagram_declaration_prime(parent=declaration_node)
        elif token in self.follow_sets["Declaration"]:
            if "epsilon" in self.first_sets["Declaration"]:
                # remove node from tree
                declaration_node.parent = None
                return
            else:
                self.error(f"Missing Declaration")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            declaration_node.parent = None
            self.transition_diagram_declaration(parent)

    def transition_diagram_declaration_initial(self, parent):
        # for this rule: Declaration-initial -> Type-specifier ID

        # add node to tree
        declaration_inital_node = Node("Declaration-initial", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token in self.first_sets["Type_specifier"]:
            self.transition_diagram_type_specifier(parent=parent)
            matched = self.match_token("ID",parent)
            if not matched:
                self.error(f"Missing ID")
        elif token in self.follow_sets["Declaration_initial"]:
            # remove node from tree
            declaration_inital_node.parent = None
            if "epsilon" in self.first_sets["Declaration_initial"]:
                return
            else:
                self.error(f"Missing Declaration_initial")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            declaration_inital_node.parent = None
            self.transition_diagram_declaration_initial(parent)

    def transition_diagram_declaration_prime(self, parent):
        # for this rule: Declaration-prime -> Fun-declaration-prime | Var-declaration-prime

        # add node to tree
        declaration_prime_node = Node("Declaration-prime", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token in self.first_sets["Fun_declaration_prime"]:
            self.transition_diagram_fun_declaration_prime(parent=declaration_prime_node)
        elif token in self.first_sets["Var_declaration_prime"]:
            self.transition_diagram_var_declaration_prime(parent=declaration_prime_node)
        elif token in self.follow_sets["Declaration_prime"]:
            # remove node from tree
            declaration_prime_node.parent = None
            if "epsilon" in self.first_sets["Declaration_prime"]:
                return
            else:
                self.error(f"Missing Declaration_prime")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            declaration_prime_node.parent = None
            self.transition_diagram_declaration_prime(parent)

    def transition_diagram_var_declaration_prime(self, parent):
        # for this rule: Var-declaration-prime -> ; | [ NUM ] ;

        # add node to tree
        var_declaration_prime_node = Node("Var-declaration-prime", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token == ";":
            self.match_token(";", var_declaration_prime_node)
        elif token == "[":
            self.match_token("[", var_declaration_prime_node)
            if not self.match_token("NUM", var_declaration_prime_node):
                self.error(f"Missing NUM")
            if not self.match_token("]", var_declaration_prime_node):
                self.error(f"Missing ]")
            if not self.match_token(";", var_declaration_prime_node):
                self.error(f"Missing ;")
        elif token in self.follow_sets["Var_declaration_prime"]:
            # remove node from tree
            var_declaration_prime_node.parent = None
            if "epsilon" in self.first_sets["Var_declaration_prime"]:
                return
            else:
                self.error(f"Missing Var_declaration_prime")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            var_declaration_prime_node.parent = None
            self.transition_diagram_var_declaration_prime(parent)

    def transition_diagram_fun_declaration_prime(self, parent):
        # for this rule: Fun-declaration-prime -> ( Params ) Compound-stmt

        # add node to tree
        fun_declaration_prime_node = Node("fun-declaration-prime", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token == "(":
            self.match_token("(", fun_declaration_prime_node)
            self.transition_diagram_params(parent=fun_declaration_prime_node)
            if not self.match_token(")", fun_declaration_prime_node):
                self.error(f"Missing )")
            self.transition_diagram_compound_stmt(parent=fun_declaration_prime_node)
        elif token in self.follow_sets["Fun_declaration_prime"]:
            # remove node from tree
            fun_declaration_prime_node.parent = None
            if "epsilon" in self.first_sets["Fun_declaration_prime"]:
                return
            else:
                self.error(f"Missing Fun_declaration_prime")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            fun_declaration_prime_node.parent = None
            self.transition_diagram_fun_declaration_prime(parent)

    def transition_diagram_type_specifier(self, parent):
        # for this rule: Type-specifier -> int | void
        token = self.scanner.get_current_token()[0]

        # add node to tree
        type_specifier_node = Node("Type-specifier", parent=parent)

        if token == "int":
            self.match_token("int", type_specifier_node)
        elif token == "void":
            self.match_token("void", type_specifier_node)
        elif token in self.follow_sets["Type_specifier"]:
            # remove node from tree
            type_specifier_node.parent = None
            if "epsilon" in self.first_sets["Type_specifier"]:
                return
            else:
                self.error(f"Missing Type_specifier")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            type_specifier_node.parent = None
            self.transition_diagram_type_specifier(parent)

    def transition_diagram_params(self, parent):
        # for this rule: Params -> int ID Param-prime Param-list | void

        # add node to tree
        params_node = Node("Params", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token == "int":
            self.match_token("int", params_node)
            if not self.match_token("ID", params_node):
                self.error(f"Missing ID")
            self.transition_diagram_param_prime(parent=params_node)
            self.transition_diagram_param_list(parent=params_node)
        elif token == "void":
            self.match_token("void", params_node)
        elif token in self.follow_sets["Params"]:
            # remove node from tree
            params_node.parent = None
            if "epsilon" in self.first_sets["Params"]:
                return
            else:
                self.error(f"Missing Params")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            params_node.parent = None
            self.transition_diagram_params(parent)

    def transition_diagram_param_list(self, parent):
        # for this rule: Param-list -> , Param Param-list | epsilon

        # add node to tree
        param_list_node = Node("Param-list", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token == ",":
            self.match_token(",", param_list_node)
            self.transition_diagram_param(parent=param_list_node)
            self.transition_diagram_param_list(parent=param_list_node)
        elif token in self.follow_sets["Param_list"]:
            # remove node from tree
            param_list_node.parent = None
            if "epsilon" in self.first_sets["Param_list"]:
                return
            else:
                self.error(f"Missing Param_list")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            param_list_node.parent = None
            self.transition_diagram_param_list(parent)

    def transition_diagram_param(self, parent):
        # for this rule: Param -> Declaration-initial Param-prime

        # add node to tree
        param_node = Node("Param", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token in self.first_sets["Declaration_initial"]:
            self.transition_diagram_declaration_initial(parent=param_node)
            self.transition_diagram_param_prime(parent=param_node)
        elif token in self.follow_sets["Param"]:
            if "epsilon" in self.first_sets["Param"]:
            # remove node from tree
                param_node.parent = None
                return
            else:
                self.error(f"Missing Param")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            param_node.parent = None
            self.transition_diagram_param(parent)

    def transition_diagram_param_prime(self, parent):
        # for this rule: Param-prime -> [ ] | epsilon

        # add node to tree
        param_prime_node = Node("Param-prime", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token == "[":
            self.match_token("[", param_prime_node)
            if not self.match_token("]", param_prime_node):
                self.error(f"Missing ]")
        elif token in self.follow_sets["Param_prime"]:
            # remove node from tree
            param_prime_node.parent = None
            if "epsilon" in self.first_sets["Param_prime"]:
                return
            else:
                self.error(f"Missing Param_prime")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            param_prime_node.parent = None
            self.transition_diagram_param_prime(parent)

    def transition_diagram_compound_stmt(self, parent):
        # for this rule: Compound-stmt -> { Declaration-list Statement-list }

        # add node to tree
        compound_stmt_node = Node("Compound-stmt", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token == "{":
            self.match_token("{", compound_stmt_node)
            self.transition_diagram_declaration_list(parent=compound_stmt_node)
            self.transition_diagram_statement_list(parent=compound_stmt_node)
            if not self.match_token("}", compound_stmt_node):
                self.error("Missing }")
        elif token in self.follow_sets["Compound_stmt"]:
            # remove node from tree
            compound_stmt_node.parent = None
            if "epsilon" in self.first_sets["Compound_stmt"]:
                return
            else:
                self.error(f"Missing Compound_stmt")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            compound_stmt_node.parent = None
            self.transition_diagram_compound_stmt(parent)

    def transition_diagram_statement_list(self, parent):
        # for this rule: Statement-list -> Statement Statement-list | epsilon

        # add node to tree
        compound_list_node = Node("Compound-list", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token in self.first_sets["Statement"]:
            self.transition_diagram_statement(parent=compound_list_node)
            self.transition_diagram_statement_list(parent=compound_list_node)
        elif token in self.follow_sets["Statement_list"]:
            # remove node from tree
            compound_list_node.parent = None
            if "epsilon" in self.first_sets["Statement_list"]:
                return
            else:
                self.error(f"Missing Statement_list")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            compound_list_node.parent = None
            self.transition_diagram_statement_list(parent)

    def transition_diagram_statement(self, parent):
        # for this rule: Statement -> Expression-stmt | Compound-stmt | Selection-stmt | Iteration-stmt | Return-stmt

        # add node to tree
        statement_node = Node("Statement", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token in self.first_sets["Expression_stmt"]:
            self.transition_diagram_expression_stmt(parent=statement_node)
        elif token in self.first_sets["Compound_stmt"]:
            self.transition_diagram_compound_stmt(parent=statement_node)
        elif token in self.first_sets["Selection_stmt"]:
            self.transition_diagram_selection_stmt(parent=statement_node)
        elif token in self.first_sets["Iteration_stmt"]:
            self.transition_diagram_iteration_stmt(parent=statement_node)
        elif token in self.first_sets["Return_stmt"]:
            self.transition_diagram_return_stmt(parent=statement_node)
        elif token in self.follow_sets["Statement"]:
            # remove node from tree
            statement_node.parent = None
            if "epsilon" in self.first_sets["Statement"]:
                return
            else:
                self.error(f"Missing Statement")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            statement_node.parent = None
            self.transition_diagram_statement(parent)

    def transition_diagram_expression_stmt(self, parent):
        # for this rule: Expression-stmt -> Expression ; | break ; | ;

        # add node to tree
        expression_stmt_node = Node("Expression_stmt", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token in self.first_sets["Expression"]:
            self.transition_diagram_expression(parent=expression_stmt_node)
            if not self.match_token(";", expression_stmt_node):
                self.error(f"Missing ;")
        elif token == "break":
            self.match_token("break", expression_stmt_node)
            if not self.match_token(";", expression_stmt_node):
                self.error(f"Missing ;")
        elif token == ";":
            self.match_token(";", expression_stmt_node)
        elif token in self.follow_sets["Expression_stmt"]:
            # remove node from tree
            exoression_stmt_node.parent = None
            if "epsilon" in self.first_sets["Expression_stmt"]:
                return
            else:
                self.error(f"Missing Expression_stmt")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            exoression_stmt_node.parent = None
            self.transition_diagram_expression_stmt(parent)

    def transition_diagram_b(self, parent):
        # for this rule: B -> = Expression | [ Expression ] H | Simple-expression-prime

        # add node to tree
        b_node = Node("B", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token == "=":
            self.match_token("=", b_node)
            self.transition_diagram_expression(parent=b_node)
        elif token == "[":
            self.match_token("[", b_node)
            self.transition_diagram_expression(parent=b_node)
            if not self.match_token("]", b_node):
                self.error(f"Missing ]")
            self.transition_diagram_h(parent=b_node)
        elif token in self.first_sets["Simple_expression_prime"]:
            self.transition_diagram_simple_expression_prime(parent=b_node)
        elif token in self.follow_sets["B"]:
            # remove node from tree
            b_node.parent = None
            if "epsilon" in self.first_sets["B"]:
                return
            else:
                self.error(f"Missing B")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            b_node.parent = None
            self.transition_diagram_b(parent)

    def transition_diagram_factor_prime(self, parent):
        # for this rule: Factor-prime -> ( Args ) | Var-prime

        # add node to tree
        factor_prime_node = Node("Factor-prime", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token == "(":
            self.match_token("(", factor_prime_node)
            self.transition_diagram_args(parent=factor_prime_node)
            if not self.match_token(")", factor_prime_node):
                self.error(f"Missing )")
        elif token in self.first_sets["Var_prime"]:
            self.transition_diagram_var_prime(parent=factor_prime_node)
        elif token in self.follow_sets["Factor_prime"]:
            # remove node from tree
            factor_prime_node.parent = None
            if "epsilon" in self.first_sets["Factor_prime"]:
                return
            else:
                self.error(f"Missing Factor_prime")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            factor_prime_node.parent = None
            self.transition_diagram_factor_prime(parent)

    def transition_diagram_factor_zegond(self, parent):
        # for this rule: Factor-zegond -> ( Expression ) | NUM

        # add node to tree
        factor_zegond_node = Node("Factor-zegond", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token == "(":
            self.match_token("(", factor_zegond_node)
            self.transition_diagram_expression(parent=factor_zegond_node)
            if not self.match_token(")", factor_zegond_node):
                self.error(f"Missing )")
        elif token == "NUM":
            self.match_token("NUM", factor_zegond_node)
        elif token in self.follow_sets["Factor_zegond"]:
            # remove node from tree
            factor_zegond_node.parent = None
            if "epsilon" in self.first_sets["Factor_zegond"]:
                return
            else:
                self.error(f"Missing Factor_zegond")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            factor_zegond_node.parent = None
            self.transition_diagram_factor_zegond(parent)

    def transition_diagram_args(self, parent):
        # for this rule: Args -> Arg-list | epsilon

        # add node to tree
        args_node = Node("Args", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token in self.first_sets["Arg_list"]:
            self.transition_diagram_arg_list(parent=args_node)
        elif token in self.follow_sets["Args"]:
            # remove node from tree
            args_node.parent = None
            if "epsilon" in self.first_sets["Args"]:
                return
            else:
                self.error(f"Missing Args")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            args_node.parent = None
            self.transition_diagram_args(parent)

    def transition_diagram_arg_list(self, parent):
        # for this rule: Arg-list -> Expression Arg-list-prime

        # add node to tree
        arg_list_node = Node("Arg-list", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token in self.first_sets["Expression"]:
            self.transition_diagram_expression(parent=arg_list_node)
            self.transition_diagram_arg_list_prime(parent=arg_list_node)
        elif token in self.follow_sets["Arg_list"]:
            # remove node from tree
            arg_list_node.parent = None
            if "epsilon" in self.first_sets["Arg_list"]:
                return
            else:
                self.error(f"Missing Arg_list")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            arg_list_node.parent = None
            self.transition_diagram_arg_list(parent)

    def transition_diagram_arg_list_prime(self, parent):
        # for this rule: Arg-list-prime -> , Expression Arg-list-prime | epsilon

        # add node to tree
        arg_list_prime_node = Node("Arg-list-prime", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token == ",":
            self.match_token(",", arg_list_prime_node)
            self.transition_diagram_expression(parent=arg_list_prime_node)
            self.transition_diagram_arg_list_prime(parent=arg_list_prime_node)
        elif token in self.follow_sets["Arg_list_prime"]:
            # remove node from tree
            arg_list_prime_node.parent = None
            if "epsilon" in self.first_sets["Arg_list_prime"]:
                return
            else:
                self.error(f"Missing Arg-list-prime")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            arg_list_prime_node.parent = None
            self.transition_diagram_arg_list_prime(parent)

    def transition_diagram_h(self, parent):

        # add node to tree
        h_node = Node("H", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token in self.first_sets["Expression"]:
            self.transition_diagram_expression(parent=h_node)
        elif token in self.first_sets["G"]:
            self.transition_diagram_g(parent=h_node)
            self.transition_diagram_d(parent=h_node)
            self.transition_diagram_c(parent=h_node)
        elif token in self.follow_sets["H"]:
            # remove node from tree
            h_node.parent = None
            if "epsilon" in self.first_sets["H"]:
                return
            else:
                self.error(f"Missing H")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            h_node.parent = None
            self.transition_diagram_h(parent)

    def transition_diagram_simple_expression_zegond(self, parent):

        # add node to tree
        simple_expression_zegond_node = Node("Simple-expression-zegond", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token in self.first_sets["Additive_expression_zegond"]:
            self.transition_diagram_additive_expression_zegond(parent=simple_expression_zegond_node)
            self.transition_diagram_c(parent=simple_expression_zegond_node)
        elif token in self.follow_sets["Simple_expression_zegond"]:
            # remove node from tree
            simple_expression_zegond_node.parent = None
            if "epsilon" in self.first_sets["Simple_expression_zegond"]:
                return
            else:
                self.error(f"Missing H")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            simple_expression_zegond_node.parent = None
            self.transition_diagram_simple_expression_zegond(parent)

    def transition_diagram_simple_expression_prime(self, parent):

        # add node to tree
        simple_expression_prime_node = Node("Simple-expression-prime", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token in self.first_sets["Additive_expression_prime"]:
            self.transition_diagram_additive_expression_prime(parent=simple_expression_prime_node)
            self.transition_diagram_c(parent=simple_expression_prime_node)
        elif token in self.follow_sets["Simple_expression_prime"]:
            # remove node from tree
            simple_expression_prime_node.parent = None
            if "epsilon" in self.first_sets["Simple_expression_prime"]:
                return
            else:
                self.error(f"Missing Simple-expression-prime")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            simple_expression_prime_node.parent = None
            self.transition_diagram_simple_expression_prime(parent)

    def transition_diagram_c(self, parent):

        # add node to tree
        c_node = Node("C", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token in self.first_sets["Relop"]:
            self.transition_diagram_relop(parent=c_node)
            self.transition_diagram_additive_expression(parent=c_node)
        elif token in self.follow_sets["C"]:
            # remove node from tree
            c_node.parent = None
            if "epsilon" in self.first_sets["C"]:
                return
            else:
                self.error(f"Missing c")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            c_node.parent = None
            self.transition_diagram_c(parent)

    def transition_diagram_relop(self, parent):

        # add node to tree
        relop_node = Node("Relop", parent=parent)

        token = self.scanner.get_current_token()[0]
        if self.match_token("<", relop_node):
                pass
        elif self.match_token("==", relop_node):
                pass
        elif token in self.follow_sets["Relop"]:
            # remove node from tree
            relop_node.parent = None
            if "epsilon" in self.first_sets["Relop"]:
                return
            else:
                self.error(f"Missing Relop")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            relop_node.parent = None
            self.transition_diagram_relop()

    def transition_diagram_additive_expression(self, parent):

        # add node to tree
        additive_expression_node = Node("Additive-expression", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token in self.first_sets["Term"]:
            self.transition_diagram_term(parent=additive_expression_node)
            self.transition_diagram_d(parent=additive_expression_node)
        elif token in self.follow_sets["Additive-expression"]:
            # remove node from tree
            additive_expression_node.parent = None
            if "epsilon" in self.first_sets["Additive-expression"]:
                return
            else:
                self.error(f"Missing Additive-expression")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            additive_expression_node.parent = None
            self.transition_diagram_additive_expression(parent)

    def transition_diagram_additive_expression_prime(self, parent):

        # add node to tree
        additive_expression_prime_node = Node("Additive-expression-prime", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token in self.first_sets["Term_prime"]:
            self.transition_diagram_term_prime(parent=additive_expression_prime_node)
            self.transition_diagram_d(parent=additive_expression_prime_node)
        elif token in self.follow_sets["Additive_expression_prime"]:
            # remove node from tree
            additive_expression_prime_node.parent = None
            if "epsilon" in self.first_sets["Additive_expression_prime"]:
                return
            else:
                self.error(f"Missing Additive_expression_prime")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            additive_expression_prime_node.parent = None
            self.transition_diagram_additive_expression_prime(parent)

    def transition_diagram_additive_expression_zegond(self, parent):

        # add node to tree
        additive_expression_zegond_node = Node("Additive-expression-zegond", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token in self.first_sets["Term_zegond"]:
            self.transition_diagram_term_zegond(parent=additive_expression_zegond_node)
            self.transition_diagram_d(parent=additive_expression_zegond_node)
        elif token in self.follow_sets["Additive_expression_zegond"]:
            # remove node from tree
            additive_expression_zegond_node.parent = None
            if "epsilon" in self.first_sets["Additive_expression_zegond"]:
                return
            else:
                self.error(f"Missing Additive_expression_zegond")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            additive_expression_zegond_node.parent = None
            self.transition_diagram_additive_expression_zegond(parent)

    def transition_diagram_d(self, parent):

        # add node to tree
        d_node = Node("D", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token in self.first_sets["Addop"]:
            self.transition_diagram_addop(parent=d_node)
            self.transition_diagram_term(parent=d_node)
            self.transition_diagram_d(parent=d_node)
        elif token in self.follow_sets["D"]:
            # remove node from tree
            d_node.parent = None
            if "epsilon" in self.first_sets["D"]:
                return
            else:
                self.error(f"Missing D")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            d_node.parent = None
            self.transition_diagram_d(parent)

    def transition_diagram_addop(self, parent):

        # add node to tree
        addop_node = Node("Addop", parent=parent)

        token = self.scanner.get_current_token()[0]
        if self.match_token("+", addop_node):
            pass
        elif self.match_token("-", addop_node):
            pass
        elif token in self.follow_sets["D"]:
            # remove node from tree
            addop_node.parent = None
            if "epsilon" in self.first_sets["Addop"]:
                return
            else:
                self.error(f"Missing Addop")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            addop_node.parent = None
            self.transition_diagram_addop(parent)

    def transition_diagram_term(self, parent):

        # add node to tree
        term_node = Node("Term", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token in self.first_sets["Factor"]:
            self.transition_diagram_factor(parent=term_node)
            self.transition_diagram_g(parent=term_node)
        elif token in self.follow_sets["Term"]:
            # remove node from tree
            term_node.parent = None
            if "epsilon" in self.first_sets["Term"]:
                return
            else:
                self.error(f"Missing Term")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            term_node.parent = None
            self.transition_diagram_term(parent)

    def transition_diagram_term_prime(self, parent):

        # add node to tree
        term_prime_node = Node("Term-prime", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token in self.first_sets["Factor_prime"]:
            self.transition_diagram_factor_prime(parent=term_prime_node)
            self.transition_diagram_g(parent=term_prime_node)
        elif token in self.follow_sets["Term_prime"]:
            # remove node from tree
            term_prime_node.parent = None
            if "epsilon" in self.first_sets["Term_prime"]:
                return
            else:
                self.error(f"Missing Term_prime")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            term_prime_node.parent = None
            self.transition_diagram_term_prime(parent)

    def transition_diagram_term_zegond(self, parent):

        # add node to tree
        term_zegond_node = Node("Term-zegond", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token in self.first_sets["Factor_zegond"]:
            self.transition_diagram_factor_zegond(parent=term_zegond_node)
            self.transition_diagram_g(parent=term_zegond_node)
        elif token in self.follow_sets["Term_zegond"]:
            # remove node from tree
            term_zegond_node.parent = None
            if "epsilon" in self.first_sets["Term_zegond"]:
                return
            else:
                self.error(f"Missing Term_zegond")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            term_zegond_node.parent = None
            self.transition_diagram_term_zegond(parent)

    def transition_diagram_g(self, parent):

        # add node to tree
        g_node = Node("G", parent=parent)

        token = self.scanner.get_current_token()[0]
        if self.match_token("*", g_node):
            self.transition_diagram_factor(parent=g_node)
            self.transition_diagram_g(parent=g_node)
        elif token in self.follow_sets["G"]:
            # remove node from tree
            g_node.parent = None
            if "epsilon" in self.first_sets["G"]:
                return
            else:
                self.error(f"Missing G")
        else:
            self.error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            g_node.parent = None
            self.transition_diagram_g(parent)

    def transition_diagram_factor(self, parent):
        token = self.scanner.get_current_token()

        # add node to tree
        factor_node = Node("Factor", parent=parent)

        if self.match_token("(", factor_node):
            self.transition_diagram_expression(parent=factor_node)
            if not self.match_token(")", factor_node):
                self.error(f"Missing )")
        elif self.match_token("ID", factor_node):
            self.transition_diagram_var_call_prime(parent=factor_node)
        elif self.match_token("NUM", factor_node):
            pass
        elif token in self.follow_sets["Factor"]:
            # remove node from tree
            factor_node.parent = None
            if "epsilon" in self.first_sets["Factor"]:
                return
            else:
                self.error(f"Missing Factor")
        else:
            self.error(f"Illegal {token[0]}")
            self.scanner.get_next_token()
            # remove node from tree
            factor_node.parent = None
            self.transition_diagram_factor(parent)

    def transition_diagram_var_call_prime(self, parent):

        # add node to tree
        var_call_prime_node = Node("Var-call-prime", parent=parent)

        token = self.scanner.get_current_token()
        if self.match_token("(", var_call_prime_node):
            self.transition_diagram_args(parent=var_call_prime_node)
            if not self.match_token(")", var_call_prime_node):
                self.error(f"Missing )")
        elif token in self.first_sets["Var_prime"]:
            self.transition_diagram_var_prime(parent=var_call_prime_node)
        elif token in self.follow_sets["Var_call_prime"]:
            # remove node from tree
            var_call_prime_node.parent = None
            if "epsilon" in self.first_sets["Var_call_prime"]:
                return
            else:
                self.error(f"Missing Var_call_prime")
        else:
            self.error(f"Illegal {token[0]}")
            self.scanner.get_next_token()
            # remove node from tree
            var_call_prime_node.parent = None
            self.transition_diagram_var_call_prime(parent)

    def transition_diagram_var_prime(self, parent):

        # add node to tree
        var_prime_node = Node("Var-prime", parent=parent)

        token = self.scanner.get_current_token()
        if self.match_token("[", var_prime_node):
            self.transition_diagram_expression(parent=var_prime_node)
            if not self.match_token("]", var_prime_node):
                self.error(f"Missing ]")
        elif token in self.follow_sets["Var_prime"]:
            # remove node from tree
            var_prime_node.parent = None
            if "epsilon" in self.first_sets["Var_prime"]:
                return
            else:
                self.error(f"Missing Var_prime")
        else:
            self.error(f"Illegal {token[0]}")
            self.scanner.get_next_token()
            # remove node from tree
            var_prime_node.parent = None
            self.transition_diagram_var_prime(parent)

    def transition_diagram_expression(self, parent):

        # add node to tree
        expression_node = Node("Expression", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token in self.first_sets["Simple_expression_zegond"]:
            self.transition_diagram_simple_expression_zegond(expression_node)
        elif token == "ID":
            self.match_token("ID", expression_node)
            self.transition_diagram_b(expression_node)
        elif token in self.follow_sets["Expression"]:
            # remove node from tree
            expression_node.parent = None
            if "epsilon" in self.first_sets["Expression"]:
                return
            else:
                error(f"Missing Expression")
        else:
            error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            expression_node.parent = None
            self.transition_diagram_expression(parent)

    def transition_diagram_selection_stmt(self, parent):

        # add node to tree
        selection_stmt_node = Node("Selection-stmt", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token == "if":
            self.match_token("if", selection_stmt_node)
            if not self.match_token("(", selection_stmt_node):
                self.error("Missing (")
            self.transition_diagram_expression(selection_stmt_node)
            if not self.match_token(")", selection_stmt_node):
                self.error("Missing )")
            self.transition_diagram_statement(selection_stmt_node)
            if not self.match_token("else", selection_stmt_node):
                self.error("Missing else")
            self.transition_diagram_statement(selection_stmt_node)
        elif token in self.follow_sets["Selection_stmt"]:
            # remove node from tree
            selection_stmt_node.parent = None
            if "epsilon" in self.first_sets["Selection_stmt"]:
                return
            else:
                error(f"Missing Selection-stmt")
        else:
            error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            selection_stmt_node.parent = None
            self.transition_diagram_selection_stmt(parent)

    def transition_diagram_iteration_stmt(self, parent):

        # add node to tree
        iteration_stmt_node = Node("Selection-stmt", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token == "repeat":
            self.match_token("repeat", iteration_stmt_node)
            self.transition_diagram_statement(iteration_stmt_node)
            if not self.match_token("until", iteration_stmt_node):
                self.error("Missing until")
            if not self.match_token("(", iteration_stmt_node):
                self.error("Missing (")
            self.transition_diagram_expression(iteration_stmt_node)
            if not self.match_token(")", iteration_stmt_node):
                self.error("Missing )")
            self.transition_diagram_statement(iteration_stmt_node)
        elif token in self.follow_sets["Iteration_stmt"]:
            # remove node from tree
            iteration_stmt_node.parent = None
            if "epsilon" in self.first_sets["Iteration_stmt"]:
                return
            else:
                error(f"Missing Iteration-stmt")
        else:
            error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            iteration_stmt_node.parent = None
            self.transition_diagram_iteration_stmt(parent)

    def transition_diagram_return_stmt(self, parent):

        # add node to tree
        return_stmt_node = Node("Return-stmt", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token == "return":
            self.match_token("return", return_stmt_node)
            self.transition_diagram_return_stmt_prime(return_stmt_node)
        elif token in self.follow_sets["Return_stmt"]:
            # remove node from tree
            return_stmt_node.parent = None
            if "epsilon" in self.first_sets["Return_stmt"]:
                return
            else:
                error(f"Missing Return-stmt")
        else:
            error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            return_stmt_node.parent = None
            self.transition_diagram_return_stmt(parent)

    def transition_diagram_return_stmt_prime(self, parent):

        # add node to tree
        return_stmt_node = Node("Return-stmt-prime", parent=parent)

        token = self.scanner.get_current_token()[0]
        if token == ";":
            self.match_token(";", selection_stmt_node)
        elif token in self.first_sets["Expression"]:
            self.transition_diagram_expression(return_stmt_node)
            if not self.match_token(";", return_stmt_node):
                self.error("Missing ;")
        elif token in self.follow_sets["Return_stmt_prime"]:
            # remove node from tree
            return_stmt_node.parent = None
            if "epsilon" in self.first_sets["Return_stmt_prime"]:
                return
            else:
                error(f"Missing Return-stmt-prime")
        else:
            error(f"Illegal {token}")
            self.scanner.get_next_token()
            # remove node from tree
            return_stmt_node.parent = None
            self.transition_diagram_return_stmt_prime(parent)

