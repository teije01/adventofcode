"""
https://adventofcode.com/2023/day/1
"""
import re

from aocd.models import Puzzle

DIGIT_MAPPING = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def derive_calibration_value(input_string, allow_text_digit=False) -> int:
    if allow_text_digit:
        any_text_digit = f"(?=(\\d|{'|'.join([digit for digit in DIGIT_MAPPING])}))"
        all_matches = re.findall(any_text_digit, input_string)
        all_digits = [DIGIT_MAPPING.get(match_result, match_result) for match_result in all_matches]
    else:
        all_digits = re.findall(r"\d", input_string)
    calibration_value = int(f"{all_digits[0]}{all_digits[-1]}")
    return calibration_value


def part_1(input_data: str) -> int:
    calibration_document = input_data.split("\n")
    answer_1 = sum(derive_calibration_value(line) for line in calibration_document)
    return answer_1


def part_2(input_data: str) -> int:
    calibration_document = input_data.split("\n")
    answer_2 = sum(derive_calibration_value(line, allow_text_digit=True) for line in calibration_document)
    return answer_2


def main():
    puzzle = Puzzle(day=1, year=2023)

    example1, example2 = puzzle.examples
    assert part_1(example1.input_data) == int(example1.answer_a)
    assert part_2(example2.input_data) == int(example2.answer_b)

    input_data = puzzle.input_data
    puzzle.answer_a = part_1(puzzle.input_data)
    puzzle.answer_b = part_2(puzzle.input_data)
    print(f"{puzzle.answer_a=}, {puzzle.answer_b=}")


if __name__ == "__main__":
    main()
