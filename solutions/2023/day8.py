"""
https://adventofcode.com/2023/day/8
"""
import itertools
import re
from collections import namedtuple
from typing import Iterator, Literal
from math import lcm

from aocd.models import Puzzle
from aocd.examples import Example


NodeMap = namedtuple("NodeMap", "L,R")


def parse_input_data(
    input_data,
) -> tuple[Iterator[Literal["L", "R"]], dict[str, NodeMap]]:
    instructions, node_lookup_str = input_data.split("\n\n")
    node_mapping = {
        m["key"]: NodeMap(m["left"], m["right"])
        for m in re.finditer(
            r"(?P<key>\w{3}) = \((?P<left>\w{3}), (?P<right>\w{3})\)", node_lookup_str
        )
    }
    return itertools.cycle(instructions), node_mapping


def part_1(input_data) -> int:
    instructions, node_mapping = parse_input_data(input_data)
    node = "AAA"
    steps = 0
    while node != "ZZZ":
        node = getattr(node_mapping[node], next(instructions))
        steps += 1
    return steps


def part_2(input_data) -> int:
    instructions, node_mapping = parse_input_data(input_data)
    nodes = [node for node in node_mapping if node.endswith("A")]
    nodes_at_z_steps = {}
    steps = 0
    while nodes:
        instruction = next(instructions)
        nodes = [getattr(node_mapping[node], instruction) for node in nodes]
        steps += 1
        node_indices_at_z = [i for i, node in enumerate(nodes) if node.endswith("Z")]
        if node_indices_at_z:
            nodes_at_z_steps.update({nodes.pop(index): steps for index in node_indices_at_z})
    return lcm(*nodes_at_z_steps.values())


def main():
    puzzle = Puzzle(day=8, year=2023)

    (example_1,) = puzzle.examples
    example_2 = Example(
        "LR\n\n"
        "11A = (11B, XXX)\n11B = (XXX, 11Z)\n11Z = (11B, XXX)\n22A = (22B, XXX)\n"
        "22B = (22C, 22C)\n22C = (22Z, 22Z)\n22Z = (22B, 22B)\nXXX = (XXX, XXX)",
        answer_b="6"
    )

    assert part_1(example_1.input_data) == 2
    assert part_2(example_2.input_data) == int(example_2.answer_b)

    input_data = puzzle.input_data
    puzzle.answer_a = part_1(input_data)
    puzzle.answer_b = part_2(input_data)
    print(f"{puzzle.answer_a=}, {puzzle.answer_b=}")


if __name__ == "__main__":
    main()
