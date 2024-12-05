"""
https://adventofcode.com/2024/day/4
"""
import inspect
from itertools import product
from typing import Iterator

from aocd.models import Puzzle


def generate_cardinal_candidates(
    row: int,
    col: int,
    shape: tuple[int, int],
    match_word: str,
) -> Iterator[tuple[list[int], list[int]]]:
    word_length = len(match_word)
    left_range = range(col, col - word_length, -1)
    right_range = range(col, col + word_length)
    top_range = range(row, row - word_length, -1)
    bottom_range = range(row, row + word_length)

    if -1 not in left_range: yield [row] * word_length, list(left_range)
    if -1 not in top_range: yield list(top_range), [col] * word_length
    if shape[1] not in right_range: yield [row] * word_length, list(right_range)
    if shape[0] not in bottom_range: yield list(bottom_range), [col] * word_length
    if -1 not in top_range and -1 not in left_range: yield list(top_range), list(left_range)
    if -1 not in top_range and shape[1] not in right_range: yield list(top_range), list(right_range)
    if shape[0] not in bottom_range and -1 not in left_range: yield list(bottom_range), list(left_range)
    if shape[0] not in bottom_range and shape[1] not in right_range: yield list(bottom_range), list(right_range)


def generate_x_candidates(
    row: int,
    col: int,
    shape: tuple[int, int],
    match_word: str,
) -> Iterator[tuple[list[int], list[int]]]:
    word_length = len(match_word)
    half_length = word_length // 2
    hor_range = range(col - half_length, col + half_length + 1)
    vert_range = range(row - half_length, row + half_length + 1)
    if (-1 in hor_range) or (-1 in vert_range) or (shape[0] in hor_range) or (shape[1] in vert_range):
        return
    yield (list(vert_range) + list(reversed(vert_range))) * 2, list(hor_range) * 2 + list(reversed(hor_range)) * 2


def part_1(input_data) -> int:
    lines = input_data.split("\n")
    match_word = list("XMAS")
    count = 0
    shape = (len(lines), len(lines[0]))
    for row, col in product(range(shape[0]), range(shape[1])):
        if lines[row][col] != match_word[0]:
            continue
        for row_candidates, col_candidates in generate_cardinal_candidates(row, col, shape, match_word):
            candidate_word = [lines[r][c] for r, c in zip(row_candidates, col_candidates)]
            count += candidate_word == match_word
    return count


def part_2(input_data) -> int:
    lines = input_data.split("\n")
    match_word = "MAS"
    count = 0
    shape = (len(lines), len(lines[0]))
    for row, col in product(range(shape[0]), range(shape[1])):
        if lines[row][col] != match_word[len(match_word) // 2]:
            continue
        for row_candidates, col_candidates in generate_x_candidates(row, col, shape, match_word):
            candidate_word = "".join(lines[r][c] for r, c in zip(row_candidates, col_candidates))
            count += candidate_word.count(match_word) == 2
    return count


def main():
    puzzle = Puzzle(day=4, year=2024)

    example_input_data = inspect.cleandoc(
        """
        MMMSXXMASM
        MSAMXMSMSA
        AMXSXMAAMM
        MSAMASMSMX
        XMASAMXAMM
        XXAMMXXAMA
        SMSMSASXSS
        SAXAMASAAA
        MAMMMXMMMM
        MXMXAXMASX
        """
    )
    assert part_1(example_input_data) == 18
    assert part_2(example_input_data) == 9

    input_data = puzzle.input_data
    puzzle.answer_a = part_1(input_data)
    puzzle.answer_b = part_2(input_data)
    print(f"{puzzle.answer_a=}, {puzzle.answer_b=}")


if __name__ == "__main__":
    main()
