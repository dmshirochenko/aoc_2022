# NOT SOLVED
# https://adventofcode.com/2022/day/24

MOVES = {"R": (0, 1), "L": (0, -1), "D": (1, 0), "U": (-1, 0)}
WIND_DIRECTION = {">": "R", "<": "L", "v": "D", "^": "U"}
ROUNDS = 10


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


class Blizzards:
    def __init__(self, bliz_sign, coordinate):
        self.direction = WIND_DIRECTION[bliz_sign]
        self.bliz_sign = bliz_sign
        self.coordinate = coordinate

    def __repr__(self) -> str:
        return f"Blizzard cord {self.coordinate} dir '{self.direction}'"


def coordinate_to_start_after_the_wall(bliz_new_row, bliz_new_col, bliz, grip_map):

    if bliz.direction == "R":
        return (bliz_new_row, 1)
    elif bliz.direction == "L":
        return (bliz_new_row, -2)
    elif bliz.direction == "U":
        return (-2, bliz_new_col)
    elif bliz.direction == "D":
        return (1, bliz_new_col)


def blizzard_move(bliz, grip_map, blizzard_dct):
    bliz_current_row, bliz_current_col, bliz_count = bliz.coordinate
    row_d, col_d = MOVES[bliz.direction]

    bliz_new_row = bliz_current_row + row_d
    bliz_new_col = bliz_current_col + col_d

    if grip_map[bliz_new_row][bliz_new_col] == "#":
        bliz_new_row, bliz_new_col = coordinate_to_start_after_the_wall(bliz_new_row, bliz_new_col, bliz, grip_map)

    # check current cell

    if grip_map[bliz_current_row][bliz_current_row] in WIND_DIRECTION:
        grip_map[bliz_current_row][bliz_current_row] = "."
    elif grip_map[bliz_current_row][bliz_current_row].isdigit():
        digit_diff = int(grip_map[bliz_current_row][bliz_current_row]) - 1
        print("digit_diff", digit_diff)
        if digit_diff > 1:
            grip_map[bliz_current_row][bliz_current_row] = str(digit_diff)
        else:
            grip_map[bliz_current_row][bliz_current_row] = "."

    # check next cell
    if grip_map[bliz_new_row][bliz_new_col] in WIND_DIRECTION:
        grip_map[bliz_new_row][bliz_new_col] = "2"
    elif grip_map[bliz_new_row][bliz_new_col].isdigit():
        digit = int(grip_map[bliz_new_row][bliz_new_col])
        grip_map[bliz_new_row][bliz_new_col] = str(digit + 1)
    elif grip_map[bliz_new_row][bliz_new_col] in [".", "E"]:
        grip_map[bliz_new_row][bliz_new_col] = bliz.bliz_sign

    bliz.coordinate = (bliz_new_row, bliz_new_col, bliz_count)


def blizzard_simulation(grip_map, blizzard_dct):
    is_blizzard_continues = True
    round_count = 0
    while is_blizzard_continues:
        round_count += 1
        for bliz in blizzard_dct:
            blizzard_move(blizzard_dct[bliz], grip_map, blizzard_dct)

        print("Round ", round_count)
        createMap(grip_map, rows, cols)

        if ROUNDS == round_count:
            is_blizzard_continues = False


def createMap(map_grid, rows, cols):
    for h in range(rows):
        for x in range(cols):
            print(map_grid[h][x], sep="", end="")
        print()


if __name__ == "__main__":
    grip_map = []
    rows = 0
    blizzard_dct = {}
    bliz_count = 0
    for line in FileReader().gen_file_reader("day_24.txt"):
        grip_map.append([])
        stripped_line = line.rstrip()
        cols = len(stripped_line)
        for i in range(cols):
            grip_map[rows].append(stripped_line[i])
            if stripped_line[i] in WIND_DIRECTION:
                blizzard_dct[(bliz_count)] = Blizzards(stripped_line[i], (rows, i, bliz_count))
                bliz_count += 1

        rows += 1

    createMap(grip_map, rows, cols)
    blizzard_simulation(grip_map, blizzard_dct)
