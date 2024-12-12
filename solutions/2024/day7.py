"""
https://adventofcode.com/2024/day/7
"""
import dataclasses
import math
from itertools import product, chain
from operator import add, mul, pow
from typing import Callable

from aocd.models import Puzzle


def concat(operand1: int, operand2: int) -> int:
    power = int(math.log10(operand2)) + 1
    return operand1 * pow(10,  power) + operand2


@dataclasses.dataclass
class Equation:
    result: int
    operands: list[int]

    @classmethod
    def from_str(cls, line: str):
        result_str, operands_str = line.split(": ")
        operands = list(map(int, operands_str.split()))
        return cls(int(result_str), operands)

    def is_valid(self, operator_candidates: tuple[Callable[[int, int], int], ...]):
        for operators in product(operator_candidates, repeat=len(self.operands)-1):
            result = self.operands[0]
            for i, operator in enumerate(operators, start=1):
                result = operator(result, self.operands[i])
            if result == self.result:
                # self.print_eq(operators)
                return True
        return False

    def print_eq(self, operators) -> None:
        op_to_str = {add: "+", mul: "*", concat: "||"}
        str_operands = [op_to_str[op] for op in operators]
        right_side = f" ".join(chain(*zip(str_operands, map(str, self.operands[1:]))))
        eq_str = f"{self.result} = {self.operands[0]} {right_side}"
        return print(eq_str)


def part_1(input_data) -> int:
    equations = [Equation.from_str(line) for line in input_data.split("\n")]
    total_calibration_result = sum(eq.result for eq in equations if eq.is_valid((add, mul)))
    return total_calibration_result


def part_2(input_data) -> int:
    equations = [Equation.from_str(line) for line in input_data.split("\n")]
    total_calibration_result = sum(eq.result for eq in equations if eq.is_valid((add, mul, concat)))
    return total_calibration_result


def main():
    puzzle = Puzzle(day=7, year=2024)

    example, = puzzle.examples
    assert part_1(example.input_data) == int(example.answer_a)
    assert part_2(example.input_data) == 11387

    input_data = puzzle.input_data
    puzzle.answer_a = part_1(input_data)
    puzzle.answer_b = part_2(input_data)
    print(f"{puzzle.answer_a=}, {puzzle.answer_b=}")


if __name__ == "__main__":
    main()
