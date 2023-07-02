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
        self.program_block.create_entity("assign", source, target)

    def push_const(self, const):
        self.semantic_stack.push(const)

    def add(self):
        operand2 = self.semantic_stack.pop()
        operand1 = self.semantic_stack.pop()
        self.semantic_stack.push(operand1 + operand2)
        self.program_block.create_entity("add", operand1, operand2)

    def sub(self):
        operand2 = self.semantic_stack.pop()
        operand1 = self.semantic_stack.pop()
        self.semantic_stack.push(operand1 - operand2)
        self.program_block.create_entity("sub", operand1, operand2)

    def mul(self):
        operand2 = self.semantic_stack.pop()
        operand1 = self.semantic_stack.pop()
        self.semantic_stack.push(operand1 * operand2)
        self.program_block.create_entity("mul", operand1, operand2)

    def save_address(self):
        self.semantic_stack.push(self.program_block.get_current_address())
        self.program_block.increase_line_number()

    def jpf_save_address(self):
        self.program_block.PB_Entity.PB[self.semantic_stack.pop()] = {
            "operation": "jpf",
            "operand1": self.semantic_stack.pop(),
            "operand2": self.program_block.get_current_address() + 1,
            "operand3": None,
        }
        self.semantic_stack.push(self.program_block.get_current_address())
        self.program_block.increase_line_number()

    def jp(self):
        self.program_block.PB_Entity.PB[self.semantic_stack.pop()] = {
            "operation": "jp",
            "operand1": self.program_block.get_current_address(),
            "operand2": None,
            "operand3": None,
        }

    def jpf(self):
        self.program_block.PB_Entity.PB[self.semantic_stack.pop()] = {
            "operation": "jpf",
            "operand1": self.semantic_stack.pop(),
            "operand2": self.program_block.get_current_address(),
            "operand3": None,
        }
