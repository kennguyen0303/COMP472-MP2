"""
Something
"""
import random
from input_parser import InputParser, StateExtractor


def get_inputs_from_database(num_of_puzzles: int):
    """
    Get randomly the 50 inputs
    """
    result = {}  # 50 random inputs
    FILE_PATH = (
        "/home/n_thekie/Desktop/school/comp 472/COMP472-MP2/Sample/random_inputs.txt"
    )
    with open(FILE_PATH, mode="r", encoding="utf-8") as f_handler:
        lines = f_handler.readlines()
        # get randomly k puzzles
        puzzle_count = 0
        while puzzle_count < num_of_puzzles:
            row_location = random.randint(0, len(lines))
            if result.get(row_location) is None:
                line = list(lines[row_location].split(" ")[1])
                for idx, char in enumerate(line):
                    if char == "o" or char == "x":
                        line[idx] = "."
                line.append("\n")
                result[row_location] = "".join(line)
                puzzle_count += 1

    data = list(result.values())
    with open("50-puzzles.txt", mode="w", encoding="utf-8") as f_handler:
        f_handler.writelines(data)


if __name__ == "__main__":
    get_inputs_from_database(50)
