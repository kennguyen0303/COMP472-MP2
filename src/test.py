"""
Something
"""
from input_parser import InputParser, StateExtractor

if __name__ == "__main__":
    FILE_PATH = "/home/n_thekie/Desktop/school/comp 472/COMP472-MP2/Sample/sample-input copy.txt"
    INPUTS = InputParser.parse(FILE_PATH)
    for idx, input_str in enumerate(INPUTS):
        print("\n-------- NEW INPUT--------\n")
        StateExtractor(input_str).print_curr_layout()
