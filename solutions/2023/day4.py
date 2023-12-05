"""
https://adventofcode.com/2023/day/4
"""
from collections import Counter
from typing import Iterator

from aocd.models import Puzzle


def iter_cards_winning_numbers(input_data: str) -> Iterator[tuple[set, set]]:
    for card in input_data.split("\n"):
        card_id, card_content = card.split(":")
        my_numbers, winning_numbers = card_content.split(" | ")
        yield set(map(int, my_numbers.split())), set(map(int, winning_numbers.split()))


def part_1_and_2(input_data: str) -> tuple[int, int]:
    total_cards = len(input_data.splitlines())
    total_points = 0
    counter = Counter(range(total_cards))
    for i, (my_numbers, winning_numbers) in enumerate(iter_cards_winning_numbers(input_data)):
        n_cards = counter.get(i)
        if n_winning_numbers := len(my_numbers.intersection(winning_numbers)):
            total_points += 2 ** (n_winning_numbers - 1)
            counter.update(dict.fromkeys(range(i+1, i+1+n_winning_numbers), n_cards))
    for key in filter(lambda k: k >= total_cards, counter):
        counter.pop(key)  # Remove keys beyond the maximum card (if any)
    return total_points, counter.total()


def main():
    puzzle = Puzzle(day=4, year=2023)

    example, = puzzle.examples
    assert part_1_and_2(example.input_data) == (int(example.answer_a), int(example.answer_b))

    input_data = puzzle.input_data
    puzzle.answer_a, puzzle.answer_b = part_1_and_2(input_data)
    print(f"{puzzle.answer_a=}, {puzzle.answer_b=}")


if __name__ == "__main__":
    main()
