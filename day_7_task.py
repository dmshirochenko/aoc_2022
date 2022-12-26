MAX_SIZE = 70000000


class FileReader:
    def __init__(self):
        pass

    def _gen_file_reader(self, file_name):
        try:
            file = open(file_name, "r")
            for row in file:
                yield row
        finally:
            file.close()

    def read_file_to_list(self, file_name):
        lines = []
        for line in self._gen_file_reader(file_name):
            lines.append(line.rstrip())

        return lines


class DirectoryTree:
    def __init__(self):
        self.directory_tree_dict = {"dir": True, "name": "/", "size": -1, "children": {}}
        self.current_path = []
        self.current_directory = self.directory_tree_dict

    def find_directory(self):
        current_directory = self.directory_tree_dict
        for path in self.current_path:
            current_directory = current_directory["children"][path]

        return current_directory

    def add_children(self, name, children):
        current_directory = self.find_directory()
        current_directory["children"][name] = children

    def path_modification_erase(self):
        self.current_path.pop()

    def path_modification_add(self, path_to_add):
        self.current_path.append(path_to_add)

    def calculate_dir_sizes_all(self, dir):
        if dir["size"] == -1:
            dir["size"] = sum([self.calculate_dir_sizes_all(dir["children"][child]) for child in dir["children"]])
        return dir["size"]


class DiskSpaceCounter:
    def __init__(self):
        pass

    def get_files_paths(self, commands_to_execute):
        command = commands_to_execute.pop(0)
        if command == "$ cd /":  # tree initialization
            directory_tree_instance = DirectoryTree()

        command = commands_to_execute.pop(0)

        while commands_to_execute:
            if command[2:] == "ls":
                while commands_to_execute:
                    command = commands_to_execute.pop(0)
                    if command[0] != "$":
                        size, name = command.split()
                        if size == "dir":  # check if it's dir
                            dir_to_add = {"dir": True, "name": name, "size": -1, "children": {}}
                            directory_tree_instance.add_children(name, dir_to_add)
                        else:
                            file_to_add = {"dir": False, "name": name, "size": int(size), "children": {}}
                            directory_tree_instance.add_children(name, file_to_add)
                    else:
                        break

            else:
                dir_name = command.split()[2]
                if dir_name == "..":
                    directory_tree_instance.path_modification_erase()
                else:
                    directory_tree_instance.path_modification_add(dir_name)

                command = commands_to_execute.pop(0)

        # calculate directories sizes
        directory_tree_instance.calculate_dir_sizes_all(directory_tree_instance.directory_tree_dict)
        return directory_tree_instance.directory_tree_dict

    def sum_size_less_than(self, dir, max_size):
        size = 0
        if not dir["dir"]:
            return 0
        if dir["size"] <= max_size:
            size += dir["size"]
        for d in dir["children"]:
            size += self.sum_size_less_than(dir["children"][d], max_size)
        return size

    def find_min_to_delete(self, dir, min_size):
        current_min = dir["size"] if dir["size"] >= min_size else MAX_SIZE
        children_min = [
            self.find_min_to_delete(dir["children"][child], min_size)
            for child in dir["children"]
            if dir["children"][child]["dir"]
        ]
        return min([current_min] + children_min)


if __name__ == "__main__":
    file_reader_instance = FileReader()
    disk_space_instance = DiskSpaceCounter()
    parsed_disk_path = disk_space_instance.get_files_paths(file_reader_instance.read_file_to_list("day_7.txt"))
    print("Size = ", disk_space_instance.sum_size_less_than(parsed_disk_path, 100000))
    min_size = parsed_disk_path["size"] - (MAX_SIZE - 30000000)
    print("Size =  ", disk_space_instance.find_min_to_delete(parsed_disk_path, min_size))
