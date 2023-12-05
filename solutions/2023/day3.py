"""
https://adventofcode.com/2023/day/3
"""
import re
from typing import Iterator

import numpy as np
from aocd.models import Puzzle


def iter_valid_parts(
    input_data: list[str], valid_part_mask: np.ndarray
) -> Iterator[int]:
    for row_nr, line in enumerate(input_data):
        for m in re.finditer(r"\d+", line):
            if np.any(valid_part_mask[row_nr, m.start() : m.end()]):
                yield int(m.group())


def part_1(input_data: str) -> int:
    input_data = input_data.split()
    shape = len(input_data), len(input_data[0])
    mask = np.full((shape[0], shape[1]), False, dtype=bool)
    for row_nr, line in enumerate(input_data):
        for m in re.finditer(r"[^\d.]", line):
            mask[
                max(row_nr - 1, 0) : min(row_nr + 2, shape[0]),
                max(m.start() - 1, 0) : min(m.start() + 2, shape[1]),
            ] = True
    answer_a = sum(iter_valid_parts(input_data, mask))
    return answer_a


def intersecting_range(r1: range, r2: range) -> range:
    return range(max(r1.start, r2.start), min(r1.stop, r2.stop))


def part_2(input_data: str) -> int:
    line_length = input_data.index("\n")
    star_locations = [
        divmod(m.start(), line_length)
        for m in re.finditer(r"\*", input_data.replace("\n", ""))
    ]  # list[(row, column), ...]
    row_matches = {
        row: list(re.finditer(r"\d+", line))
        for row, line in enumerate(input_data.split("\n"))
    }
    sum_of_gear_ratios = 0
    for star_row, star_col in star_locations:
        touching_parts = []
        col_range = range(max(0, star_col - 1), min(star_col + 2, line_length))
        for match in row_matches.get(star_row - 1, []) + row_matches.get(star_row, []) + row_matches.get(star_row + 1, []):
            if intersecting_range(range(match.start(), match.end()), col_range):
                touching_parts.append(int(match.group()))
        if len(touching_parts) == 2:
            sum_of_gear_ratios += touching_parts[0] * touching_parts[1]
    return sum_of_gear_ratios


def main():
    puzzle = Puzzle(day=3, year=2023)
    input_data = puzzle.input_data

    puzzle.answer_a = part_1(input_data)
    puzzle.answer_b = part_2(input_data)
    print(f"{puzzle.answer_a=}, {puzzle.answer_b=}")


if __name__ == "__main__":
    main()
