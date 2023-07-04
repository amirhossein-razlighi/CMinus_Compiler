from typing import Optional
from .pb import ProgramBlock
from .stack import Stack
from .abstracts import Address, OPERATION
from .activations import Activations
from .activation_record import ActivationRecord


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
        # for phase 3
        self.program_block.create_entity(OPERATION.ASSIGN, 4, Address(0))
        self.save_address()
        self.program_block.create_entity(OPERATION.JP, None)

        self.token_to_address = {}
        self.loop_stack = []
        self.activations: Activations = Activations.get_instance()
        self.func_address = Address(0 - 300)

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
        if target == "=":
            target = self.semantic_stack.pop()

        if is_array:
            self.program_block.create_entity(
                OPERATION.ASSIGN, source, target + array_index * 4
            )
        else:
            self.program_block.create_entity(OPERATION.ASSIGN, source, target)

        # push the result of assign, back in the stack
        self.semantic_stack.push("=")
        self.semantic_stack.push(target)

    def assign_zero(self, is_array=False, array_size=None, record=None):
        target = self.semantic_stack.pop()
        self.program_block.create_entity(OPERATION.ASSIGN, 0, target)
        if is_array:
            for i in range(array_size - 1):
                self.program_block.create_entity(
                    OPERATION.ASSIGN, 0, Address(target + (i + 1) * 4)
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
        self.semantic_stack.push(self.program_block.PB_Entity.get_current_line_number())
        self.program_block.create_entity(None, None)

    def jpf_save_address(self):
        a = self.semantic_stack.pop()
        while a != "vars":
            a = self.semantic_stack.pop()
        a = self.semantic_stack.pop()

        self.program_block.PB_Entity.PB[a] = {
            "operation": OPERATION.JPF,
            "operand1": self.semantic_stack.pop(),
            "operand2": self.program_block.PB_Entity.get_current_line_number() + 1,
            "operand3": None,
        }
        self.semantic_stack.push(self.program_block.PB_Entity.get_current_line_number())
        self.program_block.create_entity(None, None)

    def jp(self):
        a = self.semantic_stack.pop()

        while a != "vars":
            a = self.semantic_stack.pop()
        a = self.semantic_stack.pop()

        self.program_block.PB_Entity.PB[a] = {
            "operation": OPERATION.JP,
            "operand1": self.program_block.PB_Entity.get_current_line_number(),
            "operand2": None,
            "operand3": None,
        }

    def main_jp(self):
        a = self.semantic_stack.pop()
        if self.program_block.PB_Entity.PB[2]["operand1"] is None:
            self.program_block.PB_Entity.PB[2] = {
                "operation": OPERATION.JP,
                "operand1": self.program_block.PB_Entity.get_current_line_number(),
                "operand2": None,
                "operand3": None,
            }

    def jpf(self):
        self.program_block.PB_Entity.PB[self.semantic_stack.pop()] = {
            "operation": OPERATION.JPF,
            "operand1": self.semantic_stack.pop(),
            "operand2": self.program_block.PB_Entity.get_current_line_number(),
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
        is_main = self.activations.get_current_activation().name == "main"

        if isinstance(index, Address):
            tmp_1 = self.program_block.get_new_temp_address()
            self.program_block.create_entity(OPERATION.MUL, index, 4, tmp_1)
            if is_main:
                self.program_block.create_entity(
                    OPERATION.ADD, "#" + str(array_start_address.address), tmp_1, tmp_1
                )
                self.semantic_stack.push(Address(tmp_1).set_indirect())
            else:
                self.program_block.create_entity(
                    OPERATION.ADD,
                    Address(array_start_address.address).set_direct(),
                    tmp_1,
                    tmp_1,
                )
                self.semantic_stack.push(Address(tmp_1).set_indirect())

        else:
            self.semantic_stack.push(
                Address(array_start_address.address + int(index * 4))
            )

    def until(self):
        condition = self.semantic_stack.pop()
        where_to_go = self.semantic_stack.pop()

        while where_to_go == "vars" or where_to_go == "args" or where_to_go == "params":
            where_to_go = self.semantic_stack.pop()

        self.program_block.create_entity(
            OPERATION.JPF,
            condition,
            where_to_go,
        )

        # handling break statements
        for line in self.loop_stack:
            self.program_block.PB_Entity.PB[line] = {
                "operation": OPERATION.JP,
                "operand1": self.program_block.PB_Entity.get_current_line_number(),
                "operand2": None,
                "operand3": None,
            }

    def break_the_jail(self):
        self.loop_stack.append(
            self.program_block.PB_Entity.get_current_line_number() + 1
        )
        self.program_block.create_entity(None, None)

    def get_new_function_address(self):
        self.func_address += 400
        return self.func_address

    def call(self, function_to_call, caller_func):
        if function_to_call == None:
            return

        record = self.activations.get_activation(function_to_call)

        record.caller = self.activations.get_activation(caller_func)

        i = 0
        lst = list(record.parameters.values())
        while (item := self.semantic_stack.pop()) != "args":
            param = lst[i]

            if isinstance(item, Address):
                self.program_block.create_entity(
                    OPERATION.ASSIGN,
                    Address(item.address).set_immediate(),
                    Address(param.address).set_direct(),
                )
            else:
                self.program_block.create_entity(
                    OPERATION.ASSIGN,
                    item,
                    Address(param.address).set_indirect(),
                )
            i += 1

        self.program_block.create_entity(OPERATION.JP, record.start_line, None)
        self.program_block.create_entity(None, None)

        self.program_block.PB_Entity.PB[record.last_line] = {
            "operation": OPERATION.JP,
            "operand1": self.program_block.PB_Entity.get_current_line_number() - 1,
            "operand2": None,
            "operand3": None,
        }

        self.semantic_stack.push(record.return_address)
        if record.return_address is None:
            record.return_address = record.get_new_address()

    def return_to_caller(self, record):
        self.program_block.create_entity(OPERATION.JP, None)
        record.last_line = self.program_block.PB_Entity.get_current_line_number() - 1

    @staticmethod
    def debug(self, name_of_caller):
        print(name_of_caller)
        print("Semantic Stack:")
        print(self.semantic_stack.items)
        print("Program Block:")
        for item in self.program_block.PB_Entity.PB:
            print(item)
