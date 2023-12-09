"""
https://adventofcode.com/2023/day/6
"""
import math
from collections import namedtuple
from typing import Iterator

from aocd.models import Puzzle

RaceRecord = namedtuple("RaceRecord", ["time", "distance"])


def improve_record(race_record: RaceRecord) -> range:
    """
    time_remaining = max_duration - time_pressed
    velocity = time_pressed
    distance = velocity * time_remaining
             = time_pressed * (max_duration - time_pressed)
             = - time_pressed^2 + max_duration * time_pressed

    distance > record_distance
    - time_pressed^2 + max_duration * time_pressed > record_distance
    - time_pressed^2 + max_duration * time_pressed - record_distance > 0
    """
    max_duration = race_record.time
    d = max_duration**2 - 4 * race_record.distance
    x1 = (-max_duration + math.sqrt(d)) / -2
    x2 = (-max_duration - math.sqrt(d)) / -2
    t_improved_min = int(math.ceil(x1) + (x1 == int(x1)))
    t_improved_max = int(math.ceil(x2))
    result = range(t_improved_min, t_improved_max)
    return result


def parse_input_1(input_data: str) -> Iterator[RaceRecord]:
    time_str, distance_str = input_data.splitlines()
    times = map(int, time_str.split()[1:])
    distances = map(int, distance_str.split()[1:])
    yield from (RaceRecord(time, distance) for time, distance in zip(times, distances))


def part_1(input_data) -> int:
    return math.prod(
        len(improve_record(race_record)) for race_record in parse_input_1(input_data)
    )


def parse_input_2(input_data: str) -> RaceRecord:
    time_str, distance_str = input_data.splitlines()
    race_record = RaceRecord(
        int("".join(time_str.split()[1:])), int("".join(distance_str.split()[1:]))
    )
    return race_record


def part_2(input_data) -> int:
    return len(improve_record(parse_input_2(input_data)))


def main():
    puzzle = Puzzle(day=6, year=2023)

    (example,) = puzzle.examples
    assert part_1(example.input_data) == 288
    assert part_2(example.input_data) == int(example.answer_b)

    input_data = puzzle.input_data
    puzzle.answer_a = part_1(input_data)
    puzzle.answer_b = part_2(input_data)
    print(f"{puzzle.answer_a=}, {puzzle.answer_b=}")


if __name__ == "__main__":
    main()
