"""
https://adventofcode.com/2022/day/15
"""
from dataclasses import dataclass
from typing import Iterator, Optional

import numpy as np
import re


@dataclass
class BeaconSensor:
    sx: int
    sy: int
    bx: int
    by: int

    @property
    def manhattan_distance(self) -> int:
        return abs(self.sx - self.bx) + abs(self.sy - self.by)

    def x_range_for_y(self, y: int) -> Optional[range]:
        x_width = self.manhattan_distance - abs(self.sy - y)
        if x_width <= 0:
            return None
        return range(self.sx - x_width, self.sx + x_width + 1)

    def xy_in_sensor_range(self, x: int, y: int):
        return self.manhattan_distance >= (abs(self.sx - x) + abs(self.sy - y))


def x_ranges_for_y(beacon_sensors: list[BeaconSensor], y: int) -> Iterator[range]:
    for bs in beacon_sensors:
        x_range = bs.x_range_for_y(y)
        if x_range is not None:
            yield x_range


def overlapping_range_length(r1: range, r2: range) -> int:
    orl = 0
    if r2.start <= r1.start < r2.stop:
        orl = min(r1.stop, r2.stop) - r1.start
    elif r1.start < r2.start < r1.stop:
        orl = min(r1.stop, r2.stop) - r2.start
    return orl


def compressed_xrange_for_y(beacon_sensors: list[BeaconSensor], y: int) -> tuple[list[list[int, int]], int]:
    x_ranges = list(x_ranges_for_y(beacon_sensors, y))
    x_ranges.sort(key=lambda xr: xr.start)
    minimum_overlap = None
    stack = [[x_ranges[0].start, x_ranges[0].stop]]
    for i, x_range in enumerate(x_ranges[1:], start=1):
        x_range_max_overlap_left = max(overlapping_range_length(x_range, x_range_cmp) for x_range_cmp in x_ranges[:i])
        minimum_overlap = x_range_max_overlap_left if minimum_overlap is None else min(x_range_max_overlap_left, minimum_overlap)
        if x_range.start < stack[-1][1]:
            stack[-1][1] = max(stack[-1][1], x_range.stop)
        else:
            stack.append([x_range.start, x_range.stop])
    if minimum_overlap is None:
        minimum_overlap = 0
    return stack, max(1, minimum_overlap // 2)


loc_matcher = re.compile(
    r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
)


if __name__ == "__main__":

    with open("solutions/2022/day15/input.txt", "r") as f:
        beacon_sensors = [
            BeaconSensor(*map(int, loc_matcher.match(line).groups()))
            for line in f.read().rstrip("\n").split("\n")
        ]

    y = 2_000_000
    tuning_x_multiplier = 4_000_000
    xy_bounds = range(0, 4_000_000 + 1)

    impossible_x_positions_at_y = set.union(
        *[set(x_range) for x_range in x_ranges_for_y(beacon_sensors, y)]
    ).difference([sb.bx for sb in beacon_sensors if sb.by == y])

    tuning_frequency = None
    y = 4_000_000 - 1
    while True:

        compresed_xranges, stepsize = compressed_xrange_for_y(beacon_sensors, y)
        if len(compresed_xranges) == 1 and compresed_xranges[0][0] < xy_bounds.start and compresed_xranges[0][1] > (xy_bounds.stop - 1):
            pass
        else:
            print("Non consecutive bounds encountered")
            x_gap = compresed_xranges[0][1]
            tuning_frequency = y + x_gap * 4_000_000
            break
        y -= stepsize

    print(f"Solution 1: {len(impossible_x_positions_at_y)}")
    print(f"Solution 2: {tuning_frequency}")
