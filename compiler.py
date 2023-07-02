# This is a part of C-Minus Compiler and supposed to do the "Parser" job.
# AmirHossein Naghi Razlighi 99102423 | Hirad Davari 99106136

import os
import anytree
import json

from scanner import Scanner
from transition_diagrams.transition_diagrams import Parser


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
        else:
            for error in errors:
                # Convert error to lowercase
                error_msg = error[1]
                # error_msg = error[1].split(" ")
                # error_msg = error_msg[0].lower() + " " + error_msg[1]
                error_str = "#" + str(error[0]) + " : syntax error, " + error_msg
                f.write("{}\n".format(error_str))


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

    # Save the errors to file
    save_errors_to_file("./syntax_errors.txt", parser.errors)
