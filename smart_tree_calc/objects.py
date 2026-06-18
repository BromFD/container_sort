class CalcNode:
    def __init__(self, data=None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.data)


class CalcTree:
    def __init__(self, root=None):
        self.root = root

    def is_equal(self, node1, node2):
        #Рекурсивно проверяет, равны ли два поддерева
        if node1 is None and node2 is None:
            return True
        if node1 is None or node2 is None:
            return False
        if node1.data != node2.data:
            return False
        return self.is_equal(node1.left, node2.left) and self.is_equal(node1.right, node2.right)

    def tokenize(self, expression):
        #Разбивает инфиксную строку на токены, учитывая унарные минусы
        expression = expression.replace(" ", "")
        tokens = []
        i = 0
        while i < len(expression):
            char = expression[i]
            if char in {"+", "-", "*", "/", "(", ")"}:
                # Проверка на унарный минус: если '-' идет в начале или после другой операции/скобки
                if char == "-" and (i == 0 or expression[i - 1] in {"+", "-", "*", "/", "("}):
                    tokens.append("~")  # Используем '~' как маркер унарного минуса
                else:
                    tokens.append(char)
                i += 1
            elif char.isalnum():  # Число или переменная (буква)
                token = ""
                while i < len(expression) and expression[i].isalnum():
                    token += expression[i]
                    i += 1
                tokens.append(token)
        return tokens

    def insert_infix(self, expression):
        #Строит дерево из обычной инфиксной записи (Алгоритм Дейкстры)
        tokens = self.tokenize(expression)

        # Перевод инфиксной записи в постфиксную
        output_queue = []
        operator_stack = Stack()

        precedence = {"+": 1, "-": 1, "*": 2, "/": 2, "~": 3}

        for token in tokens:
            if token.isalnum():
                output_queue.append(token)
            elif token in precedence:
                while (operator_stack.top and operator_stack.top.data in precedence and
                       precedence[operator_stack.top.data] >= precedence[token]):
                    output_queue.append(operator_stack.pop().data)
                operator_stack.add(token)
            elif token == "(":
                operator_stack.add(token)
            elif token == ")":
                while operator_stack.top and operator_stack.top.data != "(":
                    output_queue.append(operator_stack.pop().data)
                if operator_stack.top:
                    operator_stack.pop()

        while operator_stack.top:
            output_queue.append(operator_stack.pop().data)

        # Шаг 2: Построение дерева выражений по постфиксной записи
        tree_stack = Stack()
        for token in output_queue:
            if token in precedence:
                if token == "~":
                    child = tree_stack.pop().data if tree_stack.top else None
                    node = CalcNode("-", left=CalcNode("0"), right=child)  # Представляем как 0 - X
                    tree_stack.add(node)
                else:
                    right_node = tree_stack.pop().data if tree_stack.top else None
                    left_node = tree_stack.pop().data if tree_stack.top else None
                    tree_stack.add(CalcNode(token, left=left_node, right=right_node))
            else:
                tree_stack.add(CalcNode(token))

        if tree_stack.top:
            self.root = tree_stack.pop().data

    def simplify(self, root=None):
        #Выносит общий множитель за скобки по заданным правилам
        if root is None:
            root = self.root
            if root is None:
                return

        if root.left:
            self.simplify(root.left)
        if root.right:
            self.simplify(root.right)

        if root.data in {"+", "-"}:
            L = root.left
            R = root.right

            if L and R and L.data == "*" and R.data == "*":
                f1, f2, f3, f4 = L.left, L.right, R.left, R.right

                # Шаблон 1: (f1 * f3) ± (f2 * f3)  ==>  ((f1 ± f2) * f3)
                if self.is_equal(f3, f4):
                    new_op = CalcNode(root.data, left=f1, right=f2)
                    root.data = "*"
                    root.left = new_op
                    root.right = f3

                # Шаблон 2: (f1 * f2) ± (f1 * f3)  ==>  (f1 * (f2 ± f3))
                elif self.is_equal(f1, f4):  # f1 == f4
                    new_op = CalcNode(root.data, left=f2, right=f3)
                    root.data = "*"
                    root.left = f1
                    root.right = new_op

                elif self.is_equal(f1, f3):  # f1 == f3
                    new_op = CalcNode(root.data, left=f2, right=f4)
                    root.data = "*"
                    root.left = f1
                    root.right = new_op

                elif self.is_equal(f2, f4):  # f2 == f4
                    new_op = CalcNode(root.data, left=f1, right=f3)
                    root.data = "*"
                    root.left = f2
                    root.right = new_op

        return root

    def evaluate(self, root=None, variables=None):
        #Cчитает итоговое числовое значение по дереву
        if variables is None:
            variables = {}
        if root is None:
            root = self.root
            if root is None:
                return 0

        # Ищем листы, они могут быть только константами или переменными
        if root.left is None and root.right is None:
            data_str = str(root.data)
            if data_str in variables:
                return float(variables[data_str])
            try:
                return float(data_str)
            except ValueError:
                raise ValueError(f"Ошибка: Не задано значение для переменной '{data_str}'")

        # Рекурсивный обход ветвей
        left_val = self.evaluate(root.left, variables)
        right_val = self.evaluate(root.right, variables)

        if root.data == "+": return left_val + right_val
        if root.data == "-": return left_val - right_val
        if root.data == "*": return left_val * right_val
        if root.data == "/":
            if right_val == 0:
                raise ZeroDivisionError("Ошибка: Деление на ноль!")
            return left_val / right_val
        return 0

    def get_variables(self, root=None, found_vars=None):
        #Вспомогательный метод для поиска всех уникальных букв-переменных в дереве
        if found_vars is None:
            found_vars = set()
        if root is None:
            root = self.root
            if root is None:
                return found_vars

        if root.left is None and root.right is None:
            data_str = str(root.data)
            if data_str.isalpha() and data_str != "0":
                found_vars.add(data_str)

        if root.left: self.get_variables(root.left, found_vars)
        if root.right: self.get_variables(root.right, found_vars)
        return found_vars

    def copy_s(self, root):
        if root is None:
            return None
        return CalcNode(root.data, self.copy_s(root.left), self.copy_s(root.right))

    def copy(self):
        copy = CalcTree()
        copy.root = self.copy_s(self.root)
        return copy

    def to_string(self, root=None, is_main_call=True):
        if is_main_call and root is None:
            root = self.root
        if root is None:
            return ""
        if root.left is None and root.right is None:
            return str(root.data)

        left_str = self.to_string(root.left, is_main_call=False)
        right_str = self.to_string(root.right, is_main_call=False)

        # Вывод унарного минуса (В виде 0 - X)
        if left_str == "0" and root.data == "-":
            return f"(-{right_str})"

        return f"({left_str} {root.data} {right_str})"


class StackNode:
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next


class Stack:
    def __init__(self, top=None):
        self.top = top

    def add(self, data):
        new_node = StackNode(data)
        if self.top is None:
            self.top = new_node
        else:
            new_node.next = self.top
            self.top = new_node

    def pop(self):
        if self.top is None:
            return None
        popped = self.top
        self.top = self.top.next
        return popped


