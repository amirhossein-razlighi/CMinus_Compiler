from typing import Optional
from abstracts import Address


class Activations:
    instance: Optional["Activations"] = None

    def get_instance():
        if Activations.instance is None:
            Activations.instance = Activations()
        return Activations.instance

    def __init__(self):
        self.start_address_of_funcs = {}
        self.start_address_of_main = None

    def add_func(self, name, start_address: Address):
        self.start_address_of_funcs[name] = start_address

    def get_func_address(self, name):
        if name in self.start_address_of_funcs:
            return self.start_address_of_funcs[name]
        else:
            raise Exception("Function not found")

    def set_main_address(self, start_address: Address):
        self.start_address_of_main = start_address

    def get_main_address(self):
        return self.start_address_of_main
