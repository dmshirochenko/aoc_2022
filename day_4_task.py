# https://adventofcode.com/2022/day/4


class ElvWorkOverlap:
    def __init__(self):
        pass

    def _gen_file_reader(self, file_name):
        try:
            file = open(file_name, "r")
            for row in file:
                yield row
        finally:
            file.close()

    def _file_log_writer(self, file_name, message):
        with open(file_name, "a") as file:
            file.write(message)
            file.write("\n")

    def overlap_finder_full(self, file_name):
        count_full_overlaps = 0
        for line in self._gen_file_reader(file_name):
            shift_list = line.rstrip().split(",")
            shift_one = [int(n) for n in shift_list[0].split("-")]
            shift_two = [int(n) for n in shift_list[1].split("-")]
            if (shift_one[0] <= shift_two[0]) and (shift_one[1] >= shift_two[1]):
                self._file_log_writer("day_4_logs.txt", "Overlap was found, second shift full intersection\n")
                count_full_overlaps += 1
            elif (shift_two[0] <= shift_one[0]) and (shift_two[1] >= shift_one[1]):
                self._file_log_writer("day_4_logs.txt", "Overlap was found, first shift full intersection\n")
                count_full_overlaps += 1

        return count_full_overlaps

    def overlap_finder_at_least_one(self, file_name):
        count_no_overlaps = 0
        count_all_lines = 0
        for line in self._gen_file_reader(file_name):
            shift_list = line.rstrip().split(",")
            count_all_lines += 1
            shift_one = [int(n) for n in shift_list[0].split("-")]
            shift_two = [int(n) for n in shift_list[1].split("-")]
            # count no overlaps
            if shift_one[0] > shift_two[1]:
                count_no_overlaps += 1
            elif shift_one[1] < shift_two[0]:
                count_no_overlaps += 1

        return count_all_lines - count_no_overlaps


if __name__ == "__main__":
    overlap_instance = ElvWorkOverlap()
    count_full_overlaps = overlap_instance.overlap_finder_full("day_4.txt")
    print(f"Full overlaps {count_full_overlaps}")
    count_at_least_one_overlap = overlap_instance.overlap_finder_at_least_one("day_4.txt")
    print(count_at_least_one_overlap)
    # You guessed 736 too low
