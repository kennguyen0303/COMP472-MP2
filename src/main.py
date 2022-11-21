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

    INPUT = "..I.KLBBI.KLGAADD.GH....GH.JEEFF.J.. K99 H99 A99 L98 D98"
    extractor = StateExtractor(INPUT)
    # possible moves
    extractor.print_curr_layout()
    new_move_res = move_horizontal(extractor, 'D', 1)
    new_ext = StateExtractor(new_move_res[0],new_move_res[1])
    new_ext.print_curr_layout()
    print(new_ext.get_curr_layout_str())
