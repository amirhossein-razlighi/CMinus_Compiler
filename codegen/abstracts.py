from enum import Enum


class OPERATION(Enum):
    ASSIGN = "ASSIGN"
    JP = "JP"
    ADD = "ADD"
    SUB = "SUB"
    MUL = "MULT"
    PRINT = "PRINT"
    EQ = "EQ"
    LT = "LT"
    JPF = "JPF"


class Address:
    is_indirect = False
    is_immediate = False

    def __init__(self, address):
        self.address = address

    def __str__(self):
        if self.is_indirect:
            return f"@{self.address}"
        elif self.is_immediate:
            return f"#{self.address}"
        return f"{self.address}"

    def __repr__(self):
        if self.is_indirect:
            return f"@{self.address}"
        elif self.is_immediate:
            return f"#{self.address}"
        return f"{self.address}"

    def set_indirect(self):
        self.is_indirect = True
        return self

    def set_immediate(self):
        self.is_immediate = True
        return self

    def set_direct(self):
        self.is_indirect = False
        return self

    def __add__(self, other):
        if isinstance(other, Address):
            return Address(self.address + other.address)
        return Address(self.address + other)
