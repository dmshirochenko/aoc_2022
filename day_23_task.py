# https://adventofcode.com/2022/day/23

import math
from collections import OrderedDict

MOVES = {
    "E": (0, 1),
    "W": (0, -1),
    "S": (1, 0),
    "N": (-1, 0),
    "NE": (-1, 1),
    "NW": (-1, -1),
    "SE": (1, 1),
    "SW": (1, -1),
}
directions_to_check_order_dct = OrderedDict(
    {"N": ["N", "NE", "NW"], "S": ["S", "SE", "SW"], "W": ["W", "NW", "SW"], "E": ["E", "NE", "SE"]}
)
ROUND_NUMBERS = 10


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


class Elves:
    def __init__(self, elf_coordinate):
        self.elf_coordinate = elf_coordinate
        self.elf_movements_proposal = []
        self.need_to_move = False

    def __repr__(self) -> str:
        return f"Elv coordinate  = {self.elf_coordinate}, next moves proposal {self.elf_movements_proposal}, need to move {self.need_to_move}"


def check_if_move_in_list_range(position_to_check, map_grid):
    min_row = -1
    min_col = -1

    max_row = len(map_grid)
    max_col = len(map_grid[0])
    position_to_check_row, position_to_check_col = position_to_check
    # print("position_to_check ", position_to_check)
    # print("max_row", max_row)
    if (min_row < position_to_check_row < max_row) and (min_col < position_to_check_col < max_col):
        return True
    else:
        return False


def moves_proposal(elf, map_grid):
    need_to_move = False
    for direction, directions_to_check in directions_to_check_order_dct.items():
        # print("direction ", direction)
        # print("elf", elf)
        is_valid_direction = True
        for check in directions_to_check:
            elf_row, elf_col = elf.elf_coordinate
            move_row, move_col = MOVES[check]
            coord_to_check_row = elf_row + move_row
            coord_to_check_col = elf_col + move_col
            if check_if_move_in_list_range((coord_to_check_row, coord_to_check_col), map_grid):
                if map_grid[coord_to_check_row][coord_to_check_col] == "#":
                    is_valid_direction = False
                    need_to_move = True
                    break
            else:
                if check == direction:  # if direction out of the map, we should add it
                    is_valid_direction = False
                    break

        if is_valid_direction:
            if direction not in elf.elf_movements_proposal:
                elf.elf_movements_proposal.append(direction)

    if need_to_move and elf.elf_movements_proposal:
        elf.need_to_move = True
    else:
        elf.need_to_move = False


def elf_new_temprorary_coordinates(elf):
    if elf.elf_movements_proposal:
        direction_to_move = elf.elf_movements_proposal[0]

        move_row, move_col = MOVES[direction_to_move]
        elf_row, elf_col = elf.elf_coordinate

        temp_coor_row = elf_row + move_row
        temp_coor_col = elf_col + move_col

        return (temp_coor_row, temp_coor_col)


def elf_move(elf, new_position, elves_dict, map_grid):
    old_position_row, old_position_col = elf.elf_coordinate
    new_position_row, new_position_col = new_position

    if check_if_move_in_list_range(new_position, map_grid):
        # moves on the map
        map_grid[old_position_row][old_position_col] = "."
        map_grid[new_position_row][new_position_col] = "#"

        # updating elf object
        elf.elf_coordinate = new_position
        # updating elf dict
        elves_dict[new_position] = elf
        # deleting old positing from elves dict
        del elves_dict[(old_position_row, old_position_col)]


def optimal_spots_check(elves_dict, map_grid, rows, cols):
    # for round in range(ROUND_NUMBERS):
    is_elfs_need_to_move = True
    round_number = 1
    while is_elfs_need_to_move:
        elf_round_temprorary_positions_dct = {}

        for elf in elves_dict:
            moves_proposal(elves_dict[elf], map_grid)
            if elves_dict[elf].need_to_move:
                temp_coor_row, temp_coor_col = elf_new_temprorary_coordinates(elves_dict[elf])
                if (temp_coor_row, temp_coor_col) not in elf_round_temprorary_positions_dct:
                    elf_round_temprorary_positions_dct[(temp_coor_row, temp_coor_col)] = [elves_dict[elf]]
                else:
                    elf_round_temprorary_positions_dct[(temp_coor_row, temp_coor_col)].append(elves_dict[elf])

        # print(f"elves_dict before move {elves_dict}")

        if not elf_round_temprorary_positions_dct:
            is_elfs_need_to_move = False
            break

        for temp_position, elf_list in elf_round_temprorary_positions_dct.items():
            if len(elf_list) == 1:
                elf_move(elf_list[0], temp_position, elves_dict, map_grid)

        for elf in elves_dict:
            elves_dict[elf].elf_movements_proposal.clear()

        elf_round_temprorary_positions_dct.clear()

        directions_to_check_order_dct.move_to_end(
            next(iter(directions_to_check_order_dct))
        )  # move direction to the end
        round_number += 1

        # print(f"Round {round + 1}")
        # createMap(map_grid, rows, cols)
        # print(f"elves_dict after move {elves_dict}")
        # print("Round end_________")
    print("round_number", round_number)
    return round_number


def tiles_in_rectangle(elves_dict, map_grid):
    min_row = math.inf
    min_col = math.inf
    max_row = -math.inf
    max_col = -math.inf
    for elf in elves_dict:
        row, col = elf
        if row > max_row:
            max_row = row
        if row < min_row:
            min_row = row
        if col > max_col:
            max_col = col
        if col < min_col:
            min_col = col

    width = max_col + 1 - min_col
    height = max_row + 1 - min_row
    area = width * height
    count_tiles = area - len(elves_dict)
    """
    count_tiles = 0
    for row in range(min_row, max_row + 1):
        for col in range(min_col, max_col + 1):
            if map_grid[row][col] == ".":
                count_tiles += 1
    """
    return count_tiles


def createMap(map_grid, rows, cols):
    for h in range(rows):
        for x in range(cols):
            print(map_grid[h][x], sep="", end="")
        print()


if __name__ == "__main__":
    # initial size 70x70
    gap_to_add = 50
    rows, cols = (70 + 2 * gap_to_add, 90 + 2 * gap_to_add)
    map_grid = [["." for i in range(cols)] for j in range(rows)]
    # map_grid = []
    rows_count = gap_to_add
    elves_dict = dict()
    for line in FileReader().gen_file_reader("day_23.txt"):
        # map_grid.append([])
        stripped_line = line.rstrip()
        # cols = len(stripped_line)
        for i in range(len(stripped_line)):
            try:
                map_grid[rows_count][i + gap_to_add] = stripped_line[i]
                if stripped_line[i] == "#":
                    elves_dict[(rows_count, i + gap_to_add)] = Elves((rows_count, i + gap_to_add))
            except IndexError:
                pass

        rows_count += 1

    # createMap(map_grid, rows, cols)
    optimal_spots_check(elves_dict, map_grid, rows, cols)
    print(f"tiles in min rectangle = {tiles_in_rectangle(elves_dict, map_grid)}")
    createMap(map_grid, rows, cols)
