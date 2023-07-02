from .code_gen import CodeGenerator


class Routine:
    def __init__(self, name_of_function, responsible, **params):
        self.status = "STARTED"
        self.name_of_function = name_of_function
        self.params = params
        self.responsible = responsible

    def __str__(self):
        return (
            "Routine: "
            + self.name_of_function
            + " "
            + str(self.params)
            + " "
            + self.status
        )

    def run_routine(self, code_gen: CodeGenerator):
        code_gen.run_routine(self.name_of_function, self.params)
        self.status = "FINISHED"
