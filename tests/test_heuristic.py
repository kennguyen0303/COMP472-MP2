"""
Module for tests for heuristic calculation
"""
from search_algos import (
    calculate_heuristic_1,
    calculate_heuristic_2,
    calculate_heuristic_3,
    calculate_heuristic_4,
)


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


def test_heuristic_2():
    """
    test heuristic 2
    """
    INPUTS = [
        "BBIJ....IJCC..IAAMGDDK.MGH.KL.GHFFL.",
        "BBIJ....IJCCAAI..MGDDK.MGH.KL.GHFFL.",
    ]
    OUTPUTS = [1, 2]
    for idx, input in enumerate(INPUTS):
        assert calculate_heuristic_2(input) == OUTPUTS[idx]


def test_heuristic_3():
    """
    test heuristic 3
    """
    INPUTS = [
        "BBIJ....IJCC..IAAMGDDK.MGH.KL.GHFFL.",
        "BBIJ....IJCCAAI..MGDDK.MGH.KL.GHFFL.",
    ]
    OUTPUTS = [5, 10]
    for idx, input in enumerate(INPUTS):
        assert calculate_heuristic_3(input) == OUTPUTS[idx]


def test_heuristic_4():
    """
    test heuristic 4
    """
    INPUTS = [
        "BBIJ....IJCC..IAAMGDDK.MGH.KL.GHFFL.",
        "BBIJ....IJCCAAI..MGDDK.MGH.KL.GHFFL.",
    ]
    OUTPUTS = [1, 2]
    for idx, input in enumerate(INPUTS):
        assert calculate_heuristic_4(input) == OUTPUTS[idx]
