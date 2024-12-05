"""
https://adventofcode.com/2024/day/5
"""
from operator import itemgetter
from itertools import groupby
from aocd.models import Puzzle


def read_input(input_data: str) -> tuple[list[tuple[int, ...]], list[list[int]]]:
    page_ordering, pages_to_produce = input_data.split("\n\n")
    page_ordering_rules = [tuple(map(int, line.split("|"))) for line in page_ordering.split("\n")]
    production_pages = [list(map(int, line.split(","))) for line in pages_to_produce.split("\n")]
    return page_ordering_rules, production_pages


def construct_not_left_mapper(page_ordering_rules) -> dict[int, set]:
    not_left = {
        left: set(r[1] for r in rules) for left, rules in
        groupby(sorted(page_ordering_rules, key=itemgetter(0)), key=itemgetter(0))
    }
    return not_left


def is_valid_update(pages: list[int], not_left: dict[int, set]) -> bool:
    left = set()
    for page in pages:
        if not_left.get(page, set()).intersection(left):
            return False
        left.add(page)
    else:
        return True


def order_pages(pages: list[int], not_left: dict[int, set]) -> list[int]:
    ordered_pages = [pages[0]]
    for idx in range(1, len(pages)):
        page = pages[idx]
        if not (right_of_page := not_left.get(page, set()).intersection(ordered_pages)):
            ordered_pages.append(page)  # correct sorting order
            continue
        insert_page_at = min(ordered_pages.index(p) for p in right_of_page)
        ordered_pages.insert(insert_page_at, page)
    return ordered_pages


def part_1(input_data) -> int:
    page_ordering_rules, updates = read_input(input_data)
    not_left = construct_not_left_mapper(page_ordering_rules)

    sum_mid_page_numbers = 0
    for pages in updates:
        if not is_valid_update(pages, not_left):
            continue
        sum_mid_page_numbers += pages[len(pages) // 2]
    return sum_mid_page_numbers


def part_2(input_data) -> int:
    page_ordering_rules, updates = read_input(input_data)
    not_left = construct_not_left_mapper(page_ordering_rules)

    sum_mid_page_numbers = 0
    for pages in updates:
        if is_valid_update(pages, not_left):
            continue
        pages = order_pages(pages, not_left)
        sum_mid_page_numbers += pages[len(pages) // 2]

    return sum_mid_page_numbers


def main():
    puzzle = Puzzle(day=5, year=2024)

    example, = puzzle.examples
    assert part_1(example.input_data) == int(example.answer_a)
    assert part_2(example.input_data) == 123

    input_data = puzzle.input_data
    puzzle.answer_a = part_1(input_data)
    puzzle.answer_b = part_2(input_data)
    print(f"{puzzle.answer_a=}, {puzzle.answer_b=}")


if __name__ == "__main__":
    main()
