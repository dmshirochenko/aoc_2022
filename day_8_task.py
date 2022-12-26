# https://adventofcode.com/2022/day/8


class TreesMap:
    def __init__(self):
        pass

    def _gen_file_reader(self, file_name):
        try:
            file = open(file_name, "r")
            for row in file:
                yield row
        finally:
            file.close()

    def map_builder(self, file_name):
        trees_map_array = []
        for line in self._gen_file_reader(file_name):
            row_of_tree_to_add = []
            for tree in line.rstrip():
                row_of_tree_to_add.append(tree)
            trees_map_array.append(row_of_tree_to_add)

        return trees_map_array

    def _row_of_the_trees_depends_on_direction(self, side_to_check, trees_map_array, i, j):
        list_of_trees = []
        count_trees = 1
        if side_to_check == "up":
            while (i - count_trees) >= 0:
                tree_to_add = trees_map_array[i - count_trees][j]
                list_of_trees.append(tree_to_add)
                count_trees += 1
        if side_to_check == "bottom":
            while len(trees_map_array) - 1 >= i + count_trees:
                tree_to_add = trees_map_array[i + count_trees][j]
                list_of_trees.append(tree_to_add)
                count_trees += 1
        if side_to_check == "left":
            while (j - count_trees) >= 0:
                tree_to_add = trees_map_array[i][j - count_trees]
                list_of_trees.append(tree_to_add)
                count_trees += 1
        if side_to_check == "right":
            while len(trees_map_array[0]) - 1 >= j + count_trees:
                tree_to_add = trees_map_array[i][j + count_trees]
                list_of_trees.append(tree_to_add)
                count_trees += 1

        print(f"row of trees {side_to_check}, {list_of_trees}")
        return list_of_trees

    def _compare_number_within_list(self, tree, row_trees):
        for tree_in_row in row_trees:
            if tree_in_row >= tree:
                return False
        return True

    def _count_visible_trees(self, tree, row_trees):
        count_of_visible_trees = 0
        for tree_in_row in row_trees:
            if int(tree) > int(tree_in_row):
                count_of_visible_trees += 1
            else:
                count_of_visible_trees += 1
                return count_of_visible_trees

        return count_of_visible_trees

    def find_visible_trees(self, trees_map_array):
        visible_trees = 0
        for i in range(1, len(trees_map_array[0]) - 1):  # i row number, j column number
            for j in range(1, len(trees_map_array) - 1):
                print("Current tree = ", trees_map_array[i][j])
                if self._compare_number_within_list(
                    trees_map_array[i][j], self._row_of_the_trees_depends_on_direction("up", trees_map_array, i, j)
                ):  # check up
                    print("tree is visible = ", trees_map_array[i][j])
                    visible_trees += 1
                    continue
                elif self._compare_number_within_list(
                    trees_map_array[i][j], self._row_of_the_trees_depends_on_direction("bottom", trees_map_array, i, j)
                ):  # check bottom
                    print("tree is visible = ", trees_map_array[i][j])
                    visible_trees += 1
                    continue
                elif self._compare_number_within_list(
                    trees_map_array[i][j], self._row_of_the_trees_depends_on_direction("left", trees_map_array, i, j)
                ):  # check left
                    print("tree is visible = ", trees_map_array[i][j])
                    visible_trees += 1
                    continue
                elif self._compare_number_within_list(
                    trees_map_array[i][j], self._row_of_the_trees_depends_on_direction("right", trees_map_array, i, j)
                ):  # check right
                    print("tree is visible = ", trees_map_array[i][j])
                    visible_trees += 1
                    continue

        print("Visible trees before exterior = ", visible_trees)
        exterior_trees = 2 * len(trees_map_array[0]) + 2 * len(trees_map_array) - 4
        print(exterior_trees)
        visible_trees += exterior_trees
        return visible_trees

    def best_visible_spot(self, trees_map_array):
        max_visibility = 0
        for i in range(1, len(trees_map_array[0]) - 1):  # i row number, j column number
            for j in range(1, len(trees_map_array) - 1):
                print("Current tree = ", trees_map_array[i][j])
                visible_trees_from_up = self._count_visible_trees(
                    trees_map_array[i][j], self._row_of_the_trees_depends_on_direction("up", trees_map_array, i, j)
                )
                visible_trees_from_bottom = self._count_visible_trees(
                    trees_map_array[i][j], self._row_of_the_trees_depends_on_direction("bottom", trees_map_array, i, j)
                )
                visible_trees_from_left = self._count_visible_trees(
                    trees_map_array[i][j], self._row_of_the_trees_depends_on_direction("left", trees_map_array, i, j)
                )
                visible_trees_from_rigth = self._count_visible_trees(
                    trees_map_array[i][j], self._row_of_the_trees_depends_on_direction("right", trees_map_array, i, j)
                )
                print(
                    f"for tree {trees_map_array[i][j]}, up {visible_trees_from_up}, bottom {visible_trees_from_bottom}, left {visible_trees_from_left}, right {visible_trees_from_rigth}"
                )
                tree_visibility = (
                    visible_trees_from_up
                    * visible_trees_from_bottom
                    * visible_trees_from_left
                    * visible_trees_from_rigth
                )

                if tree_visibility > max_visibility:
                    max_visibility = tree_visibility

        return max_visibility


if __name__ == "__main__":
    tree_map_instance = TreesMap()
    map = tree_map_instance.map_builder("day_8.txt")
    print("Visible trees =", tree_map_instance.find_visible_trees(map))
    print("Max visibility =", tree_map_instance.best_visible_spot(map))
