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
    if(match_token("SYMBOL")):
        if token[1] == '<':
            pass
        if token[1] == '==':
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
    if(match_token("SYMBOL")):
        if token[1] == '+':
            pass
        if token[1] == '-':
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
    if token[1] == '*':
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
    if token[1] == '(':
        match_token("SYMBOL")
        transition_diagram_expression()
        if(self.scanner.get_current_token()[1] == ')'):
            match_token("SYMBOL")
    elif token[0] == 'ID':
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
    if token[1] == '(':
        match_token("SYMBOL")
        transition_diagram_args()
        if(self.scanner.get_current_token()[1] == ')'):
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
    if token[1] == '[':
        match_token("SYMBOL")
        transition_diagram_expression()
        if(self.scanner.get_current_token()[1] == ']'):
            match_token("SYMBOL")
    elif token in self.follow_sets["Var_prime"]:
        if "Epsilon" in self.first_sets["Var_prime"]:
            return
        else:
            error(f"Missing Var_prime")
    else:
        error(f"Illegal {token[0]}")
        transition_diagram_var_prime()


