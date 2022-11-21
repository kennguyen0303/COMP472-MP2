from src.search_tree import move_up, move_down, move_horizontal
from src.input_parser import StateExtractor


def test_move_up():
    INPUT = "BBIJ....IJCC..IAAMGDDK.MGH.KL.GHFFL. G3"
    EXPECTED_OUTPUT = "BBIJ..G.IJCCG.IAAMGDDK.M.H.KL..HFFL."
    EXPECTED_FUEL_UPDATE = "G1"
    extractor = StateExtractor(INPUT)
    valid_new_state = move_up(extractor, "G", 2)
    invalid_new_state = move_up(extractor, "G", 4)
    assert EXPECTED_OUTPUT == valid_new_state[0]
    assert EXPECTED_FUEL_UPDATE == valid_new_state[1]
    assert ("","") == invalid_new_state


def test_move_down():
    EXPECTED_OUTPUT = "BBIJ....IJCC..IAAMGDDK.MGH.KL.GHFFL."
    EXPECTED_FUEL_UPDATE = "G98"
    INPUT = "BBIJ..G.IJCCG.IAAMGDDK.M.H.KL..HFFL."
    extractor = StateExtractor(INPUT)
    new_state = move_down(extractor, "G", 2)
    assert EXPECTED_OUTPUT == new_state[0]
    assert EXPECTED_FUEL_UPDATE == new_state[1]


def test_move_horizontal():
    INPUT = "BBIJ..G.IJCCG.IAAM.DDK.M.H.KL..HFFL."
    EXPECTED_INVALID_OUTPUT = ("","")
    EXPECTED_VALID_OUTPUT = "BBIJ..G.IJCCG.IAAMDD.K.M.H.KL..HFFL."
    extractor = StateExtractor(INPUT)
    # G cannot move horizontally
    # D is blocked on its right
    invalid_states = [
        move_horizontal(extractor, "G", 2),
        move_horizontal(extractor, "D", 1),
    ]
    for state in invalid_states:
        assert EXPECTED_INVALID_OUTPUT == state

    # possible moves
    move_d_left_by_1_state, move_d_left_by_1_fuel_update = move_horizontal(
        extractor, "D", -1
    )
    assert EXPECTED_VALID_OUTPUT == move_d_left_by_1_state
    assert "D99" == move_d_left_by_1_fuel_update

    # move back to right by 1
    new_extractor = StateExtractor(move_d_left_by_1_state, move_d_left_by_1_fuel_update)
    print(new_extractor.get_fuels())
    move_d_right_by_1_state, move_d_right_by_1_fuel_update = move_horizontal(
        new_extractor, "D", 1
    )
    assert INPUT == move_d_right_by_1_state
    assert "D98" == move_d_right_by_1_fuel_update
