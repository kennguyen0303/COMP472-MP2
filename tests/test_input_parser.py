"""
Sample test
"""

from src.input_parser import InputParser


def test_parsing_input():
    """
    test parsing input
    """
    parser = InputParser()
    expected_outputs = [
        "BBIJ....IJCC..IAAMGDDK.MGH.KL.GHFFL.",
        "..I...BBI.K.GHAAKLGHDDKLG..JEEFF.J..",
        "JBBCCCJDD..MJAAL.MFFKL.N..KGGN.HH...",
        "BBB..MCCDD.MAAKL.MJ.KLEEJ.GG..JHHHII J0 B4",
        "IJBBCCIJDDL.IJAAL.EEK.L...KFF..GGHH. F0 G6",
        "BB.G.HE..G.HEAAG.I..FCCIDDF..I..F...",
    ]
    filepath = "tests/Resources/sample-input.txt"
    outputs = parser.parse(filepath)
    for i, output in enumerate(outputs):
        assert output == expected_outputs[i]
