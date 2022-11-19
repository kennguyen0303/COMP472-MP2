from src.search_tree import move_up, move_down
from src.input_parser import StateExtractor


def test_move_up():
    INPUT = "BBIJ....IJCC..IAAMGDDK.MGH.KL.GHFFL. G3"
    EXPECTED_OUTPUT = "BBIJ..G.IJCCG.IAAMGDDK.M.H.KL..HFFL."
    extractor = StateExtractor(INPUT)
    extractor.collect_vehicles()
    vehicle_G = extractor.vehicles["G"]
    valid_new_state = move_up(extractor, vehicle_G, 2)
    invalid_new_state = move_up(extractor, vehicle_G, 4)
    assert EXPECTED_OUTPUT == valid_new_state
    assert "" == invalid_new_state


def test_move_down():
    EXPECTED_OUTPUT = "BBIJ....IJCC..IAAMGDDK.MGH.KL.GHFFL."
    INPUT = "BBIJ..G.IJCCG.IAAMGDDK.M.H.KL..HFFL."
    extractor = StateExtractor(INPUT)
    extractor.collect_vehicles()
    vehicle_G = extractor.vehicles["G"]
    new_state = move_down(extractor, vehicle_G, 2)
    assert EXPECTED_OUTPUT == new_state
