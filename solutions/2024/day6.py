"""
https://adventofcode.com/2024/day/6
"""
from itertools import cycle

import numpy as np
from io import StringIO
from aocd.models import Puzzle


class InfiniteLoop(Exception):
    pass


def read_input_array(input_data) -> np.ndarray:
    int_buffer = StringIO(input_data.translate(str.maketrans({".": "0 ", "#": "-1 ", "^": "1 "})))
    lab_arr = np.loadtxt(int_buffer, dtype=int, )
    return lab_arr


def walk_pattern(lab_array: np.ndarray) -> np.ndarray:
    lab_array = lab_array
    [row], [col] = np.where(lab_array == 1)
    new_direction = cycle("URDL")  # up right down left
    pivot_points = set()
    for i, direction in enumerate(new_direction, start=1):
        pivot_point = (direction, row.item(), col.item())
        if pivot_point in pivot_points:
            raise InfiniteLoop()
        pivot_points.add(pivot_point)
        try:
            if direction == "U":
                obstruction_up = np.where(lab_array[row::-1, col] == -1)[0][0]
                lab_array[row:row - obstruction_up:-1, col] = i
                row = row - obstruction_up + 1
            elif direction == "R":
                obstruction_right = np.where(lab_array[row, col:] == -1)[0][0]
                lab_array[row, col:col + obstruction_right] = i
                col = col + obstruction_right - 1
            elif direction == "D":
                obstruction_down = np.where(lab_array[row:, col] == -1)[0][0]
                lab_array[row:row + obstruction_down, col] = i
                row = row + obstruction_down - 1
            elif direction == "L":
                obstruction_left = np.where(lab_array[row, col::-1] == -1)[0][0]
                lab_array[row, col:col - obstruction_left:-1] = i
                col = col - obstruction_left + 1
        except IndexError:
            break  # out of bounds
    if direction == "U":
        lab_array[row::-1, col] = i
    elif direction == "R":
        lab_array[row, col:] = i
    elif direction == "D":
        lab_array[row:, col] = i
    elif direction == "L":
        lab_array[row, col::-1] = i
    return lab_array


def part_1(input_data) -> int:
    lab_array = read_input_array(input_data)
    lab_walked_arr = walk_pattern(lab_array.copy())
    distinct_locations = (lab_walked_arr > 0).sum()
    return distinct_locations


def part_2(input_data) -> int:
    lab_array = read_input_array(input_data)
    lab_walked_arr = walk_pattern(lab_array.copy())
    lab_walked_arr[lab_array == 1] = 0  # reset start position
    n_inf_loops = 0
    for row, col in zip(*np.where(lab_walked_arr > 0)):
        new_lab_array = lab_array.copy()
        new_lab_array[row, col] = -1
        try:
            new_lab_walked_arr = walk_pattern(new_lab_array)
        except InfiniteLoop:
            n_inf_loops += 1
    return n_inf_loops


def main():
    puzzle = Puzzle(day=6, year=2024)

    example, = puzzle.examples
    assert part_1(example.input_data) == int(example.answer_a)
    assert part_2(example.input_data) == 6

    input_data = puzzle.input_data
    puzzle.answer_a = part_1(input_data)
    puzzle.answer_b = part_2(input_data)
    print(f"{puzzle.answer_a=}, {puzzle.answer_b=}")


if __name__ == "__main__":
    main()
