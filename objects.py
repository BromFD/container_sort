import os

class StackNode:
    def __init__(self, value = None, nxt = None):
        self.value = value
        self.nxt = nxt

    def __str__(self):
        return str(self.value)

class StackOfContainers:
    noisy_mode = False

    def __init__(self):
        self.top = None
        self.stack_id = None

    def __iter__(self):
        current = self.top
        while current:
            yield current
            current = current.nxt

    def __reversed__(self):
        inversed = StackOfContainers()
        for node in self:
            inversed.put(node.value)
        return iter(inversed)

    def __str__(self):
        output_list = []
        for node in self:
            output_list.append(str(node.value))
        return " ".join(output_list)

    def __add__(self, other):
        if isinstance(other, StackOfContainers):
            conjoined = StackOfContainers()
            for node in reversed(self):
                conjoined.put(node.value)
            for node in reversed(other):
                conjoined.put(node.value)
                if StackOfContainers.noisy_mode:
                    with open(file_path, "a") as file:
                        file.write(f"| {other.stack_id} | --> | {self.stack_id} |\n")
            return conjoined
        return NotImplemented

    def __iadd__(self, other):
        if isinstance(other, StackOfContainers):
            for node in reversed(other):
                self.put(node.value)
                if StackOfContainers.noisy_mode:
                    with open(file_path, "a") as file:
                        file.write(f"| {other.stack_id} | --> | {self.stack_id} |\n")
            return self
        return NotImplemented

    def put(self, value):
        new_node = StackNode(value)
        new_node.nxt = self.top
        self.top = new_node

    def pop(self):
        if not self.top:
            return None
        popped = self.top
        self.top = popped.nxt
        return popped

    def move(self, other):
        if isinstance(other, StackOfContainers):
            popped = self.pop()
            other.put(popped.value)
            if StackOfContainers.noisy_mode:
                with open(file_path, "a") as file:
                    file.write(f"| {self.stack_id} | --> | {other.stack_id} |\n")


    def add_list(self, some_list):
        for el in some_list:
            self.put(el)


class Noisy:
    def __enter__(self):
        StackOfContainers.noisy_mode = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        StackOfContainers.noisy_mode = False
        return False


current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "output.txt")