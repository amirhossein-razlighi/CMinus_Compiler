from typing import Optional
from .pb import ProgramBlock
from .stack import Stack
from .abstracts import Address, OPERATION


class CodeGenerator:
    instance: Optional["CodeGenerator"] = None

    @staticmethod
    def get_instance():
        if CodeGenerator.instance is None:
            CodeGenerator.instance = CodeGenerator()
        return CodeGenerator.instance

    def __init__(self, semantic_stack: Stack, program_block: ProgramBlock):
        self.semantic_stack = semantic_stack
        self.program_block = program_block
        # For phase 03
        self.program_block.create_entity(OPERATION.ASSIGN, 4, Address(0))
        self.program_block.create_entity(OPERATION.JP, Address(2))

    def push_id(self, id):
        self.semantic_stack.push(id)

    def assign(self):
        source = self.semantic_stack.pop()
        target = self.semantic_stack.pop()
        self.program_block.create_entity(OPERATION.ASSIGN, source, target)

    def assign_zero(self):
        target = self.semantic_stack.pop()
        self.program_block.create_entity(OPERATION.ASSIGN, 0, target)

    def push_const(self, const):
        self.semantic_stack.push(const)

    def add(self):
        operand2 = self.semantic_stack.pop()
        operand1 = self.semantic_stack.pop()
        sum_ = operand1 + operand2
        self.semantic_stack.push(sum_)
        self.program_block.create_entity(
            OPERATION.ADD, operand1, operand2, self.program_block.get_new_temp_address()
        )

    def sub(self):
        operand2 = self.semantic_stack.pop()
        operand1 = self.semantic_stack.pop()
        subtract_ = operand1 - operand2
        self.semantic_stack.push(subtract_)
        self.program_block.create_entity(
            OPERATION.SUB, operand1, operand2, self.program_block.get_new_temp_address()
        )

    def mul(self):
        operand2 = self.semantic_stack.pop()
        operand1 = self.semantic_stack.pop()
        mul_ = operand1 * operand2
        self.semantic_stack.push(mul_)
        self.program_block.create_entity(
            OPERATION.MUL, operand1, operand2, self.program_block.get_new_temp_address()
        )

    def save_address(self):
        self.semantic_stack.push(self.program_block.get_current_address())
        self.program_block.increase_line_number()

    def jpf_save_address(self):
        self.program_block.PB_Entity.PB[self.semantic_stack.pop()] = {
            "operation": OPERATION.JPF,
            "operand1": self.semantic_stack.pop(),
            "operand2": self.program_block.get_current_address() + 1,
            "operand3": None,
        }
        self.semantic_stack.push(self.program_block.get_current_address())
        self.program_block.increase_line_number()

    def jp(self):
        self.program_block.PB_Entity.PB[self.semantic_stack.pop()] = {
            "operation": OPERATION.JP,
            "operand1": self.program_block.get_current_address(),
            "operand2": None,
            "operand3": None,
        }

    def jpf(self):
        self.program_block.PB_Entity.PB[self.semantic_stack.pop()] = {
            "operation": OPERATION.JPF,
            "operand1": self.semantic_stack.pop(),
            "operand2": self.program_block.get_current_address(),
            "operand3": None,
        }
