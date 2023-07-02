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

    def __init__(self):
        self.semantic_stack = Stack.get_instance()
        self.program_block = ProgramBlock.get_instance()
        # For phase 03
        self.program_block.create_entity(OPERATION.ASSIGN, 4, Address(0))
        self.program_block.create_entity(OPERATION.JP, Address(2))
        self.token_to_address = {}

    def run_routine(self, routine_name, params):
        func_to_call = getattr(self, routine_name)
        if func_to_call is not None and callable(func_to_call):
            func_to_call(*params)
        else:
            raise Exception("Routine not found")

    def output(self):
        operand = self.semantic_stack.pop()
        self.program_block.create_entity(OPERATION.PRINT, operand)

    def get_token_address(self, token):
        if token not in self.token_to_address:
            self.token_to_address[token] = self.program_block.get_new_address()
        return self.token_to_address[token]

    def push_id(self, id):
        self.semantic_stack.push(id)

    def assign(self, is_array=False, array_index=None):
        source = self.semantic_stack.pop()
        target = self.semantic_stack.pop()

        if is_array:
            self.program_block.create_entity(
                OPERATION.ASSIGN, source, target + array_index * 4
            )
        else:
            self.program_block.create_entity(OPERATION.ASSIGN, source, target)

    def assign_zero(self, is_array=False, array_size=None):
        target = self.semantic_stack.pop()
        self.program_block.create_entity(OPERATION.ASSIGN, 0, target)
        if is_array:
            for i in range(array_size - 1):
                self.program_block.create_entity(
                    OPERATION.ASSIGN, 0, self.program_block.get_new_address()
                )

    def push_const(self, const):
        self.semantic_stack.push(const)

    def add(self):
        operand2 = self.semantic_stack.pop()
        operand1 = self.semantic_stack.pop()
        sum_address = self.program_block.get_new_temp_address()
        self.semantic_stack.push(sum_address)
        self.program_block.create_entity(OPERATION.ADD, operand1, operand2, sum_address)

    def sub(self):
        operand2 = self.semantic_stack.pop()
        operand1 = self.semantic_stack.pop()
        subtract_address = self.program_block.get_new_temp_address()
        self.semantic_stack.push(subtract_address)
        self.program_block.create_entity(
            OPERATION.SUB, operand1, operand2, subtract_address
        )

    def mul(self):
        operand2 = self.semantic_stack.pop()
        operand1 = self.semantic_stack.pop()
        mul_address = self.program_block.get_new_temp_address()
        self.semantic_stack.push(mul_address)
        self.program_block.create_entity(OPERATION.MUL, operand1, operand2, mul_address)

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

    def less_than(self):
        operand2 = self.semantic_stack.pop()
        operand1 = self.semantic_stack.pop()
        less_than_address = self.program_block.get_new_temp_address()
        self.semantic_stack.push(less_than_address)
        self.program_block.create_entity(
            OPERATION.LT, operand1, operand2, less_than_address
        )

    def equals(self):
        operand2 = self.semantic_stack.pop()
        operand1 = self.semantic_stack.pop()
        equals_address = self.program_block.get_new_temp_address()
        self.semantic_stack.push(equals_address)
        self.program_block.create_entity(
            OPERATION.EQ, operand1, operand2, equals_address
        )

    def array_access(self):
        index = self.semantic_stack.pop()
        array_start_address = self.semantic_stack.pop()
        if isinstance(index, Address):
            index = index.address
        print(f"ARRAY_ACCESS: {array_start_address.address}, {index}")
        self.semantic_stack.push(Address(array_start_address.address + int(index * 4)))
