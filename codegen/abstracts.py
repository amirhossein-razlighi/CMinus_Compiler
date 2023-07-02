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
    JP = 10
    PRINT = 11


class Address:
    def __init__(self, address):
        self.address = address
