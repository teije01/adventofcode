"""
https://adventofcode.com/2024/day/8
"""
from itertools import combinations, starmap
from collections import namedtuple

import numpy as np
from aocd.models import Puzzle

DOT = ord('.')

Loc = namedtuple("Loc", field_names=["row", "col"])


def get_anti_node_locs(city: np.ndarray, frequency: int, limit=True) -> list[Loc]:
    antenna_locations = starmap(Loc, zip(*np.where(city == frequency)))
    antinode_locs = []
    for ant_loc_1, ant_loc_2 in combinations(antenna_locations, 2):
        rowdif, coldif = (ant_loc_2.row - ant_loc_1.row), (ant_loc_2.col - ant_loc_1.col)
        if limit:
            shifts = [-1, 2]  # with respect to antenna 1
        else:
            row_range = (-int(ant_loc_1.row / rowdif), int((city.shape[0] - ant_loc_1.row) / rowdif))
            col_range = (-int(ant_loc_1.col / coldif), int((city.shape[1] - ant_loc_1.col) / coldif))
            shifts = range(max(min(row_range), min(col_range)), min(max(row_range), max(col_range)) + 1)
        antinode_locs.extend(
            [Loc(ant_loc_1.row + shift * rowdif, ant_loc_1.col + shift * coldif)
             for shift in shifts]
        )

    return antinode_locs


def get_anti_node_mask(city: np.ndarray, limit=True) -> np.ndarray:
    anti_node_mask = np.full_like(city, False, dtype=bool)
    anti_node_locs = []
    for frequency in np.setdiff1d(np.unique(city), DOT):
        anti_node_locs.extend(get_anti_node_locs(city, frequency, limit=limit))
    rows, cols = np.array(list(zip(*anti_node_locs)))
    valid = (rows > -1) & (cols > -1) & (rows < anti_node_mask.shape[0]) & (
                cols < anti_node_mask.shape[1])
    anti_node_mask[rows[valid], cols[valid]] = True
    return anti_node_mask


def part_1(input_data) -> int:
    city = np.array([list(map(ord, line)) for line in input_data.split("\n")])
    anti_node_mask = get_anti_node_mask(city)
    return np.sum(anti_node_mask).item()


def part_2(input_data) -> int:
    city = np.array([list(map(ord, line)) for line in input_data.split("\n")])
    anti_node_mask = get_anti_node_mask(city, limit=False)
    return np.sum(anti_node_mask).item()


def main():
    puzzle = Puzzle(day=8, year=2024)

    example, = puzzle.examples
    assert part_1(example.input_data) == int(example.answer_a)
    assert part_2(example.input_data) == 34

    input_data = puzzle.input_data
    puzzle.answer_a = part_1(input_data)
    puzzle.answer_b = part_2(input_data)
    print(f"{puzzle.answer_a=}, {puzzle.answer_b=}")


if __name__ == "__main__":
    main()
