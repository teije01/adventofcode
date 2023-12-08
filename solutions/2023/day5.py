"""
https://adventofcode.com/2023/day/5
"""

MAP = dict[range, int]

from aocd.models import Puzzle


def parse_input_data(input_data) -> tuple[list[int], dict[str, MAP]]:
    seeds_section, *mapping_sections = input_data.split("\n\n")
    seeds = list(map(int, seeds_section.split(":")[1].split()))
    mappers = {}
    for section in mapping_sections:
        mapper = {}
        for map_entry in section.split("\n")[1:]:
            dst_start, src_start, range_len = map(int, map_entry.split())
            mapper[range(src_start, src_start + range_len)] = dst_start - src_start
        mappers[section.split("\n")[0].split(" map:")[0]] = mapper
    return seeds, mappers


def traverse_mappers(seed: int, mappers: dict[str, MAP]) -> int:
    value = seed
    for mapper_name, mapper in mappers.items():
        for key in mapper:
            if value in key:
                value += mapper[key]
                break
    return value


def part_1(input_data) -> int:
    seeds, mappers = parse_input_data(input_data)
    return min(traverse_mappers(seed, mappers) for seed in seeds)


def intersecting_range(r1: range, r2: range) -> range:
    return range(max(r1.start, r2.start, 1), min(r1.stop, r2.stop))


def range_remainder(r1: range, r2: range) -> tuple[range, range]:
    """Return remainding ranges (left, right) from r1 - r2"""
    remainder_left = range(r1.start, r2.start)
    remainder_right = range(r2.stop, r1.stop)
    return remainder_left, remainder_right


def traverse_mappers_range(seeds: list[range], mappers: dict[str, MAP]) -> list[range]:
    remaining_ranges = seeds
    new_ranges = []
    for mapper_name, mapper in mappers.items():
        new_ranges = []
        while remaining_ranges:
            input_range = remaining_ranges.pop(0)
            for src_range, offset in mapper.items():
                if range_intersection := intersecting_range(input_range, src_range):
                    new_ranges.append(range(range_intersection.start + offset, range_intersection.stop + offset))
                    remainder_left, remainder_right = range_remainder(input_range, src_range)
                    if remainder_left:
                        remaining_ranges.append(remainder_left)
                    if remainder_right:
                        remaining_ranges.append(remainder_right)
                    break
            else:
                new_ranges.append(input_range)
        remaining_ranges = new_ranges.copy()
    return new_ranges


def part_2(input_data) -> int:
    seeds, mappers = parse_input_data(input_data)
    seeds_r1 = range(seeds[0], seeds[0] + seeds[1])
    seeds_r2 = range(seeds[2], seeds[2] + seeds[3])
    location_ranges = traverse_mappers_range([seeds_r1, seeds_r2], mappers)
    return min(r.start for r in location_ranges)


def main():
    puzzle = Puzzle(day=5, year=2023)

    example, = puzzle.examples
    assert part_1(example.input_data) == int(example.answer_a)
    assert part_2(example.input_data) == int(example.answer_b)

    input_data = puzzle.input_data
    puzzle.answer_a = part_1(input_data)
    puzzle.answer_b = part_2(input_data)
    print(f"{puzzle.answer_a=}, {puzzle.answer_b=}")


if __name__ == "__main__":
    main()
