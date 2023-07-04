from typing import Optional
from .abstracts import Address
from .activation_record import ActivationRecord as AR


class Activations:
    instance: Optional["Activations"] = None

    def get_instance():
        if Activations.instance is None:
            Activations.instance = Activations()
        return Activations.instance

    def __init__(self):
        self.start_address_of_funcs = {}
        self.start_address_of_main = None
        self.activations_stack = [AR("global", Address(0 - 99))]

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

    def push_activation(self, activ_record: AR):
        self.activations_stack.append(activ_record)

    def pop_activation(self):
        return self.activations_stack.pop()

    def get_current_activation(self):
        return self.activations_stack[-1]

    def get_activation(self, name) -> AR:
        for activation in self.activations_stack[::-1]:
            if activation.name == name:
                return activation
        return None

    def get_var_address(self, token, func_name):
        ar = self.get_activation(func_name)
        if ar is None:
            raise Exception("Activation record not found")
        if token not in ar.vars:
            if token not in ar.params:
                raise Exception("Variable not found")
            else:
                return ar.params[token]
        else:
            return ar.vars[token]

    def set_new_var(self, token, func_name):
        ar = self.get_activation(func_name)
        if ar is None:
            raise Exception("Activation record not found")
        if token not in ar.vars:
            ar.vars[token] = ar.get_new_address()

    def set_new_param(self, token, func_name):
        ar = self.get_activation(func_name)
        if ar is None:
            raise Exception("Activation record not found")
        if token not in ar.params:
            ar.params[token] = ar.get_new_address()

    def get_new_temp(self, func_name):
        ar = self.get_activation(func_name)
        if ar is None:
            raise Exception("Activation record not found")
        return ar.get_new_temp_address()
