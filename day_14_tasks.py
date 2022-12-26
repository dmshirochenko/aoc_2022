# https://adventofcode.com/2022/day/14

MOVES = {"R": (1, 0), "L": (-1, 0), "D": (0, 1), "U": (0, -1), "DL": (-1, 1), "DR": (1, 1)}

BOTTOM_BUILD_WALLS = 165
BOTTOM_HEIGHT = BOTTOM_BUILD_WALLS + 2
BOTTOM_WIDE = 500


def createCave(dct, xx, h):
    for y in range(h):
        for x in range(500 - xx, 500 + xx):
            print(dct[(x, y)] if (x, y) in dct else ".", sep="", end="")
        print()


def walls_bottom_creation(map_grip):
    for i in range(500 - BOTTOM_WIDE, 500 + BOTTOM_WIDE):
        map_grip[(i, BOTTOM_HEIGHT)] = "#"

    return map_grip


def walls_creation(walls_coord, map_grip):
    for wall in walls_coord:
        for i in range(len(wall) - 1):
            col_begin, row_begin = [int(x) for x in wall[i].split(",")]
            col_end, row_end = [int(x) for x in wall[i + 1].split(",")]

            if col_begin > col_end:
                for i in range((col_begin - col_end) + 1):
                    map_grip[(col_begin - i, row_begin)] = "#"
            elif col_begin < col_end:
                for i in range((col_end - col_begin) + 1):
                    map_grip[(col_begin + i, row_begin)] = "#"
            elif row_begin > row_end:
                for i in range((row_begin - row_end) + 1):
                    map_grip[(col_begin, row_begin - i)] = "#"
            elif row_begin < row_end:
                for i in range((row_end - row_begin) + 1):
                    map_grip[(col_begin, row_begin + i)] = "#"

    return map_grip


def sand_move(cave_map, is_part_one=False):
    is_proceed = True
    initial_position = (500, 0)
    next_move = tuple(map(sum, zip(initial_position, MOVES["D"])))
    number_of_units = 0
    while is_proceed:
        move_down = tuple(map(sum, zip(next_move, MOVES["D"])))
        move_down_left = tuple(map(sum, zip(next_move, MOVES["DL"])))
        move_down_right = tuple(map(sum, zip(next_move, MOVES["DR"])))
        current_possition = next_move
        if sand_move_validation(move_down, cave_map):
            # check if move down is possible
            next_move = tuple(map(sum, zip(current_possition, MOVES["D"])))
        elif sand_move_validation(move_down_left, cave_map):
            # check if move down left is possible
            next_move = tuple(map(sum, zip(current_possition, MOVES["DL"])))
        elif sand_move_validation(move_down_right, cave_map):
            # check if move down right is possible
            next_move = tuple(map(sum, zip(current_possition, MOVES["DR"])))
        else:
            cave_map[current_possition] = "o"
            next_move = initial_position
            number_of_units += 1
            if current_possition == (500, 0):
                is_proceed = False

        if is_part_one:
            if next_move[1] == 165:
                is_proceed = False

    return number_of_units


def sand_move_validation(next_cell, cave_map):
    next_move = cave_map.get(next_cell)
    # print("next_move from function", next_move)
    if next_move == "#":
        return False
    if next_move == "o":
        return False
    if next_move == "+":
        return True
    if next_move is None:
        return True


if __name__ == "__main__":
    cave_map = {(500, 0): "+"}
    walls_dict = []
    xx = 120  # 100 #10
    h = 170  # 170 #12
    with open("day_14.txt", "r") as f:
        walls_dict = [l.strip().split(" -> ") for l in f.readlines()]

    """
    Part one and Part two are working only separatly,
    Uncomment Part 1 and comment part 2 to make it work
    """

    walls_creation(walls_dict, cave_map)

    # part 1
    # number_of_sand = sand_move(cave_map, is_part_one=True)
    # print(f"First part answer = ", number_of_sand)

    # part 2
    walls_bottom_creation(cave_map)
    number_of_sand_2 = sand_move(cave_map)
    print(f"Second part answer = ", number_of_sand_2)

    createCave(dct=cave_map, xx=xx, h=h)
