from abstracts import Address


class ActivationRecord:
    def __init__(self, name, start_address: Address, caller: ActivationRecord):
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

    def add_parameter(self, name, rel_address: Address):
        if name not in self.parameters:
            self.parameters[name] = self.start_address + rel_address
        return self.parameters[name]

    def add_variable(self, name, rel_address: Address):
        if name not in self.variables:
            self.variables[name] = self.start_address + rel_address
        return self.variables[name]

    def add_temp_variable(self, name, rel_address: Address):
        if name not in self.temp_variables:
            self.temp_variables[name] = self.start_address + rel_address
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

    def __str__(self):
        return f"AR: {self.name} | start_address: {self.start_address} | caller: {self.caller} | variables: {self.variables} | parameters: {self.parameters} | temp_variables: {self.temp_variables} | return_value: {self.return_value} | return_address: {self.return_address} | return_type: {self.return_type} | return_value_address: {self.return_value_address}"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.__str__())

    def __eq__(self, other):
        return self.__str__() == other.__str__()
