from typing import Optional


class Stack:

    @staticmethod
    def get_instance():
        return Stack()

    def __init__(self, debug=False):
        self.items = []
        self.dbg=debug
        self.cnt =0

    def push(self, item):
        if self.dbg:
            self.cnt += 1
            print(f"{self.cnt}\tpush {item}")
        self.items.append(item)

    def pop(self):
        if len(self.items) > 0:
            val = self.items.pop()
            if self.dbg:
                self.cnt +=1
                print(f"{self.cnt}\tpop {val}")
            return val
        else:
            if self.dbg:
                self.cnt+=1
                print(f"{self.cnt}\tpop None")
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
