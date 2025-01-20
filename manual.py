import json
from math import *


filename = "my_2025.json"


def arcsin(x):
    return degrees(asin(x))

def arccos(x):
    return degrees(acos(x))

def arctan(x):
    return degrees(atan(x))


def sine(x):
    return sin(radians(x))


def cosine(x):
    return cos(radians(x))


def tangent(x):
    return tan(radians(x))


def sort_dict_by_value(data: dict) -> dict:
    return dict(sorted(data.items(), key=lambda x: int(x[0])))


def drop_to_file(value, expression):
    value = int(value)
    with open(filename, "r") as file:
        data = json.load(file)
    data[value] = expression
    with open(filename , "w") as file:
        json.dump(sort_dict_by_value(data), file, indent=4)


def check_value(value):
    if not value == int(value):
        return 1

    value = int(value)

    if not 1 <= value <= 100:
        return 1

    with open(filename, "r") as file:
        data = json.load(file)
        if str(value) in data:
            return 2

    return 0


def verify_file():
    with open(filename, "r") as file:
        data = json.load(file)

    for i in range(1, 101):
        if not str(i) in data:
            print(f"{i} not found")

        expression = data[str(i)]
        try:
            value = float(eval(expression))
            if not value == i:
                print(f"Invalid expression for {i}")
                print(value)
        except Exception as _:
            print(f"Invalid expression for {i}")
            continue

        filtered_expr = "".join([i for i in list(expression) if i.isdigit()])
        print(filtered_expr)
        if filtered_expr != "2025":
            print(f"Invalid expression for {i}")


if __name__ == "__main__":
    verify_file()
    while True:
        expression = input(f"Enter expression: ")
        try:
            value = float(eval(expression))
        except Exception as _:
            print("Invalid expression")
            continue
        print(value)
        match check_value(value):
            case 1:
                print(f"Invalid value {value}")
            case 2:
                print(f"Value {value} already exists.")
            case 0:
                drop_to_file(value, expression)
                print(f"Expression saved for {value}")