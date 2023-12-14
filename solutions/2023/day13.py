"""
https://adventofcode.com/2023/day/13
"""
import io
from typing import Iterator

import numpy as np
from aocd.models import Puzzle


def parse_input_data(input_data) -> Iterator[np.ndarray]:
    for pattern_str in input_data.translate(str.maketrans(".#", "01")).split("\n\n"):
        pattern = np.genfromtxt(io.StringIO(pattern_str), delimiter=1).astype(bool)
        yield pattern


def find_reflection(pattern, smudge=False) -> int:
    v_size, h_size = pattern.shape
    (v_candidates,) = np.where(np.sum(pattern[:, 1:] == pattern[:, :-1], axis=0) >= (v_size - smudge))
    for cand in v_candidates:
        v_cand = cand + 1
        overlap = min(v_cand, h_size - v_cand)
        n_matches = overlap * v_size - smudge
        left_side_flipped = np.flip(pattern[:, v_cand - overlap: v_cand], axis=1)
        right_side = pattern[:, v_cand: v_cand + overlap]
        if np.sum(left_side_flipped == right_side) == n_matches:
            return v_cand


def part_1(input_data) -> int:
    score = 0
    for i, pattern in enumerate(parse_input_data(input_data)):
        v_line = find_reflection(pattern)
        h_line = find_reflection(pattern.T)
        score += (v_line or 0) + (h_line or 0) * 100
    return score


def part_2(input_data) -> int:
    score = 0
    for i, pattern in enumerate(parse_input_data(input_data)):
        v_line = find_reflection(pattern, smudge=True)
        h_line = find_reflection(pattern.T, smudge=True)
        score += (v_line or 0) + (h_line or 0) * 100
    return score


def main():
    puzzle = Puzzle(day=13, year=2023)

    (example,) = puzzle.examples
    assert part_1(example.input_data) == int(example.answer_a)
    assert part_2(example.input_data) == 400

    puzzle.answer_a = part_1(puzzle.input_data)
    puzzle.answer_b = part_2(puzzle.input_data)
    print(f"{puzzle.answer_a=}, {puzzle.answer_b=}")


if __name__ == "__main__":
    main()
