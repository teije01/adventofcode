"""
https://adventofcode.com/2022/day/12
"""
from typing import Optional

import numpy as np


class PathFinder:
    def __init__(self, dem: np.ndarray, start_elevation: int, maximum_step_up: Optional[int]):
        self.dem = dem
        self.step_arr = np.full_like(dem, -1, dtype=int)
        self.step_arr[self.dem == start_elevation] = 0
        self.step_i = 0
        self.shape = dem.shape
        self.maximum_step_up = maximum_step_up

    def _filter(
            self,
            x_i: np.ndarray,
            y_j: np.ndarray,
            elevation_at_current_positions: np.ndarray,
    ):
        inside_array_mask = ~(
            (x_i < 0) | (y_j < 0) | (x_i > self.shape[1] - 1) | (y_j > self.shape[0] - 1)
        )
        xi_step, yi_step = x_i[inside_array_mask], y_j[inside_array_mask]
        no_previous_step_mask = self.step_arr[yi_step, xi_step] == -1
        if self.maximum_step_up is not None:
            maximum_elevation_constraint = (
                self.dem[yi_step, xi_step] - elevation_at_current_positions[inside_array_mask]
            ) <= 1
            mask = no_previous_step_mask & maximum_elevation_constraint
            return xi_step[mask], yi_step[mask]
        return xi_step[no_previous_step_mask], yi_step[no_previous_step_mask]

    def step(self):
        move_positions = self.step_arr == self.step_i
        yi, xi = np.where(move_positions)
        xi_step = (xi[:, None] + np.array([-1, 1, 0, 0])[None, :]).flatten()
        yi_step = (yi[:, None] + np.array([0, 0, -1, 1])[None, :]).flatten()
        elevation_at_current_positions = (
            self.dem[move_positions][:, None] + np.array([0, 0, 0, 0])[None, :]
        ).flatten()
        xi_step, yi_step = self._filter(xi_step, yi_step, elevation_at_current_positions)
        self.step_i += 1
        self.step_arr[yi_step, xi_step] = self.step_i
        return xi_step.size

    def find_minimum_steps_to_positions(self):
        while self.step():
            pass

    def report_minimum_steps_for_position(self, position_ij):
        return self.step_arr[position_ij]


if __name__ == "__main__":
    with open("solutions/2022/day12/input.txt", "r") as f:
        dem = np.array([list(map(ord, line)) for line in f.read().rstrip("\n").split("\n")])

    end_ij = tuple(map(np.ndarray.item, np.where(dem == ord("E"))))
    dem[dem == ord("S")] = ord("a") - 1
    dem[dem == ord("E")] = ord("z") + 1

    pf_s = PathFinder(dem, start_elevation=ord("a") - 1, maximum_step_up=1)
    pf_s.find_minimum_steps_to_positions()

    pf_a = PathFinder(dem, start_elevation=ord("a"), maximum_step_up=1)
    pf_a.find_minimum_steps_to_positions()

    print(f"Solution 1: {pf_s.report_minimum_steps_for_position(end_ij)}")
    print(f"Solution 2: {pf_a.report_minimum_steps_for_position(end_ij)}")
