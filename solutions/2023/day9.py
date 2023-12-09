"""
https://adventofcode.com/2023/day/9
"""
import itertools
from io import StringIO
from typing import Literal

import numpy as np
from aocd.models import Puzzle


def rsub(a, b):
    return b - a


def predict_value(sequence: np.array, side: Literal["left", "right"]) -> int:
    seq_to_diff = sequence
    diffs = []
    while not np.all(seq_to_diff == 0):
        diffs.append(seq_to_diff)
        seq_to_diff = np.diff(seq_to_diff)
    match side:
        case "right":
            return +np.cumsum([diff[-1] for diff in diffs[::-1]])[-1]
        case "left":
            return list(itertools.accumulate((diff[0] for diff in diffs[::-1]), func=rsub, initial=0))[-1]


def part_1(input_data) -> int:
    sequences = np.loadtxt(StringIO(input_data), dtype=np.int64)
    return sum(predict_value(sequence, side="right") for sequence in sequences)


def part_2(input_data) -> int:
    sequences = np.loadtxt(StringIO(input_data), dtype=np.int64)
    return sum(predict_value(sequence, side="left") for sequence in sequences)


def main():
    puzzle = Puzzle(day=9, year=2023)

    example, = puzzle.examples
    assert part_1(example.input_data) == int(example.answer_a)
    assert part_2(example.input_data) == int(example.answer_b)

    input_data = puzzle.input_data
    puzzle.answer_a = part_1(input_data)
    puzzle.answer_b = part_2(input_data)
    print(f"{puzzle.answer_a=}, {puzzle.answer_b=}")


if __name__ == "__main__":
    main()
