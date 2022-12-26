# https://adventofcode.com/2022/day/5

from collections import deque
import re


class ElvStacks:
    def __init__(self, file_name):
        self.file_name = file_name
        self.dict_of_stacks_example = {"1": deque(["Z", "N"]), "2": ["M", "C", "D"], "3": ["P"]}
        self.dict_of_stacks_example_2 = {
            "1": deque(["V", "C", "D", "R", "Z", "G", "B", "W"]),
            "2": deque(["G", "W", "F", "C", "B", "S", "T", "V"]),
            "3": deque(["C", "B", "S", "N", "W"]),
            "4": deque(["Q", "G", "M", "N", "J", "V", "C", "P"]),
            "5": deque(["T", "S", "L", "F", "D", "H", "B"]),
            "6": deque(["J", "V", "T", "W", "M", "N"]),
            "7": deque(["P", "F", "L", "C", "S", "T", "G"]),
            "8": deque(["B", "D", "Z"]),
            "9": deque(["M", "N", "Z", "W"]),
        }

        self.dict_of_stacks = self._initial_stacks_position()

    def _gen_file_reader(self, file_name):
        try:
            file = open(file_name, "r")
            for row in file:
                yield row
        finally:
            file.close()

    def _file_log_writer(self, file_name, message):
        with open(file_name, "a") as file:
            file.write(message)
            file.write("\n")

    def _initial_stacks_position(self):
        stackes_to_return = {}
        for line in self._gen_file_reader(self.file_name):
            if "1" in line:
                break
            line_to_parse = line.rstrip().split(" ")
            stacks_index = 1
            empty_space_counter = 0
            for crate in line_to_parse:
                letter_to_find = re.match("\[(\w)\]", crate)
                if letter_to_find:
                    if str(stacks_index) in stackes_to_return:
                        stackes_to_return[str(stacks_index)].append(letter_to_find.group(1))
                        stacks_index += 1
                    else:
                        stackes_to_return[str(stacks_index)] = deque(letter_to_find.group(1))
                        stacks_index += 1
                else:
                    empty_space_counter += 1
                    if empty_space_counter == 4:
                        empty_space_counter = 0
                        stacks_index += 1

        for stack in stackes_to_return.values():
            stack.reverse()

        return stackes_to_return

    def stacks_move_task_1(self):
        for line in self._gen_file_reader(self.file_name):
            line_to_parse = line.rstrip()
            line_regex = re.search("move (\d+) from (\d+) to (\d+)", line_to_parse)
            if line_regex:
                for _ in range(1, int(line_regex.group(1)) + 1):
                    poped_item = self.dict_of_stacks[line_regex.group(2)].pop()
                    self.dict_of_stacks[line_regex.group(3)].append(poped_item)

    def stacks_move_task_2(self):
        for line in self._gen_file_reader(self.file_name):
            stack_to_keep_crate = deque()
            line_to_parse = line.rstrip()
            line_regex = re.search("move (\d+) from (\d+) to (\d+)", line_to_parse)
            if line_regex:
                for _ in range(1, int(line_regex.group(1)) + 1):
                    poped_item = self.dict_of_stacks[line_regex.group(2)].pop()
                    stack_to_keep_crate.append(poped_item)

                while stack_to_keep_crate:
                    popped_item_from_stack_to_keeep = stack_to_keep_crate.pop()
                    self.dict_of_stacks[line_regex.group(3)].append(popped_item_from_stack_to_keeep)


if __name__ == "__main__":
    stack_intance = ElvStacks("day_5.txt")
    stack_intance.stacks_move_task_2()

    result_string = ""
    for i in range(1, len(stack_intance.dict_of_stacks) + 1):
        poped_item = stack_intance.dict_of_stacks[str(i)].pop()
        result_string += poped_item
    print(result_string)
    # right answers task one TBVFVDZPN, task two VLCWHTDSZ
