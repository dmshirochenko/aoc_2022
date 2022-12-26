# https://adventofcode.com/2022/day/2


class RockPapperScissors:
    def __init__(self):
        self.mapping_dict = {"A": "Rock", "B": "Paper", "C": "Scissors", "X": "Rock", "Y": "Paper", "Z": "Scissors"}
        self.choose_points_dict = {"Rock": 1, "Paper": 2, "Scissors": 3}
        self.lose_win_points_dict = {"Win": 6, "Draw": 3, "Lose": 0}
        self.mapping_dict_game_2 = {"A": "Rock", "B": "Paper", "C": "Scissors", "X": "Lose", "Y": "Draw", "Z": "Win"}
        self.result_variants = ["Rock", "Paper", "Scissors"]

    def _gen_file_reader(self, file_name):
        for row in open(file_name, "r"):
            yield row

    def gen_count_game_points(self, file_name):
        total_points = 0
        for row in self._gen_file_reader(file_name):
            line_to_count = row.rstrip().rsplit(" ")
            elf_result = self.mapping_dict[line_to_count[0]]
            user_result = self.mapping_dict[line_to_count[1]]
            points_received, game_result = self._game_logic(elf_result, user_result)
            total_points += points_received

        return total_points

    def gen_count_game_points_2(self, file_name):
        total_points = 0
        for row in self._gen_file_reader(file_name):
            line_to_count = row.rstrip().rsplit(" ")
            elf_choise = self.mapping_dict_game_2[line_to_count[0]]
            user_game_result = self.mapping_dict_game_2[line_to_count[1]]
            for user_choice in self.result_variants:
                points_received, game_result = self._game_logic(elf_choise, user_choice)
                if game_result == user_game_result:
                    total_points += points_received

        return total_points

    def _game_logic(self, elf_result, user_result):
        if elf_result == user_result:  # Draw
            print(f"Both players selected {user_result}. It's a tie!")
            return (self.choose_points_dict[user_result] + self.lose_win_points_dict["Draw"], "Draw")
        elif user_result == "Rock":
            if elf_result == "Scissors":  # Win
                print("Rock smashes scissors! You win!")
                return (self.choose_points_dict[user_result] + self.lose_win_points_dict["Win"], "Win")
            else:  # Lose
                print("Paper covers rock! You lose.")
                return (self.choose_points_dict[user_result] + self.lose_win_points_dict["Lose"], "Lose")
        elif user_result == "Paper":
            if elf_result == "Rock":  # Win
                print("Paper covers rock! You win!")
                return (self.choose_points_dict[user_result] + self.lose_win_points_dict["Win"], "Win")
            else:  # Lose
                print("Scissors cuts paper! You lose.")
                return (self.choose_points_dict[user_result] + self.lose_win_points_dict["Lose"], "Lose")
        elif user_result == "Scissors":
            if elf_result == "Paper":  # Win
                print("Scissors cuts paper! You win!")
                return (self.choose_points_dict[user_result] + self.lose_win_points_dict["Win"], "Win")
            else:  # Lose
                print("Rock smashes scissors! You lose.")
                return (self.choose_points_dict[user_result] + self.lose_win_points_dict["Lose"], "Lose")


if __name__ == "__main__":
    game_instance = RockPapperScissors()
    total_ponits = game_instance.gen_count_game_points("day_2.txt")
    total_ponits_game_2 = game_instance.gen_count_game_points_2("day_2.txt")
    print(total_ponits)
    print(total_ponits_game_2)
    # right answer 9651
