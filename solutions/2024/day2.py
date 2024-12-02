"""
https://adventofcode.com/2024/day/2
"""

from itertools import pairwise
from aocd.models import Puzzle


def read_input(input_data: str) -> list[list[int]]:
    reports = [list(map(int, line.split())) for line in input_data.split("\n")]
    return reports


def is_safe(report: list[int], dampener=False) -> bool:

    diff = [right - left for left, right in pairwise(report)]
    is_decreasing = sum(d < 0 for d in diff) >= (len(diff) - 2)
    if is_decreasing:
        diff = [-d for d in diff]  # map to positive

    # All safe
    safe_diff = [0 < d < 4 for d in diff]
    n_bad_diff = len(safe_diff) - sum(safe_diff)
    if all(safe_diff):
        return True
    elif not (dampener and n_bad_diff < 3):
        return False  # no dampener or more than 1 bad level

    # Handle dampener
    idx = safe_diff.index(False)
    if n_bad_diff == 1 and idx in (0, len(diff) - 1):
        return True  # start or end element may be discarded as the only bad level
    elif n_bad_diff == 2 and safe_diff[idx + 1]:
        return False  # two distinct bad levels found (non-consecutive bad difference)
    else:
        return 0 < (diff[idx] + diff[idx + 1]) < 4  # difference over three levels is safe


def part_1(input_data: str) -> int:
    reports = read_input(input_data)
    safe_reports = sum(is_safe(report) for report in reports)
    return safe_reports


def part_2(input_data) -> int:
    reports = read_input(input_data)
    safe_reports = sum(is_safe(report, dampener=True) for report in reports)
    return safe_reports


def main():
    puzzle = Puzzle(day=2, year=2024)

    example, = puzzle.examples
    assert part_1(example.input_data) == int(example.answer_a)
    assert part_2(example.input_data) == int(example.answer_b)

    input_data = puzzle.input_data
    puzzle.answer_a = part_1(input_data)
    puzzle.answer_b = part_2(input_data)
    print(f"{puzzle.answer_a=}, {puzzle.answer_b=}")


if __name__ == "__main__":
    main()
