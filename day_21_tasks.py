# https://adventofcode.com/2022/day/21

import re
import math

REG_EXP = "(\w{4}) (\*|\+|\/|\-) (\w{4})"


class FileReader:
    def __init__(self):
        pass

    def gen_file_reader(self, file_name):
        try:
            file = open(file_name, "r")
            for row in file:
                yield row
        finally:
            file.close()


def message_decoder(expression, message_dct):
    return eval(expression, {}, message_dct)


def message_decription(message_dct, root_monkey_1, root_monkey_2):
    # print(message_dct)
    while isinstance(message_dct["root"], str):
        for key, message in message_dct.items():
            if isinstance(message, str):
                reg_expression = re.match(REG_EXP, message)
                monkey_1 = reg_expression.group(1)
                monkey_2 = reg_expression.group(3)
                if isinstance(message_dct[monkey_1], int) and isinstance(message_dct[monkey_2], int):
                    message_dct[key] = int(message_decoder(message, message_dct))

    # print(message_dct)
    return message_dct["root"], message_dct[root_monkey_1], message_dct[root_monkey_2]


def message_equalizer(message_dct, root_monkey_1, root_monkey_2):
    low = 0
    high = 100000000000000000
    new_value_monkey_1 = -1
    new_value_monkey_2 = 0
    while not new_value_monkey_1 == new_value_monkey_2:
        mid = math.floor((low + high) / 2)
        message_dct["humn"] = mid
        new_message_dct = message_dct.copy()
        dct, new_value_monkey_1, new_value_monkey_2 = message_decription(new_message_dct, root_monkey_1, root_monkey_2)

        # print("Mid = ", mid)
        # print("new_value_monkey_1 - new_value_monkey_2 = ", new_value_monkey_1 - new_value_monkey_2)
        if new_value_monkey_1 - new_value_monkey_2 > 0:
            low = mid
        elif new_value_monkey_1 - new_value_monkey_2 < 0:
            high = mid

    return mid


if __name__ == "__main__":
    message_dct = {}
    for line in FileReader().gen_file_reader("day_21.txt"):
        line_to_check = line.rstrip()
        try:
            message_dct[line_to_check[:4]] = int(line_to_check[6:])
        except:
            message_dct[line_to_check[:4]] = line_to_check[6:]

    root_expression = message_dct["root"]
    reg_expression = re.match(REG_EXP, root_expression)
    root_monkey_1 = reg_expression.group(1)
    root_monkey_2 = reg_expression.group(3)

    print(f"Part one Result = {message_decription(dict(message_dct), root_monkey_1, root_monkey_2)[0]}")

    print(f"New humn message =  {message_equalizer(dict(message_dct), root_monkey_1, root_monkey_2)}")
