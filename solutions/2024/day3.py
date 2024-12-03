"""
https://adventofcode.com/2024/day/3
"""
import re
from operator import mul
from aocd.models import Puzzle


def part_1(input_data) -> int:
    mul_pattern = re.compile(r"mul\((\d+),(\d+)\)")
    result = sum(mul(*map(int, m.groups())) for m in mul_pattern.finditer(input_data))
    return result


def part_2(input_data) -> int:
    op_pattern = re.compile(r"(?P<operator>mul|do|don't)\(((?P<operand_1>\d+),(?P<operand_2>\d+))?\)")
    do = True
    result = 0
    for re_match in op_pattern.finditer(input_data):
        if not do:
            if re_match["operator"] == "do":  # ignore every other operation than 'do()'
                do = True
        elif re_match["operator"] == "don't":
            do = False
        elif re_match["operator"] == "mul":
            result += mul(int(re_match["operand_1"]), int(re_match["operand_2"]))

    return result


def main():
    puzzle = Puzzle(day=3, year=2024)

    assert part_1("xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))") == 161
    assert part_2("xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))") == 48

    input_data = puzzle.input_data
    puzzle.answer_a = part_1(input_data)
    puzzle.answer_b = part_2(input_data)
    print(f"{puzzle.answer_a=}, {puzzle.answer_b=}")


if __name__ == "__main__":
    main()
