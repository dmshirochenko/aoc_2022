# https://adventofcode.com/2022/day/18


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


def count_surface(list_of_cubes):
    surface_area = 0
    for cube in list_of_cubes:
        x, y, z = cube

        neighbor_num = 0
        possible_neighbors = [(x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)]

        for neighbor in possible_neighbors:
            if neighbor not in list_of_cubes:
                neighbor_num += 1

        surface_area += neighbor_num

    return surface_area


if __name__ == "__main__":
    file_reader_instance = FileReader()
    list_of_cubes = []
    surface_area = 0
    for line in file_reader_instance.gen_file_reader("day_18.txt"):
        x, y, z = line.rstrip().split(",")
        list_of_cubes.append((int(x), int(y), int(z)))

    print("Surface area = ", count_surface(list_of_cubes))
