# https://adventofcode.com/2022/day/22

import re

MOVES = {"R": (0, 1), "L": (0, -1), "D": (1, 0), "U": (-1, 0)}
REG_EXP = "(\d+)([A-Z]{1})"  # |(\d{1})$


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


def createMap(map_grid, rows, cols):
    for h in range(rows):
        for x in range(cols):
            print(map_grid[h][x], sep="", end="")
        print()


def position_change(turn_direction, current_direction):
    if turn_direction == "R":
        if current_direction == "R":
            return "D"
        elif current_direction == "D":
            return "L"
        elif current_direction == "L":
            return "U"
        elif current_direction == "U":
            return "R"
    elif turn_direction == "L":
        if current_direction == "R":
            return "U"
        elif current_direction == "U":
            return "L"
        elif current_direction == "L":
            return "D"
        elif current_direction == "D":
            return "R"


def is_move_legal(map_grid, x, y):
    if map_grid[x][y] == "#":
        return False
    elif map_grid[x][y] in [".", "→", "←", "↓", "↑"]:
        return True


def check_if_end_of_the_map(map_grid, x, y, current_direction):
    try:
        value_for_next_cell = map_grid[x][y]
    except IndexError:
        value_for_next_cell = " "

    if value_for_next_cell == " ":
        if current_direction == "R":
            for j in range(len(map_grid[x])):
                if map_grid[x][j] in [".", "→", "←", "↓", "↑", "#"]:
                    starting_point = (x, j)
                    return starting_point
        elif current_direction == "L":
            for j in range(len(map_grid[x]) - 1, -1, -1):
                if map_grid[x][j] in [".", "→", "←", "↓", "↑", "#"]:
                    starting_point = (x, j)
                    return starting_point
        elif current_direction == "D":
            for h in range(len(map_grid)):
                if map_grid[h][y] in [".", "→", "←", "↓", "↑", "#"]:
                    starting_point = (h, y)
                    return starting_point
        elif current_direction == "U":
            for h in range(len(map_grid) - 1, -1, -1):
                if map_grid[h][y] in [".", "→", "←", "↓", "↑", "#"]:
                    starting_point = (h, y)
                    return starting_point
    else:
        return False


def sign_to_draw(current_direction):
    sign_to_draw_dct = {"R": "→", "L": "←", "D": "↓", "U": "↑"}

    return sign_to_draw_dct[current_direction]


def monkey_move(steps_list, map_grid, rows, cols, starting_point):
    current_direction = "R"
    x, y = starting_point
    for step in steps_list:
        if isinstance(step, int):
            for _ in range(step):
                x_old = x
                y_old = y
                x_d, y_d = MOVES[current_direction]
                x += x_d
                y += y_d
                if check_if_end_of_the_map(map_grid, x, y, current_direction):
                    x, y = check_if_end_of_the_map(map_grid, x, y, current_direction)

                if is_move_legal(map_grid, x, y):
                    map_grid[x][y] = sign_to_draw(current_direction)
                else:
                    x = x_old
                    y = y_old
                    break

        else:
            current_direction = position_change(step, current_direction)

    return (x, y, current_direction)


if __name__ == "__main__":
    rows, cols = (200, 150)
    # rows, cols = (12, 16)
    rows_count = 0
    map_grid = [[" " for i in range(cols)] for j in range(rows)]
    steps_list = []
    for line in FileReader().gen_file_reader("day_22.txt"):
        if ("R" in line) or ("L" in line):
            reg_expression = re.findall(REG_EXP, line)
            for item in reg_expression:
                steps_list.append(int(item[0]))
                steps_list.append(item[1])
            steps_list.append(int(line.rstrip()[-1:]))
        elif line == "\n":
            pass
        else:
            for i in range(cols):
                try:
                    if line[i] == "\n":
                        map_grid[rows_count][i] = " "
                    else:
                        map_grid[rows_count][i] = line[i]
                except:
                    pass
            rows_count += 1

    for j in range(len(map_grid[0])):
        if map_grid[0][j] == ".":
            starting_point = (0, j)
            break

    x, y, current_direction = monkey_move(steps_list, map_grid, rows, cols, starting_point)
    final_row = x + 1
    final_col = y + 1
    position_count = {"R": 0, "L": 2, "D": 1, "U": 3}
    final_result = 1000 * final_row + 4 * final_col + position_count[current_direction]
    print(f"x, y last coordinate = {x + 1}, {y + 1}, current_direction = {current_direction} ")
    createMap(map_grid, rows, cols)
    print(f"Final result = {final_result} ")
