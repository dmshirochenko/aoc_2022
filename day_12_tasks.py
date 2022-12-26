# https://adventofcode.com/2022/day/12

import string
import queue

CHAR_SCORE_MAP = {c: i for i, c in enumerate(string.ascii_lowercase)}
MOVES = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def find_source_index(grid):
    for row_idx, l in enumerate(grid):
        for col_idx, c in enumerate(l):
            if c == "S":
                return ((row_idx, col_idx), 0)


def find_source_all_a_indexs(grid):
    list_of_a_indexs = []
    for row_idx, l in enumerate(grid):
        for col_idx, c in enumerate(l):
            if c == "S" or c == "a":
                list_of_a_indexs.append(((row_idx, col_idx), 0))

    return list_of_a_indexs


def movement_check(grid, current_value, dest_row, dest_col):
    if dest_row < 0 or dest_col < 0 or dest_row >= len(grid) or dest_col >= len(grid[0]):
        return False

    if current_value == "S":
        current_value = "a"

    dest_value = grid[dest_row][dest_col]

    if dest_value == "E":
        dest_value = "z"

    if dest_value == "S":
        dest_value = "a"

    return CHAR_SCORE_MAP[dest_value] <= CHAR_SCORE_MAP[current_value] + 1


def breadth_first_search(grid, source_index):
    queue_path = queue.Queue()
    queue_path.put(source_index)
    seen_indexs = set()
    seen_indexs.add(source_index[0])
    while not queue_path.empty():
        (current_row, current_col), step_till_node = queue_path.get()
        current_value = grid[current_row][current_col]
        # print("Current value = ", current_value)

        if current_value == "E":
            return (current_row, current_col), step_till_node

        for i, j in MOVES:
            new_coord = (current_row + i, current_col + j)
            if (new_coord not in seen_indexs) and movement_check(grid, current_value, new_coord[0], new_coord[1]):
                node_to_add_to_queue = ((new_coord), step_till_node + 1)
                queue_path.put(node_to_add_to_queue)
                seen_indexs.add(new_coord)


def part_one(grid):
    source_index = find_source_index(grid)
    (current_row, current_col), step_till_node = breadth_first_search(grid, source_index)
    print(f"Minimum steps = ", step_till_node)


def part_two(grid):
    steps_list = []
    list_start_positions = find_source_all_a_indexs(grid)
    for positions in list_start_positions:
        returned_node = breadth_first_search(grid, positions)
        if returned_node:
            steps_list.append(returned_node[1])

    steps_list.sort()
    print(f"Minimum steps = ", steps_list[0])


if __name__ == "__main__":
    with open("day_12.txt", "r") as f:
        grid = [l.strip() for l in f.readlines()]

    part_one(grid)
    part_two(grid)
