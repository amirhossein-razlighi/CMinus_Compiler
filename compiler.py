# This is a part of C-Minus Compiler and supposed to do the "Parser" job.

import os
import anytree
import json

from . import scanner


def read_grammar_from_file(json_file_path):
    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)
    return (
        data["terminals"],
        data["non-terminals"],
        data["first_sets"],
        data["follow_sets"],
    )
