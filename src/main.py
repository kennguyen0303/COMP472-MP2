"""
Something
"""
from input_parser import InputParser, StateExtractor
from search_tree import move_up, move_down, move_horizontal


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

    INPUT = "BBIJ....IJCCG.IAAM.DDK.M.H.KL..HFFL."
    extractor = StateExtractor(INPUT)
    # possible moves
    extractor.print_curr_layout()
    moving_res = move_horizontal(extractor, "D", -1)
    ext = StateExtractor(moving_res[0], moving_res[1])
    ext.print_curr_layout()

    print(ext.get_fuels())
    ext.set_fuel_for_vehicles("B3 A23 C77")
    print(ext.get_fuels())
