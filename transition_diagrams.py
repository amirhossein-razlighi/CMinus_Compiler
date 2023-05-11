from scanner import Scanner


class Parser:

    def __init__(scanner):
        self.scanner = scanner
        self.first_sets = {} # read this from json
        self.follow_sets = {} # read this from json

    def match(expected_token):
        if self.scanner.get_current_token()[0] == expected_token:
            Scanner.get_next_token()
            return True
        else:
            return False


    def transition_diagram_program():
        # for this rule: Program -> Declaration-list    
        if token in self.first_sets["Declaration_list"]:
            transition_diagram_declaration_list()
        elif token in self.follow_sets["Program"]:
            if "Epsilon" in self.first_sets["Program"]:
                return
            else:
                error(f"Missing Program")
        else:
            error(f"Illegal {self.scanner.get_current_token()[0]}")
            transition_diagram_program()


    def transition_diagram_declaration_list():
        # for this rule: Declaration-list -> Declaration Declaration-list | Epsilon
        if token in self.first_sets["Declaration"]:
            transition_diagram_declaration()
            transition_diagram_declaration_list()
        elif token in self.follow_sets["Declaration_list"]:
            if "Epsilon" in self.first_sets["Declaration_list"]:
                return
            else:
                error(f"Missing Declaration_list")
        else:
            error(f"Illegal {self.scanner.get_current_token()[0]}")
            transition_diagram_declaration_list()
