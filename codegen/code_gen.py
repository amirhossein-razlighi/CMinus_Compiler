from typing import Optional
from Stack import Stack
from PB import ProgramBlock


class Routines:
    instance: Optional[Routines] = None

    def get_instance():
        if Routines.instance is None:
            Routines.instance = Routines()
        return Routines.instance

    def __init__(self, semantic_stack: Stack, program_block: ProgramBlock):
        self.semantic_stack = semantic_stack
        self.program_block = program_block

    def push_id(self, id):
        self.semantic_stack.push(id)

    def assign(self):
        source = self.semantic_stack.pop()
        target = self.semantic_stack.pop()
