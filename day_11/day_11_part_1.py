import argparse
import itertools
import numpy as np
from time import time
from typing import List, Tuple


class SeatLayout:
    def __init__(self, initial_layout: str):
        self.grid = np.array([list(line) for line in initial_layout.split("\n")])
        self.xmin = 0
        self.xmax = self.grid.shape[0] - 1
        self.ymin = 0
        self.ymax = self.grid.shape[1] - 1
        self.occupied_count_threshold = 4

    def apply_until_convergence(self):
        start_time = time()
        new_grid = self.evolve_grid()
        round_count: int = 0
        while not np.array_equal(new_grid, self.grid):
            round_count += 1
            self.grid = new_grid
            new_grid = self.evolve_grid()
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
                occupied_count = self.adjacent_occupied_count(i, j)
                # rule for seat to become occupied
                if current_value == "L" and occupied_count == 0:
                    new_grid[i, j] = "#"
                # rule for seat to become vacant
                if current_value == "#" and occupied_count >= self.occupied_count_threshold:
                    new_grid[i, j] = "L"
        return new_grid

    def adjacent_indices(self, i: int, j: int) -> List[Tuple[int, int]]:
        if not ((self.xmin <= i <= self.xmax) and (self.ymin <= j <= self.ymax)):
            raise ValueError(f"Invalid starting index tuple ({i}, {j})")
        return [
            index_tuple
            for index_tuple in itertools.product([i - 1, i, i + 1], [j - 1, j, j + 1])
            if index_tuple != (i, j)
            and self.xmin <= index_tuple[0] <= self.xmax
            and self.ymin <= index_tuple[1] <= self.ymax
        ]

    def adjacent_values(self, i: int, j: int) -> List[str]:
        adjacent_indices = self.adjacent_indices(i, j)
        return self.grid[tuple(zip(*adjacent_indices))]

    def adjacent_occupied_count(self, i: int, j: int) -> int:
        adjacent_indices = self.adjacent_indices(i, j)
        occupied_count = 0
        for adjacent_index in adjacent_indices:
            if occupied_count >= self.occupied_count_threshold:
                return occupied_count
            if self.grid[adjacent_index] == "#":
                occupied_count += 1
        return occupied_count

    def count_occupied(self) -> int:
        return np.count_nonzero(self.grid == "#")

    def to_string(self) -> str:
        return "\n".join(["".join(row) for row in self.grid])


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
