# This is a part of C-Minus Compiler and supposed to do the "Parser" job.
# AmirHossein Naghi Razlighi 99102423 | Hirad Davari 99106136

import os
import anytree
import json

from scanner import Scanner
from transition_diagrams.transition_diagrams import Parser
from codegen.abstracts import Address, OPERATION


def read_grammar_from_file(json_file_path):
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)
    return (
        data["terminals"],
        data["non_terminals"],
        data["first_sets"],
        data["follow_sets"],
    )


def save_parse_tree_to_file(file_address, parse_tree):
    with open(file_address, "w") as f:
        for pre, fill, node in anytree.RenderTree(parse_tree):
            f.write("{}{}\n".format(pre, node.name))


def save_errors_to_file(file_address, errors):
    with open(file_address, "w") as f:
        if len(errors) == 0:
            f.write("There is no syntax error.")
            return True
        else:
            for error in errors:
                # Convert error to lowercase
                error_msg = error[1]
                # error_msg = error[1].split(" ")
                # error_msg = error_msg[0].lower() + " " + error_msg[1]
                error_str = "#" + str(error[0]) + " : syntax error, " + error_msg
                f.write("{}\n".format(error_str))
            return False


def save_semantic_errors_to_file(file_address, errors):
    with open(file_address, "w") as f:
        if len(errors) == 0:
            f.write("The input program is semantically correct.\n")
            return True
        else:
            for error in errors:
                f.write(f"{error}\n")
            return False


def convert_address(inp):
    if isinstance(inp, Address):
        return str(inp)

    elif not str(inp).startswith("@"):
        if not str(inp).startswith("#"):
            return "#" + str(inp)
    return inp


def save_code_gen_result(file_address: str, parser: Parser):
    with open(file_address, "w") as f:
        i = 0
        for item in parser.code_generator.program_block.PB_Entity.PB:
            operation, operand1, operand2, operand3 = item.values()
            if operation == None:
                operation = OPERATION.ASSIGN
                operand1 = 0
                operand2 = 0
            print(i, end="\t", file=f)
            print("(", end="", file=f)
            if operation == None:
                print(operation, ",", end=" ", file=f)
            else:
                print(operation.value, ",", end=" ", file=f)
                if operation.value != "JP":
                    operand1 = convert_address(operand1)

            print(operand1, ",", end=" ", file=f)
            if operand2 != None:
                operand2 = convert_address(operand2)
                print(operand2, ",", end=" ", file=f)
            else:
                print(",", end=" ", file=f)
            if operand3 != None:
                operand3 = convert_address(operand3)
                print(operand3, end=")", file=f)
            else:
                print(")", end="", file=f)
            print("", file=f)
            i += 1


if __name__ == "__main__":
    # Read the grammar from the file
    (
        terminals,
        non_terminals,
        first_sets,
        follow_sets,
    ) = read_grammar_from_file("./data.json")

    # Create the scanner
    scanner = Scanner("./input.txt")
    if scanner == None:
        print("Error opening input.txt")
        exit(1)

    # Create the parser
    parser = Parser(
        scanner,
        terminals,
        non_terminals,
        first_sets,
        follow_sets,
    )

    # Parse the input
    parser.parse()

    # Print the parse tree
    # for pre, fill, node in anytree.RenderTree(parser.tree):
    #     print("{}{}".format(pre, node.name))
    # print(parser.errors)

    # Save the parse tree to file
    save_parse_tree_to_file("./parse_tree.txt", parser.tree)

    generate = True

    # Save the errors to file
    generate = generate and save_errors_to_file("./syntax_errors.txt", parser.errors)

    # check if there are semantic errors
    sem = save_semantic_errors_to_file("./semantic_errors.txt", 
                                                         parser.semantic_analyzer.errors)

    generate = generate and sem

    # only generate code when there are no errors
    if generate:
        # Save the code generation result to file
        save_code_gen_result("./output.txt", parser)
    else:
        with open("./output.txt", "w") as f:
            f.write("The output code has not been generated.")
