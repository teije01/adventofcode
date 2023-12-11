"""
https://adventofcode.com/2023/day/11
"""
import itertools as it
from dataclasses import dataclass
from io import StringIO

import numpy as np
from aocd.models import Puzzle


def min_max(*args):
    return min(args), max(*args)


@dataclass
class Galaxy:
    row: int
    col: int

    def shortest_manhattan_distance(
        self, other: "Galaxy", distance_arr: np.ndarray | None = None
    ):
        if distance_arr is None:
            return abs(other.row - self.row) + abs(other.col - self.col)
        distance = (
            distance_arr[slice(*min_max(self.row, other.row)), self.col].sum()
            + distance_arr[other.row, slice(*min_max(self.col, other.col))].sum()
        )
        return distance


def parse_input_data(input_data, empty_distance) -> tuple[np.ndarray, np.ndarray]:
    galaxy_str = StringIO(input_data.translate(str.maketrans(".#", "01")))
    galaxy_arr = np.genfromtxt(galaxy_str, dtype=int, delimiter=1).astype(bool)
    distance_arr = np.full_like(galaxy_arr, 1, dtype=int)
    empty_cols = np.where(np.logical_not(galaxy_arr.sum(axis=0)))[0]
    empty_rows = np.where(np.logical_not(galaxy_arr.sum(axis=1)))[0]
    galaxy_arr = np.insert(galaxy_arr, empty_cols, False, axis=1)
    distance_arr = np.insert(distance_arr, empty_cols, empty_distance, axis=1)
    galaxy_arr = np.insert(galaxy_arr, empty_rows, False, axis=0)
    distance_arr = np.insert(distance_arr, empty_rows, empty_distance, axis=0)
    return galaxy_arr, distance_arr


def part_1(input_data) -> int:
    galaxy_arr, distance_arr = parse_input_data(input_data, empty_distance=1)
    galaxies = list(it.starmap(Galaxy, zip(*np.where(galaxy_arr))))
    return sum(
        galaxy_1.shortest_manhattan_distance(galaxy_2)
        for galaxy_1, galaxy_2 in it.combinations(galaxies, 2)
    )


def part_2(input_data, empty_distance=999_999) -> int:
    galaxy_arr, distance_arr = parse_input_data(
        input_data, empty_distance=empty_distance
    )
    galaxies = list(it.starmap(Galaxy, zip(*np.where(galaxy_arr))))
    return sum(
        galaxy_1.shortest_manhattan_distance(galaxy_2, distance_arr)
        for galaxy_1, galaxy_2 in it.combinations(galaxies, 2)
    )


def main():
    puzzle = Puzzle(day=11, year=2023)

    (example,) = puzzle.examples
    assert part_1(example.input_data) == int(example.answer_a)
    assert part_2(example.input_data, empty_distance=9) == 1030
    assert part_2(example.input_data, empty_distance=99) == 8410

    input_data = puzzle.input_data
    puzzle.answer_a = part_1(input_data)
    puzzle.answer_b = part_2(input_data)
    print(f"{puzzle.answer_a=}, {puzzle.answer_b=}")


if __name__ == "__main__":
    main()
