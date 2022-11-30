"""
Sample test
"""

from src.input_parser import InputParser, StateExtractor, Vehicle, MovingDirection


def test_parsing_input():
    """
    test parsing input
    """
    EXPECTED_OUTPUTS = [
        "BBIJ....IJCC..IAAMGDDK.MGH.KL.GHFFL.",
        "..I...BBI.K.GHAAKLGHDDKLG..JEEFF.J..",
        "JBBCCCJDD..MJAAL.MFFKL.N..KGGN.HH...",
        "BBB..MCCDD.MAAKL.MJ.KLEEJ.GG..JHHHII J0 B4",
        "IJBBCCIJDDL.IJAAL.EEK.L...KFF..GGHH. F0 G6",
        "BB.G.HE..G.HEAAG.I..FCCIDDF..I..F...",
    ]
    FILE_PATH = "tests/Resources/sample-input.txt"
    outputs = InputParser.parse(FILE_PATH)
    for i, output in enumerate(outputs):
        assert output == EXPECTED_OUTPUTS[i]


def test_convert_to_array():
    FILE_PATH = "./tests/Resources/small-sample-input.txt"
    EXPECTED_RESULT = [
        ["A", "."],
        ["A", "."],
    ]
    INPUTS = InputParser.parse(FILE_PATH)
    extractor = StateExtractor(INPUTS[0], size=2)
    for i, output in enumerate(extractor.convert_to_array()):
        assert output == EXPECTED_RESULT[i]


# @pytest.mark.skip(reason="no way of currently testing this")
def test_collect_vehicles():
    FILE_PATH = "./tests/Resources/sample-input.txt"
    EXPECTED_VEHICLE = Vehicle("A", (2, 4), 2, MovingDirection.HORIZONTAL, fuel=100)
    INPUTS = InputParser.parse(FILE_PATH)
    extractor = StateExtractor(INPUTS[0])
    extractor.collect_vehicles()
    print(extractor.vehicles["J"])
    for veh in extractor.vehicles.values():
        if veh.name == "A":
            assert veh.last_point_loc == EXPECTED_VEHICLE.last_point_loc
            assert veh.fuel == EXPECTED_VEHICLE.fuel
            assert veh.size == EXPECTED_VEHICLE.size
