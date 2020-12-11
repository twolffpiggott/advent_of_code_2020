import argparse
import numpy as np
from collections.abc import Iterator
from time import time


class SeatLayout:
    def __init__(self, initial_layout: str):
        self.grid = np.array([list(line) for line in initial_layout.split("\n")])
        self.xmin = 0
        self.xmax = self.grid.shape[0] - 1
        self.ymin = 0
        self.ymax = self.grid.shape[1] - 1
        self.occupied_count_threshold = 5

    def apply_until_convergence(self):
        start_time = time()
        new_grid = self.evolve_grid()
        round_count: int = 0
        while not np.array_equal(new_grid, self.grid):
            round_count += 1
            self.grid = new_grid
            new_grid = self.evolve_grid()
            print(f"Applied {round_count} round(s)")
        end_time = time()
        print(
            f"Grid converged after {round_count} rounds in {end_time - start_time:.2f} seconds"
        )

    def apply_round(self):
        new_grid = self.evolve_grid()
        self.grid = new_grid

    def evolve_grid(self) -> np.ndarray:
        new_grid: np.ndarray = self.grid.copy()
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                current_value: str = self.grid[i, j]
                # exclude floor cells
                if current_value == ".":
                    continue
                occupied_count = self.visible_occupied_count(i, j)
                # rule for seat to become occupied
                if current_value == "L" and occupied_count == 0:
                    new_grid[i, j] = "#"
                # rule for seat to become vacant
                if (
                    current_value == "#"
                    and occupied_count >= self.occupied_count_threshold
                ):
                    new_grid[i, j] = "L"
        return new_grid

    def visible_occupied_count(self, i: int, j: int) -> int:
        occupied_count = 0
        for path in [
            gen_left,
            gen_right,
            gen_down,
            gen_up,
            gen_left_upper_diagonal,
            gen_left_lower_diagonal,
            gen_right_upper_diagonal,
            gen_right_lower_diagonal
        ]:
            occupied_increment = self.search_path(path(i, j))
            occupied_count += occupied_increment
            if occupied_count >= self.occupied_count_threshold:
                return occupied_count
        return occupied_count

    def search_path(self, gen: Iterator) -> int:
        while True:
            i_new, j_new = next(gen)
            # catch case of special meaning of "-1" index
            if not (i_new >= 0 and j_new >= 0):
                return 0
            try:
                current_value = self.grid[i_new, j_new]
            except IndexError:
                return 0
            else:
                if current_value == "#":
                    return 1
                if current_value == "L":
                    return 0

    def count_occupied(self) -> int:
        return np.count_nonzero(self.grid == "#")

    def to_string(self) -> str:
        return "\n".join(["".join(row) for row in self.grid])


def gen_left(i: int, j: int):
    i_current = i
    while True:
        i_current -= 1
        yield i_current, j


def gen_right(i: int, j: int):
    i_current = i
    while True:
        i_current += 1
        yield i_current, j


def gen_up(i: int, j: int):
    j_current = j
    while True:
        j_current += 1
        yield i, j_current


def gen_down(i: int, j: int):
    j_current = j
    while True:
        j_current -= 1
        yield i, j_current


def gen_left_upper_diagonal(i: int, j: int):
    i_current = i
    j_current = j
    while True:
        i_current -= 1
        j_current += 1
        yield i_current, j_current


def gen_left_lower_diagonal(i: int, j: int):
    i_current = i
    j_current = j
    while True:
        i_current -= 1
        j_current -= 1
        yield i_current, j_current


def gen_right_upper_diagonal(i: int, j: int):
    i_current = i
    j_current = j
    while True:
        i_current += 1
        j_current += 1
        yield i_current, j_current


def gen_right_lower_diagonal(i: int, j: int):
    i_current = i
    j_current = j
    while True:
        i_current += 1
        j_current -= 1
        yield i_current, j_current


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_txt_file", type=str, help="Path to text file of initial grid layout."
    )
    args = parser.parse_args()
    with open(args.input_txt_file, "r") as f:
        layout_string = f.read()
    seat_layout = SeatLayout(layout_string)
    seat_layout.apply_until_convergence()
    print(seat_layout.count_occupied())
