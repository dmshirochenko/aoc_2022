# https://adventofcode.com/2022/day/9


class RopeModeling:
    def __init__(self):
        self.rows = 750
        self.cols = 750
        self.initial_state = [
            [
                {
                    "H": {"Visited": False},
                    "T": [
                        {"Visited": False},
                        {"Visited": False},
                        {"Visited": False},
                        {"Visited": False},
                        {"Visited": False},
                        {"Visited": False},
                        {"Visited": False},
                        {"Visited": False},
                        {"Visited": False},
                    ],
                }
                for i in range(self.cols)
            ]
            for j in range(self.rows)
        ]
        self.head_current_position = [250, 250]
        self.tail_current_position = [
            [250, 250],
            [250, 250],
            [250, 250],
            [250, 250],
            [250, 250],
            [250, 250],
            [250, 250],
            [250, 250],
            [250, 250],
        ]

    def _gen_file_reader(self, file_name):
        try:
            file = open(file_name, "r")
            for row in file:
                yield row
        finally:
            file.close()

    def _change_position_state(self, position, point_of_the_rope, tail_num=0):
        # print(position, point_of_the_rope, tail_num)
        if point_of_the_rope == "H":
            self.initial_state[position[0]][position[1]][point_of_the_rope]["Visited"] = True
        elif point_of_the_rope == "T":
            self.initial_state[position[0]][position[1]][point_of_the_rope][tail_num]["Visited"] = True

    def _check_if_tail_move(self, direction, coordinate_1, coordinate_2):
        print("coordinate_1", coordinate_1)
        print("coordinate_2", coordinate_2)
        print("direction", direction)
        # if abs(coordinate_1[0] - coordinate_2[0]) > 1 or abs(coordinate_1[1] - coordinate_2[1]) > 1:
        #    return True

        if direction == "R" or direction == "L":
            # diff_coordinate = coordinate_1[1] - coordinate_2[1]
            if abs(coordinate_1[1] - coordinate_2[1]) > 1:
                return True

        if direction == "U" or direction == "D":
            # diff_coordinate = coordinate_1[0] - coordinate_2[0]
            if abs(coordinate_1[0] - coordinate_2[0]) > 1:
                return True

        return False

    def _check_if_tail_move_2(self, direction, coordinate_1, coordinate_2):
        if abs(coordinate_1[0] - coordinate_2[0]) > 1 or abs(coordinate_1[1] - coordinate_2[1]) > 1:
            return True

    def _sign(self, value):
        return min(max(value, -1), 1)

    def _new_tail_position(self, head_position, tail_position):
        print("head_position", head_position)
        print("tail_position", tail_position)
        tail_position[0] += self._sign(head_position[0] - tail_position[0])
        tail_position[1] += self._sign(head_position[1] - tail_position[1])
        """
        for i in range(2):
            tail_position[i] += 1 if head_position[i] > tail_position[i] else -1 if head_position[i] < tail_position[i] else 0
        """
        print("tail_position_new", tail_position)
        return tail_position

    def rope_checker(self, file_name):
        self._change_position_state(self.head_current_position, "H")
        for tail_number in range(9):
            self._change_position_state(self.tail_current_position[tail_number], "T", tail_number)
        for line in self._gen_file_reader(file_name):
            direction, number_of_steps = line.rstrip()[:1], int(line.rstrip()[2:])
            for step in range(number_of_steps):
                if direction == "R":
                    print("R")
                    self.head_current_position[1] += 1
                    if self._check_if_tail_move(direction, self.head_current_position, self.tail_current_position[0]):
                        new_tail_position = self.head_current_position.copy()
                        new_tail_position[1] -= 1
                        self.tail_current_position[0] = new_tail_position.copy()
                        self._change_position_state(self.tail_current_position[0], "T")
                        for tail_number in range(1, 9):
                            # print("tail_numner =", tail_number)
                            if self._check_if_tail_move_2(
                                direction,
                                self.tail_current_position[tail_number - 1],
                                self.tail_current_position[tail_number],
                            ):
                                # new_tail_position = self.tail_current_position[tail_number-1].copy()
                                # new_tail_position[1] -= 1
                                self.tail_current_position[tail_number] = self._new_tail_position(
                                    self.tail_current_position[tail_number - 1], self.tail_current_position[tail_number]
                                )
                                self._change_position_state(self.tail_current_position[tail_number], "T", tail_number)
                    self._change_position_state(self.head_current_position, "H")
                elif direction == "L":
                    print("L")
                    self.head_current_position[1] -= 1
                    if self._check_if_tail_move(direction, self.head_current_position, self.tail_current_position[0]):
                        new_tail_position = self.head_current_position.copy()
                        new_tail_position[1] += 1
                        self.tail_current_position[0] = new_tail_position.copy()
                        self._change_position_state(self.tail_current_position[0], "T")
                        for tail_number in range(1, 9):
                            # print("tail_numner =", tail_number)
                            if self._check_if_tail_move_2(
                                direction,
                                self.tail_current_position[tail_number - 1],
                                self.tail_current_position[tail_number],
                            ):
                                # new_tail_position = self.tail_current_position[tail_number-1].copy()
                                # new_tail_position[1] += 1
                                self.tail_current_position[tail_number] = self._new_tail_position(
                                    self.tail_current_position[tail_number - 1], self.tail_current_position[tail_number]
                                )
                                self._change_position_state(self.tail_current_position[tail_number], "T", tail_number)
                    self._change_position_state(self.head_current_position, "H")
                elif direction == "U":
                    print("U")
                    self.head_current_position[0] -= 1
                    if self._check_if_tail_move(direction, self.head_current_position, self.tail_current_position[0]):
                        new_tail_position = self.head_current_position.copy()
                        new_tail_position[0] += 1
                        self.tail_current_position[0] = new_tail_position
                        self._change_position_state(self.tail_current_position[0], "T")
                        print("self.tail_current_position[0]", self.tail_current_position[0])
                        for tail_number in range(1, 9):
                            print("tail_numner =", tail_number)
                            if self._check_if_tail_move_2(
                                direction,
                                self.tail_current_position[tail_number - 1],
                                self.tail_current_position[tail_number],
                            ):
                                # new_tail_position = self.tail_current_position[tail_number-1].copy()
                                # print('self.tail_current_position[tail_number-1]', self.tail_current_position[tail_number-1])
                                # new_tail_position[0] += 1
                                # print("tail_number-1", tail_number-1)
                                self.tail_current_position[tail_number] = self._new_tail_position(
                                    self.tail_current_position[tail_number - 1], self.tail_current_position[tail_number]
                                )
                                print(
                                    "self.tail_current_position[tail_number]", self.tail_current_position[tail_number]
                                )
                                self._change_position_state(self.tail_current_position[tail_number], "T", tail_number)
                    self._change_position_state(self.head_current_position, "H")
                elif direction == "D":
                    print("D")
                    self.head_current_position[0] += 1
                    if self._check_if_tail_move(direction, self.head_current_position, self.tail_current_position[0]):
                        new_tail_position = self.head_current_position.copy()
                        new_tail_position[0] -= 1
                        self.tail_current_position[0] = new_tail_position.copy()
                        self._change_position_state(self.tail_current_position[0], "T")
                        for tail_number in range(1, 9):
                            # print("tail_numner =", tail_number)
                            if self._check_if_tail_move_2(
                                direction,
                                self.tail_current_position[tail_number - 1],
                                self.tail_current_position[tail_number],
                            ):
                                # new_tail_position = self.tail_current_position[tail_number-1].copy()
                                # new_tail_position[0] -= 1
                                self.tail_current_position[tail_number] = self._new_tail_position(
                                    self.tail_current_position[tail_number - 1], self.tail_current_position[tail_number]
                                )
                                self._change_position_state(self.tail_current_position[tail_number], "T", tail_number)
                    self._change_position_state(self.head_current_position, "H")

                print("H", self.head_current_position)
                print("T", self.tail_current_position)

        # for row in self.initial_state:
        #    print(row)


if __name__ == "__main__":
    print("start")
    rope_model_instance = RopeModeling()
    rope_model_instance.rope_checker("day_9.txt")
    count_tail_pos = 0
    for row in rope_model_instance.initial_state:
        for cell in row:
            if cell["T"][8]["Visited"] == True:
                count_tail_pos += 1

    print(count_tail_pos)
    # Puzzle 1:  6175
    # Puzzle 2:  2578
