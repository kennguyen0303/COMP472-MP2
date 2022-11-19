"""
Something
"""
from input_parser import InputParser, StateExtractor
from search_tree import move_up, move_down


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
    # FILE_PATH = "./tests/Resources/sample-input.txt"
    # INPUTS = InputParser.parse(FILE_PATH)
    # extractor = StateExtractor(INPUTS[3])
    # extractor.collect_vehicles()
    # print(extractor.vehicles["J"])
    # print(extractor.vehicles["B"])
    # print(extractor.convert_to_array())

    INPUT = "BBIJ....IJCC..IAAMGDDK.MGH.KL.GHFFL."
    extractor = StateExtractor(INPUT)
    extractor.collect_vehicles()
    vehicle_M = extractor.vehicles["M"]
    new_state = move_down(extractor, vehicle_M, 1)
    extractor.print_curr_layout()
    extractor2 = StateExtractor(new_state)
    print("---")
    extractor2.print_curr_layout()
