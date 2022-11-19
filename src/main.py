"""
Something
"""
from input_parser import InputParser, StateExtractor


class Node:
    """
    asd
    """

    def __init__(self, val: int) -> None:
        """
        something
        """
        self.val = val


if __name__ == "__main__":
    FILE_PATH = "./tests/Resources/sample-input.txt"
    INPUTS = InputParser.parse(FILE_PATH)
    extractor = StateExtractor(INPUTS[3])
    extractor.collect_vehicles()
    print(extractor.vehicles["J"])
    print(extractor.vehicles["B"])
