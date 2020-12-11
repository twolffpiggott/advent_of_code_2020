import pytest
import day_11_part_1 as sut


@pytest.fixture
def layout_0():
    return """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""


@pytest.fixture
def layout_1():
    return """#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##"""


@pytest.fixture
def layout_2():
    return """#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##"""


@pytest.fixture
def layout_3():
    return """#.##.L#.##
#L###LL.L#
L.#.#..#..
#L##.##.L#
#.##.LL.LL
#.###L#.##
..#.#.....
#L######L#
#.LL###L.L
#.#L###.##"""


@pytest.fixture
def layout_4():
    return """#.#L.L#.##
#LLL#LL.L#
L.L.L..#..
#LLL.##.L#
#.LL.LL.LL
#.LL#L#.##
..L.L.....
#L#LLLL#L#
#.LLLLLL.L
#.#L#L#.##"""


@pytest.fixture
def layout_5():
    return """#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##"""


def test_seat_layout__apply_round(
    layout_0, layout_1, layout_2, layout_3, layout_4, layout_5
):
    seat_layout = sut.SeatLayout(layout_0)
    assert seat_layout.to_string() == layout_0
    for grid in [layout_1, layout_2, layout_3, layout_4, layout_5]:
        seat_layout.apply_round()
        assert seat_layout.to_string() == grid


def test_seat_layout__apply_until_convergence(layout_0, capsys):
    seat_layout = sut.SeatLayout(layout_0)
    seat_layout.apply_until_convergence()
    out, _ = capsys.readouterr()
    assert "Grid converged after 5 rounds" in out


def test_seat_layout__count_occupied(layout_0):
    seat_layout = sut.SeatLayout(layout_0)
    seat_layout.apply_until_convergence()
    assert seat_layout.count_occupied() == 37
