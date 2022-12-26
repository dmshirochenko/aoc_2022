# https://adventofcode.com/2022/day/1

from get_json_file import UrlConnector


class ElvesCanteen:
    def __init__(self):
        self.top_3_callories_list = [0 for _ in range(3)]

    def _string_reader(self, string_to_read):
        return string_to_read.rsplit("\n")

    def count_max_calories(self, calories_input):
        sum_for_elv = 0
        formatter_calories_list = self._string_reader(calories_input)

        for cal in formatter_calories_list:
            if cal != "":
                sum_for_elv += int(cal)
            else:
                self._max_array_check(sum_for_elv)  # store top 3 results
                sum_for_elv = 0

        return self.top_3_callories_list[-1:], self._sum_of_the_list()

    def _max_array_check(self, sum_to_check):
        for index in range(len(self.top_3_callories_list)):
            if sum_to_check > self.top_3_callories_list[index]:
                self.top_3_callories_list[index] = sum_to_check
                self.top_3_callories_list.sort()
                return True

    def _sum_of_the_list(self):
        return sum(self.top_3_callories_list)


if __name__ == "__main__":
    connection_instance = UrlConnector()
    response = connection_instance.get_json("https://adventofcode.com/2022/day/1/input")

    canteen_instance = ElvesCanteen()
    max_value, sum_of_the_3 = canteen_instance.count_max_calories(response)
    print(f"Max value is = {max_value}, Sum_of_the_3 is = {sum_of_the_3}")
    # part one, correct answer = 66616
    # part two, correct answer [66250, 66306, 66616] sum 199172
