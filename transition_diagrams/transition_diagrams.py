from scanner import Scanner
from anytree import Node, RenderTree
import sys
from codegen.code_gen import CodeGenerator


class Parser:
    def __init__(self, scanner, terminals, non_terminals, first_sets, follow_sets):
        self.scanner = scanner
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.first_sets = first_sets
        self.follow_sets = follow_sets
        self.errors = []
        self.tree = None
        self.grim = False
        self.code_generator = CodeGenerator.get_instance()
        self.routines_to_run = []

    def parse(self):
        # call get next token for the first time
        self.scanner.get_next_token()
        res = self.transition_diagram_program()
        return res

    def match_token(self, expected_token, parent):
        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return True
        if token0 == expected_token or token1 == expected_token:
            # add node to tree
            node = Node(f"({token0}, {token1})", parent=parent)

            self.scanner.get_next_token()
            return True
        else:
            return False

    def error(self, message):
        self.errors.append((self.scanner.get_line_number(), message))

    def transition_diagram_program(self):
        # for this rule: Program -> Declaration-list

        token0, token1, _ = self.scanner.get_current_token()

        # add root node
        node = Node("Program")
        self.tree = node

        if (
            "epsilon" in self.first_sets["Program"]
            or token0 in self.first_sets["Program"]
            or token1 in self.first_sets["Program"]
        ):
            self.transition_diagram_declaration_list(parent=node)
            if self.scanner.get_current_token()[0] == "$" and not self.grim:
                Node("$", node)
        elif (
            token0 in self.follow_sets["Program"]
            or token1 in self.follow_sets["Program"]
        ):
            if "epsilon" in self.first_sets["Program"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Program")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_program()

    def transition_diagram_declaration_list(self, parent):
        # for this rule: Declaration-list -> Declaration Declaration-list | epsilon

        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Declaration_list"]
            and "epsilon" in self.first_sets["Declaration_list"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Declaration-list", parent=parent)

        if (
            token0 in self.first_sets["Declaration_list"]
            or token1 in self.first_sets["Declaration_list"]
        ):
            self.transition_diagram_declaration(parent=node)
            self.transition_diagram_declaration_list(parent=node)
        elif (
            token0 in self.follow_sets["Declaration_list"]
            or token1 in self.follow_sets["Declaration_list"]
        ):
            if "epsilon" in self.first_sets["Declaration_list"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Declaration_list")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_declaration_list(parent)

    def transition_diagram_declaration(self, parent):
        # for this rule: Declaration -> Declaration-initial Declaration-prime

        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Declaration"]
            and "epsilon" in self.first_sets["Declaration"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Declaration", parent=parent)

        if (
            "epsilon" in self.first_sets["Declaration"]
            or token0 in self.first_sets["Declaration"]
            or token1 in self.first_sets["Declaration"]
        ):
            self.transition_diagram_declaration_initial(parent=node)
            self.transition_diagram_declaration_prime(parent=node)
        elif (
            token0 in self.follow_sets["Declaration"]
            or token1 in self.follow_sets["Declaration"]
        ):
            if "epsilon" in self.first_sets["Declaration"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Declaration")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_declaration(parent)

    def transition_diagram_declaration_initial(self, parent):
        # for this rule: Declaration-initial -> Type-specifier ID

        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Declaration_initial"]
            and "epsilon" in self.first_sets["Declaration_initial"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Declaration-initial", parent=parent)

        if (
            "epsilon" in self.first_sets["Declaration_initial"]
            or token0 in self.first_sets["Declaration_initial"]
            or token1 in self.first_sets["Declaration_initial"]
        ):
            self.transition_diagram_type_specifier(parent=node)

            _, token, _ = self.scanner.get_current_token()
            matched = self.match_token("ID", node)
            if not matched:
                self.error(f"missing ID")
            else:
                if not token == "main":
                    # Action: PID
                    self.code_generator.push_id(
                        self.code_generator.get_token_address(token)
                    )
                else:
                    self.code_generator.main_jp()
        elif (
            token0 in self.follow_sets["Declaration_initial"]
            or token1 in self.follow_sets["Declaration_initial"]
        ):
            if "epsilon" in self.first_sets["Declaration_initial"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Declaration-initial")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_declaration_initial(parent)

    def transition_diagram_declaration_prime(self, parent):
        # for this rule: Declaration-prime -> Fun-declaration-prime | Var-declaration-prime

        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Declaration_prime"]
            and "epsilon" in self.first_sets["Declaration_prime"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Declaration-prime", parent=parent)

        if (
            "epsilon" in self.first_sets["Declaration_prime"]
            or token0 in self.first_sets["Declaration_prime"]
            or token1 in self.first_sets["Declaration_prime"]
        ):
            if (
                token0 in self.first_sets["Fun_declaration_prime"]
                or token1 in self.first_sets["Fun_declaration_prime"]
            ):
                self.transition_diagram_fun_declaration_prime(parent=node)
            else:
                self.transition_diagram_var_declaration_prime(parent=node)
        elif (
            token0 in self.follow_sets["Declaration_prime"]
            or token1 in self.follow_sets["Declaration_prime"]
        ):
            if "epsilon" in self.first_sets["Declaration_prime"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Declaration-prime")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_declaration_prime(parent)

    def transition_diagram_var_declaration_prime(self, parent):
        # for this rule: Var-declaration-prime -> ; | [ NUM ] ;

        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Var_declaration_prime"]
            and "epsilon" in self.first_sets["Var_declaration_prime"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Var-declaration-prime", parent=parent)

        if (
            token0 in self.first_sets["Var_declaration_prime"]
            or token1 in self.first_sets["Var_declaration_prime"]
        ):
            if token1 == ";":
                self.match_token(";", node)

                # Action: assign_zero
                self.code_generator.assign_zero()

            elif token1 == "[":
                self.match_token("[", node)
                size = int(self.scanner.get_current_token()[1])
                if not self.match_token("NUM", node):
                    self.error(f"missing NUM")
                if not self.match_token("]", node):
                    self.error(f"missing ]")
                if not self.match_token(";", node):
                    self.error(f"missing ;")

                # Action: assign_zero
                self.code_generator.assign_zero(is_array=True, array_size=size)
        elif (
            token0 in self.follow_sets["Var_declaration_prime"]
            or token1 in self.follow_sets["Var_declaration_prime"]
        ):
            if "epsilon" in self.first_sets["Var_declaration_prime"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Var_declaration_prime")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_var_declaration_prime(parent)

    def transition_diagram_fun_declaration_prime(self, parent):
        # for this rule: Fun-declaration-prime -> ( Params ) Compound-stmt

        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Fun_declaration_prime"]
            and "epsilon" in self.first_sets["Fun_declaration_prime"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Fun-declaration-prime", parent=parent)

        if (
            token0 in self.first_sets["Fun_declaration_prime"]
            or token1 in self.first_sets["Fun_declaration_prime"]
        ):
            if token1 == "(":
                self.match_token("(", node)
                self.transition_diagram_params(parent=node)
                if not self.match_token(")", node):
                    self.error(f"missing )")
                self.transition_diagram_compound_stmt(parent=node)
        elif (
            token0 in self.follow_sets["Fun_declaration_prime"]
            or token1 in self.follow_sets["Fun_declaration_prime"]
        ):
            if "epsilon" in self.first_sets["Fun_declaration_prime"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Fun_declaration_prime")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_fun_declaration_prime(parent)

    def transition_diagram_type_specifier(self, parent):
        # for this rule: Type-specifier -> int | void
        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Type_specifier"]
            and "epsilon" in self.first_sets["Type_specifier"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Type-specifier", parent=parent)

        if (
            token0 in self.first_sets["Type_specifier"]
            or token1 in self.first_sets["Type_specifier"]
        ):
            if token1 == "int":
                self.match_token("int", node)
            elif token1 == "void":
                self.match_token("void", node)
        elif (
            token0 in self.follow_sets["Type_specifier"]
            or token1 in self.follow_sets["Type_specifier"]
        ):
            if "epsilon" in self.first_sets["Type_specifier"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Type_specifier")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_type_specifier(parent)

    def transition_diagram_params(self, parent):
        # for this rule: Params -> int ID Param-prime Param-list | void

        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Params"] and "epsilon" in self.first_sets["Params"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Params", parent=parent)

        if token0 in self.first_sets["Params"] or token1 in self.first_sets["Params"]:
            if token1 == "int":
                self.match_token("int", node)
                if not self.match_token("ID", node):
                    self.error(f"missing ID")
                self.transition_diagram_param_prime(parent=node)
                self.transition_diagram_param_list(parent=node)
            elif token1 == "void":
                self.match_token("void", node)
        elif (
            token0 in self.follow_sets["Params"] or token1 in self.follow_sets["Params"]
        ):
            if "epsilon" in self.first_sets["Params"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Params")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_params(parent)

    def transition_diagram_param_list(self, parent):
        # for this rule: Param-list -> , Param Param-list | epsilon

        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Param_list"]
            and "epsilon" in self.first_sets["Param_list"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Param-list", parent=parent)

        if (
            token0 in self.first_sets["Param_list"]
            or token1 in self.first_sets["Param_list"]
        ):
            if token1 == ",":
                self.match_token(",", node)
                self.transition_diagram_param(parent=node)
                self.transition_diagram_param_list(parent=node)
        elif (
            token0 in self.follow_sets["Param_list"]
            or token1 in self.follow_sets["Param_list"]
        ):
            if "epsilon" in self.first_sets["Param_list"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Param_list")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_param_list(parent)

    def transition_diagram_param(self, parent):
        # for this rule: Param -> Declaration-initial Param-prime

        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Param"] and "epsilon" in self.first_sets["Param"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Param", parent=parent)

        if (
            "epsilon" in self.first_sets["Param"]
            or token0 in self.first_sets["Param"]
            or token1 in self.first_sets["Param"]
        ):
            self.transition_diagram_declaration_initial(parent=node)
            self.transition_diagram_param_prime(parent=node)
        elif token0 in self.follow_sets["Param"] or token1 in self.follow_sets["Param"]:
            if "epsilon" in self.first_sets["Param"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Param")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_param(parent)

    def transition_diagram_param_prime(self, parent):
        # for this rule: Param-prime -> [ ] | epsilon

        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Param_prime"]
            and "epsilon" in self.first_sets["Param_prime"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Param-prime", parent=parent)

        if (
            token0 in self.first_sets["Param_prime"]
            or token1 in self.first_sets["Param_prime"]
        ):
            if token1 == "[":
                self.match_token("[", node)
                if not self.match_token("]", node):
                    self.error(f"missing ]")
        elif (
            token0 in self.follow_sets["Param_prime"]
            or token1 in self.follow_sets["Param_prime"]
        ):
            if "epsilon" in self.first_sets["Param_prime"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Param_prime")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_param_prime(parent)

    def transition_diagram_compound_stmt(self, parent):
        # for this rule: Compound-stmt -> { Declaration-list Statement-list }

        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Compound_stmt"]
            and "epsilon" in self.first_sets["Compound_stmt"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Compound-stmt", parent=parent)

        if (
            token0 in self.first_sets["Compound_stmt"]
            or token1 in self.first_sets["Compound_stmt"]
        ):
            if token1 == "{":
                self.match_token("{", node)
                self.transition_diagram_declaration_list(parent=node)
                self.transition_diagram_statement_list(parent=node)
                if not self.match_token("}", node):
                    self.error("missing }")
        elif (
            token0 in self.follow_sets["Compound_stmt"]
            or token1 in self.follow_sets["Compound_stmt"]
        ):
            if "epsilon" in self.first_sets["Compound_stmt"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Compound_stmt")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_compound_stmt(parent)

    def transition_diagram_statement_list(self, parent):
        # for this rule: Statement-list -> Statement Statement-list | epsilon

        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Statement_list"]
            and "epsilon" in self.first_sets["Statement_list"]
        ):
            # if not self.grim:
            # self.grim = True
            # self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Statement-list", parent=parent)

        if (
            token0 in self.first_sets["Statement_list"]
            or token1 in self.first_sets["Statement_list"]
        ):
            self.transition_diagram_statement(parent=node)
            self.transition_diagram_statement_list(parent=node)
        elif (
            token0 in self.follow_sets["Statement_list"]
            or token1 in self.follow_sets["Statement_list"]
        ):
            if "epsilon" in self.first_sets["Statement_list"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Statement_list")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_statement_list(parent)

    def transition_diagram_statement(self, parent):
        # for this rule: Statement -> Expression-stmt | Compound-stmt | Selection-stmt | Iteration-stmt | Return-stmt

        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Statement"]
            and "epsilon" in self.first_sets["Statement"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Statement", parent=parent)

        if (
            "epsilon" in self.first_sets["Statement"]
            or token0 in self.first_sets["Statement"]
            or token1 in self.first_sets["Statement"]
        ):
            if (
                token0 in self.first_sets["Expression_stmt"]
                or token1 in self.first_sets["Expression_stmt"]
            ):
                self.transition_diagram_expression_stmt(parent=node)
            elif (
                token0 in self.first_sets["Compound_stmt"]
                or token1 in self.first_sets["Compound_stmt"]
            ):
                self.transition_diagram_compound_stmt(parent=node)
            elif (
                token0 in self.first_sets["Selection_stmt"]
                or token1 in self.first_sets["Selection_stmt"]
            ):
                self.transition_diagram_selection_stmt(parent=node)
            elif (
                token0 in self.first_sets["Iteration_stmt"]
                or token1 in self.first_sets["Iteration_stmt"]
            ):
                self.transition_diagram_iteration_stmt(parent=node)
            elif (
                token0 in self.first_sets["Return_stmt"]
                or token1 in self.first_sets["Return_stmt"]
            ):
                self.transition_diagram_return_stmt(parent=node)
        elif (
            token0 in self.follow_sets["Statement"]
            or token1 in self.follow_sets["Statement"]
        ):
            if "epsilon" in self.first_sets["Statement"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Statement")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_statement(parent)

    def transition_diagram_expression_stmt(self, parent):
        # for this rule: Expression-stmt -> Expression ; | break ; | ;

        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Expression_stmt"]
            and "epsilon" in self.first_sets["Expression_stmt"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Expression-stmt", parent=parent)

        if (
            token0 in self.first_sets["Expression_stmt"]
            or token1 in self.first_sets["Expression_stmt"]
        ):
            if (
                token0 in self.first_sets["Expression"]
                or token1 in self.first_sets["Expression"]
            ):
                self.transition_diagram_expression(parent=node)
                if not self.match_token(";", node):
                    self.error(f"missing ;")
            elif token1 == "break":
                self.match_token("break", node)
                if not self.match_token(";", node):
                    self.error(f"missing ;")

                # Action: break
                self.code_generator.break_the_jail()

            elif token1 == ";":
                self.match_token(";", node)
        elif (
            token0 in self.follow_sets["Expression_stmt"]
            or token1 in self.follow_sets["Expression_stmt"]
        ):
            if "epsilon" in self.first_sets["Expression_stmt"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Expression-stmt")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_expression_stmt(parent)

    def transition_diagram_b(self, parent):
        # for this rule: B -> = Expression | [ Expression ] H | Simple-expression-prime

        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["B"] and "epsilon" in self.first_sets["B"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node(f"B", parent=parent)

        if (
            "epsilon" in self.first_sets["B"]
            or token0 in self.first_sets["B"]
            or token1 in self.first_sets["B"]
        ):
            if token1 == "=":
                self.match_token("=", node)
                self.transition_diagram_expression(parent=node)

                # Action: assign
                self.code_generator.assign()

            elif token1 == "[":
                self.match_token("[", node)
                self.transition_diagram_expression(parent=node)
                if not self.match_token("]", node):
                    self.error(f"missing ]")

                # Action: array_access
                self.code_generator.array_access()

                self.transition_diagram_h(parent=node)
            else:
                self.transition_diagram_simple_expression_prime(parent=node)
        elif token0 in self.follow_sets["B"] or token1 in self.follow_sets["B"]:
            if "epsilon" in self.first_sets["B"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing B")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_b(parent)

    def transition_diagram_factor_prime(self, parent):
        # for this rule: Factor-prime -> ( Args ) | Var-prime

        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Factor_prime"]
            and "epsilon" in self.first_sets["Factor_prime"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Factor-prime", parent=parent)

        if (
            token0 in self.first_sets["Factor_prime"]
            or token1 in self.first_sets["Factor_prime"]
        ):
            if token1 == "(":
                self.match_token("(", node)
                self.transition_diagram_args(parent=node)
                if not self.match_token(")", node):
                    self.error(f"missing )")
        elif (
            token0 in self.follow_sets["Factor_prime"]
            or token1 in self.follow_sets["Factor_prime"]
        ):
            if "epsilon" in self.first_sets["Factor_prime"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Factor-prime")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_factor_prime(parent)

    def transition_diagram_factor_zegond(self, parent):
        # for this rule: Factor-zegond -> ( Expression ) | NUM

        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Factor_zegond"]
            and "epsilon" in self.first_sets["Factor_zegond"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Factor-zegond", parent=parent)

        if (
            token0 in self.first_sets["Factor_zegond"]
            or token1 in self.first_sets["Factor_zegond"]
        ):
            if token1 == "(":
                self.match_token("(", node)
                self.transition_diagram_expression(parent=node)
                if not self.match_token(")", node):
                    self.error(f"missing )")
            elif token0 == "NUM":
                _, token, _ = self.scanner.get_current_token()
                self.match_token("NUM", node)
                token = int(token)  # float
                # Action: PID (const)
                self.code_generator.push_const(token)
        elif (
            token0 in self.follow_sets["Factor_zegond"]
            or token1 in self.follow_sets["Factor_zegond"]
        ):
            if "epsilon" in self.first_sets["Factor_zegond"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Factor-zegond")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_factor_zegond(parent)

    def transition_diagram_args(self, parent):
        # for this rule: Args -> Arg-list | epsilon

        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Args"] and "epsilon" in self.first_sets["Args"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Args", parent=parent)

        if token0 in self.first_sets["Args"] or token1 in self.first_sets["Args"]:
            self.transition_diagram_arg_list(parent=node)

            # Action: Output
            if self.handle_output:
                self.code_generator.output()
                self.handle_output = False

        elif token0 in self.follow_sets["Args"] or token1 in self.follow_sets["Args"]:
            if "epsilon" in self.first_sets["Args"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Args")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_args(parent)

    def transition_diagram_arg_list(self, parent):
        # for this rule: Arg-list -> Expression Arg-list-prime

        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Arg_list"]
            and "epsilon" in self.first_sets["Arg_list"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Arg-list", parent=parent)

        if (
            "epsilon" in self.first_sets["Arg_list"]
            or token0 in self.first_sets["Arg_list"]
            or token1 in self.first_sets["Arg_list"]
        ):
            self.transition_diagram_expression(parent=node)
            self.transition_diagram_arg_list_prime(parent=node)
        elif (
            token0 in self.follow_sets["Arg_list"]
            or token1 in self.follow_sets["Arg_list"]
        ):
            if "epsilon" in self.first_sets["Arg_list"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Arg-list")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_arg_list(parent)

    def transition_diagram_arg_list_prime(self, parent):
        # for this rule: Arg-list-prime -> , Expression Arg-list-prime | epsilon

        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Arg_list_prime"]
            and "epsilon" in self.first_sets["Arg_list_prime"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Arg-list-prime", parent=parent)

        if (
            token0 in self.first_sets["Arg_list_prime"]
            or token1 in self.first_sets["Arg_list_prime"]
        ):
            if token1 == ",":
                self.match_token(",", node)
                self.transition_diagram_expression(parent=node)
                self.transition_diagram_arg_list_prime(parent=node)
        elif (
            token0 in self.follow_sets["Arg_list_prime"]
            or token1 in self.follow_sets["Arg_list_prime"]
        ):
            if "epsilon" in self.first_sets["Arg_list_prime"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Arg-list-prime")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_arg_list_prime(parent)

    def transition_diagram_h(self, parent):
        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["H"] and "epsilon" in self.first_sets["H"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("H", parent=parent)

        if (
            "epsilon" in self.first_sets["H"]
            or token0 in self.first_sets["H"]
            or token1 in self.first_sets["H"]
        ):
            if token1 == "=":
                self.match_token("=", node)
                self.transition_diagram_expression(parent=node)
                # Action: assign
                self.code_generator.assign()
            else:
                self.transition_diagram_g(parent=node)
                self.transition_diagram_d(parent=node)
                self.transition_diagram_c(parent=node)
        elif token0 in self.follow_sets["H"] or token1 in self.follow_sets["H"]:
            if "epsilon" in self.first_sets["H"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing H")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_h(parent)

    def transition_diagram_simple_expression_zegond(self, parent):
        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Simple_expression_zegond"]
            and "epsilon" in self.first_sets["Simple_expression_zegond"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Simple-expression-zegond", parent=parent)

        if (
            "epsilon" in self.first_sets["Simple_expression_zegond"]
            or token0 in self.first_sets["Simple_expression_zegond"]
            or token1 in self.first_sets["Simple_expression_zegond"]
        ):
            self.transition_diagram_additive_expression_zegond(parent=node)
            self.transition_diagram_c(parent=node)
        elif (
            token0 in self.follow_sets["Simple_expression_zegond"]
            or token1 in self.follow_sets["Simple_expression_zegond"]
        ):
            if "epsilon" in self.first_sets["Simple_expression_zegond"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing H")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_simple_expression_zegond(parent)

    def transition_diagram_simple_expression_prime(self, parent):
        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Simple_expression_prime"]
            and "epsilon" in self.first_sets["Simple_expression_prime"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Simple-expression-prime", parent=parent)

        if (
            "epsilon" in self.first_sets["Simple_expression_prime"]
            or token0 in self.first_sets["Simple_expression_prime"]
            or token1 in self.first_sets["Simple_expression_prime"]
        ):
            self.transition_diagram_additive_expression_prime(parent=node)
            self.transition_diagram_c(parent=node)
        elif (
            token0 in self.follow_sets["Simple_expression_prime"]
            or token1 in self.follow_sets["Simple_expression_prime"]
        ):
            if "epsilon" in self.first_sets["Simple_expression_prime"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Simple-expression-prime")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_simple_expression_prime(parent)

    def transition_diagram_c(self, parent):
        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["C"] and "epsilon" in self.first_sets["C"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("C", parent=parent)

        if token0 in self.first_sets["C"] or token1 in self.first_sets["C"]:
            is_lt = False
            if token1 == "<":
                is_lt = True

            self.transition_diagram_relop(parent=node)
            self.transition_diagram_additive_expression(parent=node)

            # Action: ReLOP
            if is_lt:
                self.code_generator.less_than()
            else:
                self.code_generator.equals()

        elif token0 in self.follow_sets["C"] or token1 in self.follow_sets["C"]:
            if "epsilon" in self.first_sets["C"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing c")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_c(parent)

    def transition_diagram_relop(self, parent):
        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Relop"] and "epsilon" in self.first_sets["Relop"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Relop", parent=parent)

        if token0 in self.first_sets["Relop"] or token1 in self.first_sets["Relop"]:
            if self.match_token("<", node):
                pass
            elif self.match_token("==", node):
                pass
        elif token0 in self.follow_sets["Relop"] or token1 in self.follow_sets["Relop"]:
            if "epsilon" in self.first_sets["Relop"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Relop")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_relop()

    def transition_diagram_additive_expression(self, parent):
        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Additive_expression"]
            and "epsilon" in self.first_sets["Additive_expression"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Additive-expression", parent=parent)

        if (
            "epsilon" in self.first_sets["Additive_expression"]
            or token0 in self.first_sets["Additive_expression"]
            or token1 in self.first_sets["Additive_expression"]
        ):
            self.transition_diagram_term(parent=node)
            self.transition_diagram_d(parent=node)
        elif (
            token0 in self.follow_sets["Additive_expression"]
            or token1 in self.follow_sets["Additive_expression"]
        ):
            if "epsilon" in self.first_sets["Additive-expression"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Additive-expression")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_additive_expression(parent)

    def transition_diagram_additive_expression_prime(self, parent):
        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Additive_expression_prime"]
            and "epsilon" in self.first_sets["Additive_expression_prime"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Additive-expression-prime", parent=parent)

        if (
            "epsilon" in self.first_sets["Additive_expression_prime"]
            or token0 in self.first_sets["Additive_expression_prime"]
            or token1 in self.first_sets["Additive_expression_prime"]
        ):
            self.transition_diagram_term_prime(parent=node)
            self.transition_diagram_d(parent=node)
        elif (
            token0 in self.follow_sets["Additive_expression_prime"]
            or token1 in self.follow_sets["Additive_expression_prime"]
        ):
            if "epsilon" in self.first_sets["Additive_expression_prime"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Additive-expression-prime")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_additive_expression_prime(parent)

    def transition_diagram_additive_expression_zegond(self, parent):
        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Additive_expression_zegond"]
            and "epsilon" in self.first_sets["Additive_expression_zegond"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Additive-expression-zegond", parent=parent)

        if (
            "epsilon" in self.first_sets["Additive_expression_zegond"]
            or token0 in self.first_sets["Additive_expression_zegond"]
            or token1 in self.first_sets["Additive_expression_zegond"]
        ):
            self.transition_diagram_term_zegond(parent=node)
            self.transition_diagram_d(parent=node)
        elif (
            token0 in self.follow_sets["Additive_expression_zegond"]
            or token1 in self.follow_sets["Additive_expression_zegond"]
        ):
            if "epsilon" in self.first_sets["Additive_expression_zegond"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Additive-expression-zegond")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_additive_expression_zegond(parent)

    def transition_diagram_d(self, parent):
        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["D"] and "epsilon" in self.first_sets["D"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("D", parent=parent)

        if token0 in self.first_sets["D"] or token1 in self.first_sets["D"]:
            if token1 == "+":
                is_plus = True
            else:
                is_plus = False

            self.transition_diagram_addop(parent=node)
            self.transition_diagram_term(parent=node)

            # Action: ADD OR SUB
            if is_plus:
                self.code_generator.add()
            else:
                self.code_generator.sub()

            self.transition_diagram_d(parent=node)
        elif token0 in self.follow_sets["D"] or token1 in self.follow_sets["D"]:
            if "epsilon" in self.first_sets["D"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing D")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_d(parent)

    def transition_diagram_addop(self, parent):
        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Addop"] and "epsilon" in self.first_sets["Addop"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Addop", parent=parent)

        if token0 in self.first_sets["Addop"] or token1 in self.first_sets["Addop"]:
            if self.match_token("+", node):
                pass
            elif self.match_token("-", node):
                pass
        elif token0 in self.follow_sets["Addop"] or token1 in self.follow_sets["Addop"]:
            if "epsilon" in self.first_sets["Addop"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Addop")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_addop(parent)

    def transition_diagram_term(self, parent):
        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Term"] and "epsilon" in self.first_sets["Term"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Term", parent=parent)

        if (
            "epsilon" in self.first_sets["Term"]
            or token0 in self.first_sets["Term"]
            or token1 in self.first_sets["Term"]
        ):
            self.transition_diagram_factor(parent=node)
            self.transition_diagram_g(parent=node)
        elif token0 in self.follow_sets["Term"] or token1 in self.follow_sets["Term"]:
            if "epsilon" in self.first_sets["Term"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Term")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_term(parent)

    def transition_diagram_term_prime(self, parent):
        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Term_prime"]
            and "epsilon" in self.first_sets["Term_prime"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Term-prime", parent=parent)

        if (
            "epsilon" in self.first_sets["Term_prime"]
            or token0 in self.first_sets["Term_prime"]
            or token1 in self.first_sets["Term_prime"]
        ):
            self.transition_diagram_factor_prime(parent=node)
            self.transition_diagram_g(parent=node)
        elif (
            token0 in self.follow_sets["Term_prime"]
            or token1 in self.follow_sets["Term_prime"]
        ):
            if "epsilon" in self.first_sets["Term_prime"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Term-prime")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_term_prime(parent)

    def transition_diagram_term_zegond(self, parent):
        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Term_zegond"]
            and "epsilon" in self.first_sets["Term_zegond"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Term-zegond", parent=parent)

        if (
            "epsilon" in self.first_sets["Term_zegond"]
            or token0 in self.first_sets["Term_zegond"]
            or token1 in self.first_sets["Term_zegond"]
        ):
            self.transition_diagram_factor_zegond(parent=node)
            self.transition_diagram_g(parent=node)
        elif (
            token0 in self.follow_sets["Term_zegond"]
            or token1 in self.follow_sets["Term_zegond"]
        ):
            if "epsilon" in self.first_sets["Term_zegond"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Term-zegond")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_term_zegond(parent)

    def transition_diagram_g(self, parent):
        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["G"] and "epsilon" in self.first_sets["G"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("G", parent=parent)

        if token0 in self.first_sets["G"] or token1 in self.first_sets["G"]:
            if self.match_token("*", node):
                self.transition_diagram_factor(parent=node)

                # Action: MUL
                self.code_generator.mul()

                self.transition_diagram_g(parent=node)
        elif token0 in self.follow_sets["G"] or token1 in self.follow_sets["G"]:
            if "epsilon" in self.first_sets["G"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing G")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_g(parent)

    def transition_diagram_factor(self, parent):
        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Factor"] and "epsilon" in self.first_sets["Factor"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Factor", parent=parent)

        if token0 in self.first_sets["Factor"] or token1 in self.first_sets["Factor"]:
            if self.match_token("(", node):
                self.transition_diagram_expression(parent=node)
                if not self.match_token(")", node):
                    self.error(f"missing )")
            elif self.match_token("ID", node):
                # Action: PID
                self.code_generator.push_id(
                    self.code_generator.get_token_address(token1)
                )
                self.transition_diagram_var_call_prime(parent=node)
            elif self.match_token("NUM", node):
                # Action: PID (const)
                self.code_generator.push_const(token1)
                pass
        elif (
            token0 in self.follow_sets["Factor"] or token1 in self.follow_sets["Factor"]
        ):
            if "epsilon" in self.first_sets["Factor"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Factor")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_factor(parent)

    def transition_diagram_var_call_prime(self, parent):
        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Var_call_prime"]
            and "epsilon" in self.first_sets["Var_call_prime"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Var-call-prime", parent=parent)

        if (
            token1 == ")"
            or token1 == ";"
            or token0 in self.first_sets["Var_call_prime"]
            or token1 in self.first_sets["Var_call_prime"]
        ):
            if self.match_token("(", node):
                self.transition_diagram_args(parent=node)
                if not self.match_token(")", node):
                    self.error(f"missing )")
            else:
                self.transition_diagram_var_prime(parent=node)
        elif (
            token0 in self.follow_sets["Var_call_prime"]
            or token1 in self.follow_sets["Var_call_prime"]
        ):
            if "epsilon" in self.first_sets["Var_call_prime"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Var-call-prime")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_var_call_prime(parent)

    def transition_diagram_var_prime(self, parent):
        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Var_prime"]
            and "epsilon" in self.first_sets["Var_prime"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Var-prime", parent=parent)

        if (
            token0 in self.first_sets["Var_prime"]
            or token1 in self.first_sets["Var_prime"]
        ):
            if self.match_token("[", node):
                self.transition_diagram_expression(parent=node)
                if not self.match_token("]", node):
                    self.error(f"missing ]")

                # Action: array access
                self.code_generator.array_access()
        elif (
            token0 in self.follow_sets["Var_prime"]
            or token1 in self.follow_sets["Var_prime"]
        ):
            if "epsilon" in self.first_sets["Var_prime"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Var-prime")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_var_prime(parent)

    def transition_diagram_expression(self, parent):
        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Expression"]
            and "epsilon" in self.first_sets["Expression"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Expression", parent=parent)

        if (
            "epsilon" in self.first_sets["Expression"]
            or token0 in self.first_sets["Expression"]
            or token1 in self.first_sets["Expression"]
        ):
            if (
                token0 in self.first_sets["Simple_expression_zegond"]
                or token1 in self.first_sets["Simple_expression_zegond"]
            ):
                self.transition_diagram_simple_expression_zegond(node)
            elif token0 == "ID":
                _, token, _ = self.scanner.get_current_token()
                self.match_token("ID", node)

                if token == "output":
                    self.handle_output = True
                else:
                    # Action: PID
                    self.code_generator.push_id(
                        self.code_generator.get_token_address(token)
                    )
                self.transition_diagram_b(node)
        elif (
            token0 in self.follow_sets["Expression"]
            or token1 in self.follow_sets["Expression"]
        ):
            if "epsilon" in self.first_sets["Expression"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Expression")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_expression(parent)

    def transition_diagram_selection_stmt(self, parent):
        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Selection_stmt"]
            and "epsilon" in self.first_sets["Selection_stmt"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Selection-stmt", parent=parent)

        if (
            token0 in self.first_sets["Selection_stmt"]
            or token1 in self.first_sets["Selection_stmt"]
        ):
            if token1 == "if":
                self.match_token("if", node)
                if not self.match_token("(", node):
                    self.error("missing (")
                self.transition_diagram_expression(node)
                if not self.match_token(")", node):
                    self.error("missing )")

                # Action: save_address
                self.code_generator.save_address()
                self.code_generator.program_block.create_entity(None, None)

                self.transition_diagram_statement(node)

                if not self.match_token("else", node):
                    self.error("missing else")

                # Action: jpf_save
                self.code_generator.else_save_address()

                self.transition_diagram_statement(node)

                # Action: jp
                self.code_generator.jp()
        elif (
            token0 in self.follow_sets["Selection_stmt"]
            or token1 in self.follow_sets["Selection_stmt"]
        ):
            if "epsilon" in self.first_sets["Selection_stmt"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Selection-stmt")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_selection_stmt(parent)

    def transition_diagram_iteration_stmt(self, parent):
        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Iteration_stmt"]
            and "epsilon" in self.first_sets["Iteration_stmt"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Iteration-stmt", parent=parent)

        if (
            token0 in self.first_sets["Iteration_stmt"]
            or token1 in self.first_sets["Iteration_stmt"]
        ):
            if token1 == "repeat":
                # Action: save_address
                self.code_generator.save_address()

                self.match_token("repeat", node)
                self.transition_diagram_statement(node)
                if not self.match_token("until", node):
                    self.error("missing until")
                if not self.match_token("(", node):
                    self.error("missing (")
                self.transition_diagram_expression(node)
                if not self.match_token(")", node):
                    self.error("missing )")

                # Action: until
                self.code_generator.until()
        elif (
            token0 in self.follow_sets["Iteration_stmt"]
            or token1 in self.follow_sets["Iteration_stmt"]
        ):
            if "epsilon" in self.first_sets["Iteration_stmt"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Iteration-stmt")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_iteration_stmt(parent)

    def transition_diagram_return_stmt(self, parent):
        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Return_stmt"]
            and "epsilon" in self.first_sets["Return_stmt"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Return-stmt", parent=parent)

        if (
            token0 in self.first_sets["Return_stmt"]
            or token1 in self.first_sets["Return_stmt"]
        ):
            if token1 == "return":
                self.match_token("return", node)
                self.transition_diagram_return_stmt_prime(node)
        elif (
            token0 in self.follow_sets["Return_stmt"]
            or token1 in self.follow_sets["Return_stmt"]
        ):
            if "epsilon" in self.first_sets["Return_stmt"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Return-stmt")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_return_stmt(parent)

    def transition_diagram_return_stmt_prime(self, parent):
        token0, token1, _ = self.scanner.get_current_token()
        if self.grim:
            return
        if token0 == "$" and not (
            "$" in self.follow_sets["Return_stmt_prime"]
            and "epsilon" in self.first_sets["Return_stmt_prime"]
        ):
            if not self.grim:
                self.grim = True
                self.error("Unexpected EOF")
            return

        # add node to tree
        node = Node("Return-stmt-prime", parent=parent)

        if (
            token0 in self.first_sets["Return_stmt_prime"]
            or token1 in self.first_sets["Return_stmt_prime"]
        ):
            if token1 == ";":
                self.match_token(";", node)
            elif (
                token0 in self.first_sets["Expression"]
                or token1 in self.first_sets["Expression"]
            ):
                self.transition_diagram_expression(node)
                if not self.match_token(";", node):
                    self.error("missing ;")
        elif (
            token0 in self.follow_sets["Return_stmt_prime"]
            or token1 in self.follow_sets["Return_stmt_prime"]
        ):
            if "epsilon" in self.first_sets["Return_stmt_prime"]:
                Node("epsilon", node)
                return
            else:
                # remove node from tree
                node.parent = None
                self.error(f"missing Return-stmt-prime")
        else:
            if token0 == "SYMBOL" or token0 == "KEYWORD":
                self.error(f"illegal {token1}")
            else:
                self.error(f"illegal {token0}")
            self.scanner.get_next_token()
            # remove node from tree
            node.parent = None
            self.transition_diagram_return_stmt_prime(parent)
