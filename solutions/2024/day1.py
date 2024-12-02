"""
https://adventofcode.com/2024/day/1
"""
from itertools import batched
from collections import Counter

from aocd.models import Puzzle


def read_input(input_data: str) -> tuple[tuple[int, ...], tuple[int, ...]]:
    left, right = zip(*batched(map(int, input_data.split()), 2))
    return left, right


def part_1(input_data: str) -> int:
    left, right = read_input(input_data)
    left = sorted(left)
    right = sorted(right)
    total_distance = sum(abs(l - r) for l, r in zip(left, right))
    return total_distance


def part_2(input_data) -> int:
    left, right = read_input(input_data)
    right_counter = Counter(right)
    similarity_socre = sum(right_counter.get(l, 0) * l for l in left)
    return similarity_socre


def main():
    puzzle = Puzzle(day=1, year=2024)

    example, = puzzle.examples
    assert part_1(example.input_data) == int(example.answer_a)
    assert part_2(example.input_data) == 31

    input_data = puzzle.input_data
    puzzle.answer_a = part_1(input_data)
    puzzle.answer_b = part_2(input_data)
    print(f"{puzzle.answer_a=}, {puzzle.answer_b=}")


if __name__ == "__main__":
    main()
