# This is a part of C-Minus Compiler and supposed to do the "Parser" job.

import os
import anytree
import json

from scanner import Scanner
from transition_diagrams import Parser


def read_grammar_from_file(json_file_path):
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)
    return (
        data["terminals"],
        data["non_terminals"],
        data["first_sets"],
        data["follow_sets"],
    )



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
    for pre, fill, node in anytree.RenderTree(parser.tree):
        print("{}{}".format(pre, node.name))
    print(parser.errors)

