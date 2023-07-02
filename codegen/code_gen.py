from typing import Optional

class Routines:
    instance: Optional[Routines] = None

    def get_instance():
        if Routines.instance is None:
            Routines.instance = Routines()
        return Routines.instance

    def __init__(self, semantic_stack):
        self.semantic_stack = semantic_stack
