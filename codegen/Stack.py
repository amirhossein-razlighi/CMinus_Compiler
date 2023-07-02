from typing import Optional
class Stack:
    instance: Optional[Stack] = None

    def get_instance():
        if Stack.instance is None:
            Stack.instance = Stack()
        return Stack.instance

    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if len(self.items) > 0:
            return self.items.pop()
        else:
            return None

    def peek(self):
        if len(self.items) > 0:
            return self.items[len(self.items) - 1]
        else:
            return None

    def size(self):
        return len(self.items)

    def isEmpty(self):
        return len(self.items) == 0

    def __str__(self):
        return str(self.items)
