# https://adventofcode.com/2022/day/10


class TvResponder:
    def __init__(self):
        self.signal_strength = {"20": 0, "60": 0, "100": 0, "140": 0, "180": 0, "220": 0}
        self.crt_wide = 40
        self.crt_high = 6
        self.crt = [["." for x in range(self.crt_wide)] for y in range(self.crt_high)]
        self.sprite_position = [0, 1, 2]
        self.line_to_draw = 0

    def _gen_file_reader(self, file_name):
        try:
            file = open(file_name, "r")
            for row in file:
                yield row
        finally:
            file.close()

    def _check_the_line(self, number):
        if number <= 39:
            return (0, 0)
        elif 40 <= number <= 79:
            return (1, 40)
        elif 80 <= number <= 119:
            return (2, 80)
        elif 120 <= number <= 159:
            return (3, 120)
        elif 160 <= number <= 199:
            return (4, 160)
        elif 200 <= number <= 240:
            return (5, 200)

    def _check_the_cycle(self, cycle_number, signal_value_x):
        if str(cycle_number) in self.signal_strength:
            # print("cycle_number", cycle_number)
            # print("signal_value_x", signal_value_x)
            self.signal_strength[str(cycle_number)] += cycle_number * signal_value_x

    def _pixel_check_to_draw(self, cycle_number):
        print("cycle_number", cycle_number)
        row_to_draw, sum_to_extract = self._check_the_line(cycle_number)
        print("row_to_draw", row_to_draw)
        print("sum_to_extract", sum_to_extract)
        if cycle_number - sum_to_extract in self.sprite_position:
            self.crt[row_to_draw][cycle_number - sum_to_extract] = "#"
            print("self.crt[0][cycle_number] =", self.crt[0][cycle_number - sum_to_extract])

    def _register_move(self, signal_value_x):
        print("index_to_draw")
        self.sprite_position = [x + signal_value_x for x in self.sprite_position]
        print("Crt move", self.sprite_position)

    def tv_signal_processing(self, file_name):
        signal_value_x = 1
        cycle_number = 0
        for line in self._gen_file_reader(file_name):
            line_stripped = line.rstrip()
            if line_stripped[:4] == "addx":
                self._pixel_check_to_draw(cycle_number)
                cycle_number += 1
                self._pixel_check_to_draw(cycle_number)
                self._check_the_cycle(cycle_number, signal_value_x)
                cycle_number += 1
                # self._pixel_check_to_draw(cycle_number)
                self._check_the_cycle(cycle_number, signal_value_x)
                self._register_move(int(line_stripped[5:]))
                signal_value_x += int(line_stripped[5:])
            elif line_stripped[:4] == "noop":
                cycle_number += 1
                self._pixel_check_to_draw(cycle_number)
                self._check_the_cycle(cycle_number, signal_value_x)


if __name__ == "__main__":
    tv_responder_instance = TvResponder()
    tv_responder_instance.tv_signal_processing("day_10.txt")
    sum_of_signal_strength = 0
    for val in tv_responder_instance.signal_strength.values():
        sum_of_signal_strength += val

    print("sum_of_signal_strength = ", sum_of_signal_strength)
    for row in tv_responder_instance.crt:
        print(row)
