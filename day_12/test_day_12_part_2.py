import pytest
import day_12_part_2 as sut


@pytest.fixture
def instructions():
    return """F10
N3
F7
R90
F11"""


def test_ship_navigator__apply_instructions(instructions):
    navigator = sut.ShipNavigator(instructions)
    navigator.apply_instructions()
    assert (navigator.x, navigator.y) == (214, -72)


def test_ship_navigator__manhattan_distance(instructions):
    navigator = sut.ShipNavigator(instructions)
    navigator.apply_instructions()
    assert navigator.manhattan_distance() == 286

