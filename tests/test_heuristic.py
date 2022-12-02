"""
Module for tests for heuristic calculation
"""
from search_algos import calculate_heuristic_1


def test_heuristic_1():
    """
    test heuristic 1
    """
    INPUTS = [
        "BBIJ....IJCC..IAAMGDDK.MGH.KL.GHFFL.",
        "BBIJ....IJCCAAI..MGDDK.MGH.KL.GHFFL.",
    ]
    OUTPUTS = [1, 2]
    for idx, input in enumerate(INPUTS):
        assert calculate_heuristic_1(input) == OUTPUTS[idx]
