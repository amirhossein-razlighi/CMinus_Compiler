from typing import Optional
from .abstracts import Address


class ProgramBlockEntity:
    instance: Optional["ProgramBlockEntity"] = None

    def get_instance():
        if ProgramBlockEntity.instance is None:
            ProgramBlockEntity.instance = ProgramBlockEntity()
        return ProgramBlockEntity.instance

    def __init__(self):
        self.line_number = 0
        self.PB = []

    def create_entity(self, operation, operand1, operand2=None, operand3=None):
        self.operation = operation
        self.operand1 = operand1
        self.operand2 = operand2
        self.operand3 = operand3
        entity = {
            "operation": self.operation,
            "operand1": self.operand1,
            "operand2": self.operand2,
            "operand3": self.operand3,
        }
        if operation == None:
            print("None")
            print(self.line_number)
        self.PB.append(entity)
        self.increase_line_number()
        return entity

    def increase_line_number(self):
        self.line_number += 1

    def get_current_line_number(self):
        return self.line_number


class ProgramBlock:
    instance: Optional["ProgramBlock"] = None

    def get_instance():
        if ProgramBlock.instance is None:
            ProgramBlock.instance = ProgramBlock()
        return ProgramBlock.instance

    def __init__(self):
        self.PB_Entity = ProgramBlockEntity.get_instance()
        self.last_temp_address = Address(500 - 4)
        self.last_address = Address(100 - 4)

    def get_new_temp_address(self):
        self.last_temp_address.address += 4
        return Address(self.last_temp_address.address)

    def get_new_address(self):
        self.last_address.address += 4
        return Address(self.last_address.address)

    def get_current_address(self, get_value=False):
        if get_value:
            return self.last_address.address
        return Address(self.last_address.address)

    def get_current_temp_address(self, get_value=False):
        if get_value:
            return self.last_temp_address.address
        return Address(self.last_temp_address.address)

    def create_entity(self, operation, operand1, operand2=None, operand3=None):
        return self.PB_Entity.create_entity(operation, operand1, operand2, operand3)
