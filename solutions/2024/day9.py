"""
https://adventofcode.com/2024/day/9
"""
from itertools import repeat, zip_longest
from operator import ge
from typing import Iterator, Generator

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


def find_indices(lst, condition, left_of_idx=None) -> Generator[int, None, None]:
    return (i for i, elem in enumerate(lst[:left_of_idx]) if condition(elem))


def greater_or_equal_func(compared_to):
    def greater_or_equal(element, compared_to=compared_to):
        return ge(element, compared_to)
    return greater_or_equal


def de_fragment_file_blocks(file_blocks: list[int], free_blocks: list[int]) -> list[int]:
    file_blocks = file_blocks.copy()
    free_blocks = free_blocks.copy()
    free_blocks.append(0)
    file_ids = list(range(len(file_blocks)))

    largest_free_space = max(free_blocks)
    back_idx = len(file_blocks) - 1  # start at the back and work to the left
    while back_idx > 0:

        file_blocks_to_move = file_blocks[back_idx]
        if file_blocks_to_move > largest_free_space:
            back_idx -= 1  # consider next file to move
            continue
        try:
            move_to_free_block_idx = next(
                find_indices(
                    free_blocks,
                    condition=greater_or_equal_func(file_blocks_to_move),
                    left_of_idx=back_idx
                )
            )
        except StopIteration:
            largest_free_space = max(b for b in free_blocks[:back_idx])
            back_idx -= 1  # consider next file to move
            continue

        # Adjust free blocks for the move of the file blocks
        free_blocks[move_to_free_block_idx] -= file_blocks_to_move  # free space decreases at destination
        free_blocks.insert(move_to_free_block_idx, 0)  # no free space between moved file and file before
        free_blocks[back_idx] += file_blocks_to_move + free_blocks.pop(back_idx + 1)  # merge free space where file was moved from
        # Move file blocks to the insert index (insert at free block + 1)
        file_blocks.insert(move_to_free_block_idx + 1, file_blocks.pop(back_idx))  # move file block to new position
        file_ids.insert(move_to_free_block_idx + 1, file_ids.pop(back_idx))  # move file_id to new position

    file_ids_out = []
    for file_block, free_block, file_id in zip(file_blocks, free_blocks, file_ids):
        file_ids_out.extend(repeat(file_id, file_block))
        file_ids_out.extend(repeat(0, free_block))
    return file_ids_out


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

    def de_fragment_files(self) -> "FileSystem":
        self.file_ids_compacted = de_fragment_file_blocks(self.file_blocks, self.free_blocks)

    @property
    def checksum(self) -> int:
        return sum(i * file_id for i, file_id in enumerate(self.file_ids_compacted))

def part_1(input_data) -> int:
    disk_map, = (FileSystem.from_disk_map(dm) for dm in input_data.split("\n"))
    disk_map.de_fragment_blocks()
    return disk_map.checksum


def part_2(input_data) -> int:
    disk_map, = (FileSystem.from_disk_map(dm) for dm in input_data.split("\n"))
    disk_map.de_fragment_files()
    return disk_map.checksum


def main():
    puzzle = Puzzle(day=9, year=2024)

    example, = puzzle.examples
    assert part_1(example.input_data) == int(example.answer_a)
    assert part_2(example.input_data) == 2858

    input_data = puzzle.input_data
    puzzle.answer_a = part_1(input_data)
    puzzle.answer_b = part_2(input_data)
    print(f"{puzzle.answer_a=}, {puzzle.answer_b=}")


if __name__ == "__main__":
    main()
