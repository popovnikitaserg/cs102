import math
import typing as tp


def calc(num_1: float, num_2: float, command: str) -> tp.Union[float, str]:
    if command == "+":
        return num_1 + num_2
    if command == "-":
        return num_1 - num_2
    if command == "/":
        return num_1 / num_2
    if command == "*":
        return num_1 * num_2
    if command == "**":
        return num_1**num_2
    if command == "**2":
        return num_1**2
    if command == "sin":
        return math.sin(num_1)
    if command == "cos":
        return math.cos(num_1)
    if command == "tan":
        return math.tan(num_1)
    if command == "nlog":
        return math.log(num_1)
    if command == "log10":
        return math.log10(num_1)
    return f"Неизвестный оператор: {command!r}."


if __name__ == "__main__":
    while True:
        COMMAND = input("Введите операцию >")
        if COMMAND not in ["+", "-", "/", "*", "**"]:
            if COMMAND not in ["**2", "sin", "cos", "tan", "nlog", "log10"]:
                print("Неизвестный оператор, попробуйте ещё раз")
                continue
            else:
                try:
                    NUM_1 = float(input("Первое число >"))
                    NUM_2 = 0.0
                    print(calc(NUM_1, NUM_2, COMMAND))
                except:
                    print("Введите другое число")
                    continue

        else:
            if COMMAND in ["+", "-", "/", "*", "**"]:
                try:
                    NUM_1 = float(input("Первое число >"))
                    NUM_2 = float(input("Второе число >"))
                    if COMMAND == "/" and NUM_2 == 0:
                        print("На ноль делить нельзя")
                        continue
                    print(calc(NUM_1, NUM_2, COMMAND))
                except:
                    print("Введите другое число")
