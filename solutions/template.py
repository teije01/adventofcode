"""
https://adventofcode.com/20xx/day/x
"""

from aocd.models import Puzzle


def part_1(input_data) -> int:
    return None


def part_2(input_data) -> int:
    return None


def main():
    puzzle = Puzzle(day=None, year=None)

    example, = puzzle.examples
    assert part_1(example.input_data) == int(example.answer_a)
    assert part_2(example.input_data) == int(example.answer_b)

    input_data = puzzle.input_data
    puzzle.answer_a = part_1(input_data)
    puzzle.answer_b = part_2(input_data)
    print(f"{puzzle.answer_a=}, {puzzle.answer_b=}")


if __name__ == "__main__":
    main()
