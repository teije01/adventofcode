"""
https://adventofcode.com/2022/day/13
"""
import json
from dataclasses import dataclass
from itertools import zip_longest, chain
from typing import Union, Optional

PacketStructure = Union[int, list['PacketStructure'], None]

SEP = ">> "


def packet_pair_isordered(left: PacketStructure, right: PacketStructure, depth=0) -> Optional[bool]:
    print(f"{SEP*depth} Comparing packets {left} and {right}")
    match left, right:
        case int(), int():
            if left < right:
                return True
            elif left > right:
                return False
            return None
        case list(), list():  # both lists
            for left_sub, right_sub in zip_longest(left, right):
                result = packet_pair_isordered(left_sub, right_sub, depth=depth+1)
                if result is not None:
                    return result
        case list(), int():
            result = packet_pair_isordered(left, [right], depth=depth+1)
            if result is not None:
                return result
        case int(), list():
            result = packet_pair_isordered([left], right, depth=depth+1)
            if result is not None:
                return result
        case None, _:
            return True
        case _, None:
            return False
        case _:
            raise TypeError(f"Wrong packet type for packets: {left_packet, right_packet}")


@dataclass
class Packet:

    structure: PacketStructure

    @classmethod
    def from_string(cls, txt: str):
        return cls(structure=json.loads(txt))

    def __cmp__(self, other: "Packet"):
        return packet_pair_isordered(self.structure, other.structure) is None

    def __lt__(self, other: "Packet"):
        return packet_pair_isordered(self.structure, other.structure) is True

    def __gt__(self, other: "Packet"):
        return packet_pair_isordered(self.structure, other.structure) is False


if __name__ == "__main__":
    with open("solutions/2022/day13/input.txt", "r") as f:
        packet_pairs: list[tuple[Packet, ...]] = [
            tuple(map(Packet.from_string, line.split("\n")))
            for line in f.read().rstrip("\n").split("\n\n")
        ]

    indices_sum = 0
    for i, (left_packet, right_packet) in enumerate(packet_pairs, start=1):
        if left_packet < right_packet:
            indices_sum += i

    div_1 = Packet([[2]])
    div_2 = Packet([[6]])
    packet_pairs.append((div_1, div_2))

    all_packets_sorted = sorted(chain(*packet_pairs))
    div_1_index = all_packets_sorted.index(div_1) + 1
    div_2_index = all_packets_sorted.index(div_2) + 1

    print(f"Solution 1: {indices_sum}")
    print(f"Solution 2: {div_1_index * div_2_index}")
