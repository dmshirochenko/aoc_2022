# https://adventofcode.com/2022/day/11

import math


class FileReader:
    def __init__(self, file_name):
        self.file_name = file_name

    def _gen_file_reader(self):
        try:
            file = open(self.file_name, "r")
            for row in file:
                yield row
        finally:
            file.close()

    def file_string_append(self, string_to_write):
        with open(self.file_name, "a") as writer:
            writer.write(string_to_write)


class Item:
    def __init__(self, worry_level):
        self.worry_level = int(worry_level)

    def __str__(self):
        return f"Item worried level = {self.worry_level}"

    def set_new_worry_level(self, new_worry_level):
        self.worry_level = new_worry_level


class Monkey:
    def __init__(self, monkey_number):
        self.monkey_number = monkey_number
        self.holding_items = []
        self.opretations_string = ""
        self.tests_conditions_string = ""
        self.if_true_condition = ""
        self.if_false_condition = ""
        self.number_of_inspected_items = 0

    def add_all_items_to_moneky(self, items_string):
        items_list = items_string.split(", ")
        for worried_level in items_list:
            self.holding_items.append(Item(worried_level))

    def monkey_inspect_item(self):
        self.number_of_inspected_items += 1

    def add_item(self, item):
        self.holding_items.append(item)

    def worry_level_change_by_monkey_after_inspection(self, item):
        old = item.worry_level
        new_value = eval(self.opretations_string)
        return new_value

    def worry_level_change_by_monkey_after_they_borred(self, item):
        value_to_change = item.worry_level
        return value_to_change // 3

    def monkey_to_which_throw_the_item(self, item, lcm):
        if lcm:
            item.worry_level %= lcm
        if item.worry_level % int(self.tests_conditions_string) == 0:
            item_to_throw = self.holding_items.pop(0)
            return (int(self.if_true_condition[-1]), item_to_throw)
        else:
            item_to_throw = self.holding_items.pop(0)
            return (int(self.if_false_condition[-1]), item_to_throw)

    def __str__(self):
        return f"Monkey number is {self.monkey_number}"


class ItemsCarriedByMonkeyCounter:
    def __init__(self):
        pass

    def mounkey_parser(self, file_reader_instance):
        monkey_list = []
        monkey_number = 0
        test_conditions_string = ""
        for line in file_reader_instance._gen_file_reader():
            if "Monkey" in line.rstrip():
                monkey_instance = Monkey(monkey_number)
            elif "Starting items" in line.rstrip():
                monkey_instance.add_all_items_to_moneky(line[17:].strip())
            elif "Operation" in line.rstrip():
                monkey_instance.opretations_string = line[18:].strip()
            elif "Test" in line.rstrip():
                monkey_instance.tests_conditions_string = line[20:].strip()
            elif "If true" in line.rstrip():
                monkey_instance.if_true_condition = line[12:].strip()
            elif "If false" in line.rstrip():
                monkey_instance.if_false_condition = line[14:].strip()
                monkey_list.append(monkey_instance)
                monkey_number += 1
                test_conditions_string

        return monkey_list

    def round_runner(self, number_of_rounds, monkey_list, is_first_part=False, lcm=None):
        for i in range(number_of_rounds):
            for monkey in monkey_list:
                for item in list(monkey.holding_items):
                    monkey.monkey_inspect_item()
                    new_worry_level_set_by_monkey = monkey.worry_level_change_by_monkey_after_inspection(item)
                    item.set_new_worry_level(new_worry_level_set_by_monkey)

                    if is_first_part:
                        new_worry_level_set_by_monkey_bored = monkey.worry_level_change_by_monkey_after_they_borred(
                            item
                        )
                        item.set_new_worry_level(new_worry_level_set_by_monkey_bored)

                    monkey_number_to_trow, item = monkey.monkey_to_which_throw_the_item(item, lcm)
                    monkey_list[monkey_number_to_trow].add_item(item)
                    # print(f"Item with worry level {item.worry_level} is thrown to monkey {monkey_number_to_trow}")

        return monkey_list


def final_result_repr(monkey_list):
    print(f"Final results after all rounds")
    resulted_activities_list = []
    for monkey in monkey_list:
        resulted_activities_list.append(monkey.number_of_inspected_items)
        # for item in monkey.holding_items:
        #    print(f"Monkey {monkey.monkey_number} holding item {item}")

    resulted_activities_list.sort(reverse=True)
    result_larger_two_multiple = resulted_activities_list[0] * resulted_activities_list[1]
    print(f"Final result = {result_larger_two_multiple}")


if __name__ == "__main__":
    file_reader_instance_day_11 = FileReader("day_11.txt")
    item_counter_instance = ItemsCarriedByMonkeyCounter()

    # Part 1
    number_of_rounds = 20
    monkey_list_1 = item_counter_instance.mounkey_parser(file_reader_instance_day_11)
    item_counter_instance.round_runner(number_of_rounds, monkey_list_1, is_first_part=True)
    final_result_repr(monkey_list_1)

    # Part_2
    number_of_rounds = 10000
    monkey_list_2 = item_counter_instance.mounkey_parser(file_reader_instance_day_11)
    lcm = math.lcm(*[int(monkey.tests_conditions_string) for monkey in monkey_list_2])
    item_counter_instance.round_runner(number_of_rounds, monkey_list_2, lcm=lcm)
    final_result_repr(monkey_list_2)

    # Least Common Multiple acros all dividers of condition Test: divisible by X
    lcm_test = math.lcm(*[x for x in [2, 3, 5, 7, 11, 13, 17, 19]])
    worry_level_test = 19
    print(worry_level_test)
    print(lcm_test)
    # Then mo
    worry_level_test = worry_level_test % lcm
    if worry_level_test % 19 == 0:
        print("True", worry_level_test)
