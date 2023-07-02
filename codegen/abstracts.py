from enum import Enum


class OPERATION(Enum):
    ASSIGN = 1
    JP = 2
    ADD = 3
    SUB = 4
    MUL = 5
    PRINT = 6
    EQ = 7
    LT = 8
    JPF = 9


class Address:
    is_indirect = False

    def __init__(self, address):
        self.address = address

    def __str__(self):
        if self.is_indirect:
            return f"@{self.address}"
        return f"{self.address}"

    def __repr__(self):
        if self.is_indirect:
            return f"@{self.address}"
        return f"{self.address}"

    def set_indirect(self):
        self.is_indirect = True
        return self
