"""
https://adventofcode.com/2024/day/9
"""
from itertools import repeat
from typing import Iterator

from aocd.models import Puzzle
from dataclasses import dataclass, field


def gen_file_ids(file_blocks: list[int], free_blocks: list[int]) -> Iterator[int]:
    file_blocks = file_blocks.copy()
    free_blocks = free_blocks.copy()
    start_id = 0
    end_id = len(file_blocks) - 1
    while file_blocks:
        yield from repeat(start_id, file_blocks.pop(0))
        start_id += 1
        free_blocks_to_fill = free_blocks.pop(0)
        while file_blocks and (free_blocks_to_fill > 0):
            take_from_last_file_block = min(free_blocks_to_fill, file_blocks[-1])
            yield from repeat(end_id, take_from_last_file_block)
            free_blocks_to_fill -= take_from_last_file_block
            file_blocks[-1] -= take_from_last_file_block
            if file_blocks[-1] == 0:
                file_blocks.pop(-1)
                end_id -= 1


@dataclass
class FileSystem:
    file_blocks: list[int]
    free_blocks: list[int]
    file_ids_compacted: list[int] = field(default_factory=list, init=False)

    @classmethod
    def from_disk_map(cls, disk_map: str):
        disk_map = list(map(int, disk_map))
        return cls(file_blocks=disk_map[::2], free_blocks=disk_map[1::2])

    def de_fragment_blocks(self):
        self.file_ids_compacted = list(gen_file_ids(self.file_blocks, self.free_blocks))

    def de_fragment_files(self):
        pass

    @property
    def checksum(self) -> int:
        return sum(i * file_id for i, file_id in enumerate(gen_file_ids(self.file_blocks, self.free_blocks)))

def part_1(input_data) -> int:
    disk_map, = (FileSystem.from_disk_map(dm) for dm in input_data.split("\n"))
    return disk_map.checksum


def part_2(input_data) -> int:
    disk_map, = (FileSystem.from_disk_map(dm) for dm in input_data.split("\n"))
    return None


def main():
    puzzle = Puzzle(day=9, year=2024)

    example, = puzzle.examples
    assert part_1(example.input_data) == int(example.answer_a)
    # assert part_2(example.input_data) == int(example.answer_b)

    input_data = puzzle.input_data
    puzzle.answer_a = part_1(input_data)
    # puzzle.answer_b = part_2(input_data)
    # print(f"{puzzle.answer_a=}, {puzzle.answer_b=}")


if __name__ == "__main__":
    main()
