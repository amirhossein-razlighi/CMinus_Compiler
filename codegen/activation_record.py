from .abstracts import Address


class ActivationRecord:
    def __init__(self, name, start_address: Address, caller=None):
        self.name = name
        self.start_address = start_address
        self.caller = caller
        self.variables = {}
        self.parameters = {}
        self.temp_variables = {}
        self.return_value = None
        self.return_address = None
        self.return_type = None
        self.return_value_address = None
        self.last_var_address = Address(100 - 4)
        self.last_temp_address = Address(500 - 4)

    def add_parameter(self, name, address: Address = None):
        if name not in self.parameters:
            if address is None:
                address = self.get_new_address().set_indirect()
            self.parameters[name] = address
        return self.parameters[name]

    def add_variable(self, name, address: Address = None):
        if name not in self.variables:
            if address is None:
                address = self.get_new_address()
            self.variables[name] = address
        return self.variables[name]

    def add_temp_variable(self, name, address: Address = None):
        if name not in self.temp_variables:
            if address is None:
                address = self.get_new_temp_address()
            self.temp_variables[name] = address
        return self.temp_variables[name]

    def get_variable_address(self, name):
        if name in self.variables:
            return self.variables[name]
        elif self.caller is not None:
            return self.caller.get_variable_address(name)
        else:
            return None

    def get_temp_variable_address(self, name):
        if name in self.temp_variables:
            return self.temp_variables[name]
        elif self.caller is not None:
            return self.caller.get_temp_variable_address(name)
        else:
            return None

    def get_parameter_address(self, name):
        if name in self.parameters:
            return self.parameters[name]
        elif self.caller is not None:
            return self.caller.get_parameter_address(name)
        else:
            return None

    def get_new_address(self, array_size=None):
        self.last_var_address.address += 4
        result = Address(self.start_address.address + self.last_var_address.address)

        if array_size is not None:
            self.last_var_address += (array_size - 1) * 4

        return result

    def get_new_temp_address(self):
        self.last_temp_address.address += 4
        return self.start_address + self.last_temp_address.address

    def __str__(self):
        return f"AR: {self.name} | start_address: {self.start_address} | caller: {self.caller} | variables: {self.variables} | parameters: {self.parameters} | temp_variables: {self.temp_variables} | return_value: {self.return_value} | return_address: {self.return_address} | return_type: {self.return_type} | return_value_address: {self.return_value_address}"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.__str__())

    def __eq__(self, other):
        return self.__str__() == other.__str__()
