from scanner import *

def match(token, expected_token):
    if token == expected_token:
        return True
        get_next_token()
    else:
        return False


def transition_diagram_program(token, first_sets, follow_sets):
    # for this rule: Program -> Declaration-list
    if token in first_sets["Declaration_list"]:
        transition_diagram_declaration_list(token, first_sets, follow_sets)
    elif token in follow_sets["Program"]:
        if "Epsilon" in first_sets["Program"]:
            return
        else:
            error(f"Missing Program")
    else:
        error(f"Illegal {token}")
        transition_diagram_program(token, first_sets, follow_sets)


def transition_diagram_declaration_list():
    # for this rule: Declaration-list -> Declaration Declaration-list | Epsilon
    if token in first_sets["Declaration"]:
        transition_diagram_declaration(token, first_sets, follow_sets)
        transition_diagram_declaration_list(token, first_sets, follow_sets)
    elif token in follow_sets["Declaration_list"]:
        if "Epsilon" in first_sets["Declaration_list"]:
            return
        else:
            error(f"Missing Declaration_list")
    else:
        error(f"Illegal {token}")
        transition_diagram_declaration_list(token, first_sets, follow_sets)
