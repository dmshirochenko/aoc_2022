# https://adventofcode.com/2022/day/3

import string


class ElvRuckSacks:
    def __init__(self):
        self.mapping_table = self._mapping_table_fill()
        self.number_of_rucks_to_compare = 3

    def _gen_file_reader(self, file_name):
        for row in open(file_name, "r"):
            yield row

    def _mapping_table_fill(self):
        return dict(zip(string.ascii_letters, range(1, 58)))

    def rucksack_reorginizer_part_1(self, file_name):
        priority_score_sum = 0
        shared_items = set()
        for row in self._gen_file_reader(file_name):
            first_compartment = row[: len(row) // 2]
            second_compartment = row[len(row) // 2 :]
            for item in first_compartment:
                for item_2 in second_compartment:
                    if item == item_2:
                        shared_items.add(item)

            for shared_item in shared_items:  # count points
                priority_score_sum += self.mapping_table[shared_item]

            shared_items.clear()  # clear set for next before reading next row

        return priority_score_sum

    def rucksack_reorginizer_part_2(self, file_name):
        priority_score_sum = 0
        shared_items_1_2 = set()
        shared_items_1_2_3 = set()
        list_of_shared_items = []
        row_number = 0
        for row in self._gen_file_reader(file_name):
            list_of_shared_items.append(set(row.rstrip("\n")))

        group_by_three = [list_of_shared_items[i : i + 3] for i in range(0, len(list_of_shared_items), 3)]

        for sets in group_by_three:
            for letter_1 in sets[0]:
                for letter_2 in sets[1]:
                    if letter_1 == letter_2:
                        shared_items_1_2.add(letter_1)

            for letter_common_1_2 in shared_items_1_2:
                for letter_3 in sets[2]:
                    if letter_common_1_2 == letter_3:
                        shared_items_1_2_3.add(letter_common_1_2)

            for shared_item in shared_items_1_2_3:  # count points
                priority_score_sum += self.mapping_table[shared_item]

            shared_items_1_2.clear()
            shared_items_1_2_3.clear()

        return priority_score_sum


if __name__ == "__main__":
    rucksack_instance = ElvRuckSacks()
    priority_score_sum = rucksack_instance.rucksack_reorginizer_part_1("day_3.txt")
    priority_score_sum_2 = rucksack_instance.rucksack_reorginizer_part_2("day_3.txt")
    print(priority_score_sum)
    print(priority_score_sum_2)
