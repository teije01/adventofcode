"""
https://adventofcode.com/2022/day/11
"""
import re
from typing import Callable
from math import lcm


class Monkey:
    def __init__(
            self,
            monkey_nr: int,
            items: list[int],
            apply: Callable,
            divider: int,
            monkey_test_true: int,
            monkey_test_false: int,
    ):
        self.monkey_nr = monkey_nr
        self.items = items
        self.apply = apply
        self.divider = divider
        self.monkey_mapper = {True: monkey_test_true, False: monkey_test_false}
        self.inspection_counter = 0
        self.limit: None | int = None

    def __repr__(self):
        return f"Monkey {self.monkey_nr} holds: {self.items}"

    @classmethod
    def from_monkey_setup(cls, setup_txt: str):
        monkey_nr, starting_items, operation, test, if_true, if_false = setup_txt.split("\n")
        nr = int(re.search(r"Monkey (\d)+:", monkey_nr).groups()[0])
        items = list(map(int, re.search(r"Starting items: ((?:\d+(?:, )?)+)",
                                        starting_items).groups()[0].split(", ")))
        operation = operation.split("Operation: new = ")[1]
        apply = lambda old: eval(operation, None, {"old": old})
        divider = int(re.search(r"Test: divisible by (\d+)", test).groups()[0])
        monkey_nr_true = int(re.search(r"If true: throw to monkey (\d+)", if_true).groups()[0])
        monkey_nr_false = int(re.search(r"If false: throw to monkey (\d+)", if_false).groups()[0])
        return cls(nr, items, apply, divider, monkey_nr_true, monkey_nr_false)

    def set_worry_limit(self, value: int):
        self.limit = value

    def test(self, item):
        return item % self.divider == 0

    def inspect_and_trow_item(self) -> tuple:
        item = self.items.pop(0)
        self.inspection_counter += 1
        if self.limit is None:
            new_worry_level = self.apply(item) // 3
        else:
            new_worry_level = self.apply(item) % self.limit
        pass_to_monkey_nr = self.monkey_mapper[self.test(new_worry_level)]
        return pass_to_monkey_nr, new_worry_level

    def receive_item(self, item: int):
        self.items.append(item)


class MonkeyGame:
    def __init__(self, monkeys: list[Monkey]):
        self.monkeys: dict[int, Monkey] = {monkey.monkey_nr: monkey for monkey in monkeys}

    def play(self, rounds: int):
        for round_nr in range(rounds):
            self.play_round()

    def play_round(self):
        for monkey_nr, monkey in self.monkeys.items():
            while monkey.items:
                pass_to_monkey_nr, new_worry_level = monkey.inspect_and_trow_item()
                self.monkeys[pass_to_monkey_nr].receive_item(new_worry_level)


if __name__ == "__main__":
    with open("solutions/2022/day11/test-input.txt", "r") as f:
        monkey_setup_list = [m for m in f.read().rstrip("\n").split("\n\n")]

    mg = MonkeyGame([Monkey.from_monkey_setup(setup) for setup in monkey_setup_list])
    mg.play(rounds=20)
    monkey_business_1 = sorted(
        [monkey.inspection_counter for monkey_nr, monkey in mg.monkeys.items()],
        reverse=True
    )

    mg = MonkeyGame([Monkey.from_monkey_setup(setup) for setup in monkey_setup_list])
    limit = lcm(*[monkey.divider for monkey in mg.monkeys.values()])
    for monkey in mg.monkeys.values():
        monkey.set_worry_limit(limit)
    mg.play(rounds=10000)
    monkey_business_2 = sorted(
        [monkey.inspection_counter for monkey_nr, monkey in mg.monkeys.items()],
        reverse=True
    )

    print(f"Solution 1: {monkey_business_1[0] * monkey_business_1[1]}")
    print(f"Solution 2: {monkey_business_2[0] * monkey_business_2[1]}")
