# https://adventofcode.com/2022/day/13

import json


class Node:
    # Constructor to create a new node
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def list_checker(message):
    count = -1
    mess_1, mess_2 = message
    for pair in zip(mess_1, mess_2):
        # print("Message in checker left ", pair[0])
        # print("Message in checker right ", pair[1])
        if isinstance(pair[0], int) and isinstance(pair[1], int):  # compare ints
            if pair[0] < pair[1]:
                count = 1
            elif pair[0] > pair[1]:
                count = 0
            else:
                count = -1
        elif isinstance(pair[0], list) and isinstance(pair[1], list):  # both lists
            count = list_checker([pair[0], pair[1]])
        elif isinstance(pair[0], list) and isinstance(pair[1], int):  # rigth int
            count = list_checker([pair[0], [pair[1]]])
        elif isinstance(pair[0], int) and isinstance(pair[1], list):  # left int
            count = list_checker([[pair[0]], pair[1]])
        if count > -1:
            break
    if count == -1:
        if len(mess_1) < len(mess_2):
            count = 1
        elif len(mess_1) > len(mess_2):
            count = 0
    return count


def message_checker(dict_of_messages):
    right_message = 0
    number_of_index = 1
    right_indexs = []
    for key, message in dict_of_messages.items():
        print("message", message)
        is_equal = list_checker(message)
        if is_equal == 1:
            print("GOOD MESSAGE")
            right_message += number_of_index
            right_indexs.append(number_of_index)
        else:
            print("BAD MESSAGE")
        number_of_index += 1
        print("_________________________")

    return right_message


def message_reordering(dict_of_messages):
    is_continue_to_check = True
    messages_block = []
    messages_block.append([[2]])
    messages_block.append([[6]])
    divider_index_1 = 1
    divider_index_2 = 1
    for key, message in dict_of_messages.items():
        for item in message:
            messages_block.append(item)

    print("Initial messages_block", messages_block)
    while is_continue_to_check:
        is_continue_to_check = False
        for index in range(len(messages_block) - 1):
            print("message to compare = ", (messages_block[index], messages_block[index + 1]))
            if list_checker((messages_block[index], messages_block[index + 1])) != 1:
                print("Left is bigger that right")
                poped_item = messages_block.pop(index + 1)
                messages_block.insert(index, poped_item)
                is_continue_to_check = True
            if messages_block[index] == [[2]]:
                divider_index_1 = index + 1
            if messages_block[index] == [[6]]:
                divider_index_2 = index + 1

    print("messages_block final ", messages_block)
    print(divider_index_1, divider_index_2)
    return divider_index_1 * divider_index_2


if __name__ == "__main__":
    dict_of_messages = {}
    list_of_messages_to_add = []
    n = 1
    with open("day_13.txt", "a") as f:
        f.write("\n")
    with open("day_13.txt", "r") as f:
        for l in f.readlines():
            if "[" in l:
                list_of_messages_to_add.append(json.loads(l.strip()))
            elif l == "\n":
                if list_of_messages_to_add:
                    dict_of_messages[n] = list_of_messages_to_add
                    list_of_messages_to_add = []
                    n += 1

    correct_messages = message_checker(dict_of_messages)
    message_reorder_result = message_reordering(dict_of_messages)
    print(f"Part one correct messages = {correct_messages}")
    print(f"Part two correct messages = {message_reorder_result}")
    # list_to_check = ['Adam', ['Bob', ['Chet', 'Cat'], 'Barb', 'Bert'], 'Alex', ['Bea', 'Bill'], 'Ann']
    # count_leaf_items(list_to_check)
