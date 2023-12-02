"""
https://adventofcode.com/2023/day/1
"""
import re


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


def main():
    with open("solutions/2023/day1/input.txt", "r") as f:
        calibration_document = f.read().rstrip('\n').split("\n")

    answer_1 = sum(derive_calibration_value(line) for line in calibration_document)
    answer_2 = sum(derive_calibration_value(line, allow_text_digit=True) for line in calibration_document)

    print(f"Solution 1: {answer_1}")
    print(f"Solution 2: {answer_2}")


if __name__ == "__main__":
    main()
