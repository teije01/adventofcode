"""
https://adventofcode.com/2023/day/7
"""
from collections import Counter
from dataclasses import dataclass, field
from typing import Literal

from aocd.models import Puzzle


CARD_HEX_TRANS_RULESET = {
    1: str.maketrans("TJQKA", "ABCDE"),
    2: str.maketrans("TJQKA", "A1CDE"),
}


@dataclass
class HandBid:
    hand: str
    bid: int
    ruleset: Literal[1, 2]
    score: int = field(default=0, init=False)

    def __post_init__(self):
        hand_counter = Counter(self.hand)
        if self.ruleset == 2:
            j_count = hand_counter.pop("J", 0)
            hand_counter.update(
                {hand_counter.most_common(1)[0][0]: j_count}
                if hand_counter
                else {"A": j_count}
            )
        trans = CARD_HEX_TRANS_RULESET[self.ruleset]
        match tuple(v[1] for v in hand_counter.most_common()):
            case (5,):
                self.score = int(f"6{self.hand}".translate(trans), base=15)
            case (4, 1):
                self.score = int(f"5{self.hand}".translate(trans), base=15)
            case (3, 2):
                self.score = int(f"4{self.hand}".translate(trans), base=15)
            case (3, 1, 1):
                self.score = int(f"3{self.hand}".translate(trans), base=15)
            case (2, 2, 1):
                self.score = int(f"2{self.hand}".translate(trans), base=15)
            case (2, 1, 1, 1):
                self.score = int(f"1{self.hand}".translate(trans), base=15)
            case _:
                self.score = int(self.hand.translate(trans), base=15)


def part_1(input_data) -> int:
    hand_bids = [
        HandBid(hand, int(bid), ruleset=1)
        for hand, bid in map(str.split, input_data.splitlines())
    ]
    hand_bids.sort(key=lambda hb: hb.score)
    return sum(rank * hand_bid.bid for rank, hand_bid in enumerate(hand_bids, start=1))


def part_2(input_data) -> int:
    hand_bids = [
        HandBid(hand, int(bid), ruleset=2)
        for hand, bid in map(str.split, input_data.splitlines())
    ]
    hand_bids.sort(key=lambda hb: hb.score)
    return sum(rank * hand_bid.bid for rank, hand_bid in enumerate(hand_bids, start=1))


def main():
    puzzle = Puzzle(day=7, year=2023)

    (example,) = puzzle.examples
    assert part_1(example.input_data) == int(example.answer_a)
    assert part_2(example.input_data) == 5905

    input_data = puzzle.input_data
    puzzle.answer_a = part_1(input_data)
    puzzle.answer_b = part_2(input_data)
    print(f"{puzzle.answer_a=}, {puzzle.answer_b=}")


if __name__ == "__main__":
    main()
