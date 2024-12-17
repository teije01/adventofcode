"""
https://adventofcode.com/2024/day/11
"""
import math
from collections import Counter

from aocd.models import Puzzle


class StoneCollection:

    def __init__(self, stone_values: list[int]):
        self.stone_counter = Counter(stone_values)

    def __len__(self):
        return self.stone_counter.total()

    def blink(self):
        new_counter = Counter()
        for key, count in self.stone_counter.items():
            key_str = str(key)
            if key == 0:
                new_counter[1] += count
            elif len(key_str) % 2 == 1:  # uneven no of digits
                new_counter[key * 2024] += count
            else:
                new_counter[int(key_str[:len(key_str)//2])] += count
                new_counter[int(key_str[len(key_str)//2:])] += count
        self.stone_counter = new_counter


def part_1(input_data) -> int:
    stone_collection = StoneCollection(list(map(int, input_data.split())))
    [stone_collection.blink() for _ in range(25)]
    return len(stone_collection)


def part_2(input_data) -> int:
    stone_collection = StoneCollection(list(map(int, input_data.split())))
    [stone_collection.blink() for _ in range(75)]
    return len(stone_collection)


def main():
    puzzle = Puzzle(day=11, year=2024)

    example, = puzzle.examples
    assert part_1("125 17") == int(example.answer_a)

    input_data = puzzle.input_data
    puzzle.answer_a = part_1(input_data)
    puzzle.answer_b = part_2(input_data)
    print(f"{puzzle.answer_a=}, {puzzle.answer_b=}")


if __name__ == "__main__":
    main()
