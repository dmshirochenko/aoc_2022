# https://adventofcode.com/2022/day/6


class ElvComminicationSystem:
    def __init__(self):
        pass

    def _gen_file_reader(self, file_name):
        try:
            file = open(file_name, "r")
            for row in file:
                yield row
        finally:
            file.close()

    def commication_reader(self, file_name, message_length):
        line_to_check = ""
        for line in self._gen_file_reader(file_name):
            line_to_check += line

        index_to_search = 0
        non_unique_symbols_found = True
        set_to_store_values = set()
        while non_unique_symbols_found:
            for char in line_to_check[index_to_search : index_to_search + message_length]:
                set_to_store_values.add(char)

            if len(set_to_store_values) == message_length:
                non_unique_symbols_found = False
            else:
                index_to_search += 1
                set_to_store_values.clear()

            if index_to_search >= len(line_to_check):  # if non unique symbols will not be found
                return False

        return index_to_search + message_length


if __name__ == "__main__":
    communication_system_instance = ElvComminicationSystem()
    char_to_find_task_1 = communication_system_instance.commication_reader("day_6.txt", 4)
    char_to_find_task_2 = communication_system_instance.commication_reader("day_6.txt", 14)
    print(f"Task one = {char_to_find_task_1}, Task two = {char_to_find_task_2}")
