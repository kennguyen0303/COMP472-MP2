from src.search_algos import UCS


def test_ucs():
    INPUT = "BBIJ....IJCC..IAAMGDDK.MGH.KL.GHFFL."
    ucs = UCS()
    ucs.search_ucs(INPUT)
    assert ucs.is_final_state_reached == True
