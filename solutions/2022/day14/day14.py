"""
https://adventofcode.com/2022/day/14
"""
from collections import namedtuple
from typing import Optional

import numpy as np

Coordinate = namedtuple("Coordinate", ["x", "y"])


class AbyssEncontered(Exception):
    pass


class DepositionBlocked(Exception):
    pass


def drop_sand(cave_arr: np.ndarray, column_candidate: int, row_candidate: Optional[int] = None):
    if column_candidate in {0, cave_arr.shape[1]}:
        raise AbyssEncontered()
    if row_candidate is None:
        solid, = cave_arr[:, column_candidate].nonzero()
        row_candidate = solid[0] - 1
        if row_candidate == -1:
            raise DepositionBlocked()
    if row_candidate == cave_arr.shape[0] - 1:
        raise AbyssEncontered()
    support = cave_arr[row_candidate + 1, column_candidate-1:column_candidate+2]
    if all(support > 0):
        cave_arr[row_candidate, column_candidate] = 1
    elif support[1] == 0: # move down
        drop_sand(cave_arr, column_candidate, row_candidate + 1)
    elif support[0] == 0:  # move left
        drop_sand(cave_arr, column_candidate - 1, row_candidate + 1)
    elif support[2] == 0:  # move right
        drop_sand(cave_arr, column_candidate + 1, row_candidate + 1)


if __name__ == "__main__":

    with open("solutions/2022/day14/input.txt", "r") as f:
        coordinate_sequence_list = []
        for line in f.read().rstrip("\n").split("\n"):
            coordinate_sequence_list.append(
                [Coordinate(*map(int, coord.split(","))) for coord in line.split(" -> ")]
            )

    min_y = 0
    max_y = max(max(coord_seq, key=lambda c: c.y).y for coord_seq in coordinate_sequence_list)
    min_x = min(min(coord_seq, key=lambda c: c.x).x for coord_seq in coordinate_sequence_list)
    max_x = max(max(coord_seq, key=lambda c: c.x).x for coord_seq in coordinate_sequence_list)

    sand_discharge_loc = Coordinate(500, 0)

    shape1 = max_y - min_y + 1, max_x - min_x + 1
    cave1 = np.zeros(shape1, int)
    for coord_seq in coordinate_sequence_list:
        for c1, c2 in zip(coord_seq[1:], coord_seq[:-1]):
            row_slice = slice(min(c1.y, c2.y) - min_y, max(c1.y, c2.y) - min_y + 1)
            col_slice = slice(min(c1.x, c2.x) - min_x, max(c1.x, c2.x) - min_x + 1)
            cave1[(row_slice, col_slice)] = 2
    required_width = 1 + 2 * (shape1[0] + 2)  # width of the floor around the deposition
    add_left = required_width // 2 + (min_x - sand_discharge_loc.x)
    add_right = required_width // 2 + (sand_discharge_loc.x - max_x)
    add_bottom = 2
    add_top = 0
    cave2 = np.pad(cave1, ((add_top, add_bottom), (add_left, add_right)))
    cave2[-1, :] = 2

    sand_units1 = 0
    while True:
        try:
            drop_sand(cave1, sand_discharge_loc.x - min_x)
            sand_units1 += 1
        except AbyssEncontered:
            break

    sand_units2 = 0
    while True:
        try:
            drop_sand(cave2, sand_discharge_loc.x - min_x + add_left)
            sand_units2 += 1
        except DepositionBlocked:
            break

    print(f"Solution 1: {sand_units1}")
    print(f"Solution 2: {sand_units2}")

    # plt.imshow(cave1, extent=(min_x, max_x, cave1.shape[0], 0 ))
    # plt.imshow(cave2, extent=(min_x - add_left, max_x + add_right, cave2.shape[0], 0 ))
