from typing import Optional


class ProgramBlockEntity:
    instance: Optional[ProgramBlockEntity] = None

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
        self.PB.append(entity)
        self.increase_line_number()
        return entity

    def increase_line_number(self):
        pass


class ProgramBlock:
    instance: Optional[ProgramBlock] = None

    def get_instance():
        if ProgramBlock.instance is None:
            ProgramBlock.instance = ProgramBlock()
        return ProgramBlock.instance

    def __init__(self):
        self.PB_Entity = ProgramBlockEntity.get_instance()
