"""
Sample test
"""

from src.main import Node


def func(obj: Node, val: int):
    """
    sample test method
    """
    return obj.val + val


def test_answer():
    """
    test node
    """
    obj = Node(3)
    assert func(obj, 3) == 5
