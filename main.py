import json
import math

year = "2025"

class ValueNode:
    def __init__(self, value):
        self.value = value
        self.ops = 0
        self.sqrt_count = 0

    def evaluate(self):
        return self.value

    def __repr__(self):
        return f"{self.value}"


class BinaryNode:
    def __init__(self, func, left, right):
        self.func = func
        self.left = left
        self.right = right
        self.ops = left.ops + right.ops + 1
        self.sqrt_count = left.sqrt_count + right.sqrt_count

    def evaluate(self):
        return self.func(self.left.evaluate(), self.right.evaluate())


class UnaryNode:
    def __init__(self, func, child):
        self.func = func
        self.child = child
        self.ops = child.ops + 1
        self.sqrt_count = child.sqrt_count

    def evaluate(self):
        return self.func(self.child.evaluate())


class AddNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(lambda x, y: x + y, left, right)

    def __repr__(self):
        return f"({self.left} + {self.right})"


class SubtractNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(lambda x, y: x - y, left, right)

    def __repr__(self):
        return f"({self.left} - {self.right})"


class MultiplyNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(lambda x, y: x * y, left, right)

    def __repr__(self):
        return f"({self.left} * {self.right})"


class DivideNode(BinaryNode):
    def __init__(self, left, right):
        super().__init__(lambda x, y: x / y, left, right)

    def __repr__(self):
        return f"({self.left} / {self.right})"


class PowerNode(BinaryNode):
    def __init__(self, left, right):
        def power(x, y):
            if x == 0 and y < 0:
                raise ValueError("0 to the power of negative number")
            if x < 0 and not y.is_integer():
                raise ValueError("Negative number to the power of non-integer")
            if y > 100:
                raise ValueError("Number to the power of number greater than 100")
            return x ** y
        super().__init__(power, left, right)

    def __repr__(self):
        return f"({self.left} ** {self.right})"


class FloorNode(UnaryNode):
    def __init__(self, child):
        super().__init__(math.floor, child)

    def __repr__(self):
        return f"floor({self.child})"


class CeilNode(UnaryNode):
    def __init__(self, child):
        super().__init__(math.ceil, child)

    def __repr__(self):
        return f"ceil({self.child})"


class SqrtNode(UnaryNode):
    def __init__(self, child):
        super().__init__(math.sqrt, child)
        self.sqrt_count = child.sqrt_count + 1

    def __repr__(self):
        return f"sqrt({self.child})"


class AbsNode(UnaryNode):
    def __init__(self, child):
        super().__init__(abs, child)

    def __repr__(self):
        return f"abs({self.child})"


class FactorialNode(UnaryNode):
    def __init__(self, child):
        def fact(x):
            if x < 0:
                raise ValueError("Factorial of negative number")
            if x > 25:
                raise ValueError("Factorial of number greater than 25")
            return math.factorial(x)
        super().__init__(fact, child)

    def __repr__(self):
        return f"factorial({self.child})"


class UnaryMinusNode(UnaryNode):
    def __init__(self, child):
        super().__init__(lambda x: -x, child)

    def __repr__(self):
        return f"(-{self.child})"


binary_ops = [
    AddNode, SubtractNode, MultiplyNode, DivideNode, PowerNode
]

unary_ops = [
    FactorialNode, UnaryMinusNode, AbsNode
]


# dp[start][end] = the set of all possible values formed by the substring of 2025[start:end] inclusive

dp = [[dict() for _ in range(len(year))] for _ in range(len(year))]

for i in range(len(year)):
    dp[i][i][int(year[i])] = ValueNode(int(year[i]))

factorials = [math.factorial(i) for i in range(25)]

for start in range(len(year)):
    for end in range(start+1, len(year)):
        value = "".join([str(i) for i in year[start:end+1]])
        if len(value) != len(str(int(value))):
            continue
        dp[start][end][int(value)] = ValueNode(int(value))

        for decimal_point in range(start, end):
            left = year[start:decimal_point+1]
            right = year[decimal_point+1:end+1]
            value = f"{left}.{right}"
            if int(float(value)) == float(value):
                continue
            if len(value) != len(str(float(value))):
                continue

            dp[start][end][float(value)] = ValueNode(float(value))


def add_value(start, end, node):
    try:
        value = node.evaluate()
    except Exception as _:
        return

    if abs(value) > 10**9:
        return

    if node.sqrt_count > 2:
        return

    if value - int(value) < 1e-6:
        value = int(value)

    if value not in dp[start][end]:
        dp[start][end][value] = node

    elif node.ops < dp[start][end][value].ops:
        dp[start][end][value] = node


def unarise(start, end, depth):
    values = list(dp[start][end].keys())
    for value in values:
        for op in unary_ops:
            add_value(start, end, op(dp[start][end][value]))

    if depth > 0:
        unarise(start, end, depth-1)


for start in range(len(year)):
    for end in range(start, len(year)):
        unarise(start, end, 2)


for length in range(2, len(year)+1):
    for start in range(len(year)+1-length):
        end = start + length - 1
        for mid in range(start, end):
            for left in dp[start][mid]:
                for right in dp[mid+1][end]:
                    for op in binary_ops:
                        add_value(start, end, op(dp[start][mid][left], dp[mid+1][end][right]))

        unarise(start, end, 2)


output = {}
for i in range(1, 101):
    if i in dp[0][len(year)-1]:
        expression = str(dp[0][len(year)-1][i])
        value = float(eval(expression, {"__builtins__": {
            "ceil": math.ceil,
            "floor": math.floor,
            "abs": abs,
            "factorial": math.factorial,
            "sqrt": math.sqrt
        }}))
        if value != i:
            print(f"Bug on {i}")
            print(value)
            exit()
        output[str(i)] = str(dp[0][len(year)-1][i])
    else:
        output[str(i)] = "No expression found"

with open(f"{year}.json", "w") as file:
    json.dump(output, file, indent=4)
