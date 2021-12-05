"""
--- Day 5: Hydrothermal Venture ---

You come across a field of hydrothermal vents on the ocean floor! These vents constantly produce
large, opaque clouds, so it would be best to avoid them if possible.

They tend to form in lines; the submarine helpfully produces a list of nearby lines of vents (your
puzzle input) for you to review. For example:

0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2

Each line of vents is given as a line segment in the format x1,y1 -> x2,y2 where x1,y1 are the
coordinates of one end the line segment and x2,y2 are the coordinates of the other end. These line
segments include the points at both ends. In other words:

    An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
    An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.

For now, only consider horizontal and vertical lines: lines where either x1 = x2 or y1 = y2.

So, the horizontal and vertical lines from the above list would produce the following diagram:

.......1..
..1....1..
..1....1..
.......1..
.112111211
..........
..........
..........
..........
222111....

In this diagram, the top left corner is 0,0 and the bottom right corner is 9,9. Each position is
shown as the number of lines which cover that point or . if no line covers that point. The top-left
pair of 1s, for example, comes from 2,2 -> 2,1; the very bottom row is formed by the overlapping
lines 0,9 -> 5,9 and 0,9 -> 2,9.

To avoid the most dangerous areas, you need to determine the number of points where at least two
lines overlap. In the above example, this is anywhere in the diagram with a 2 or larger - a total
of 5 points.

Consider only horizontal and vertical lines. At how many points do at least two lines overlap?

--- Part Two ---

Unfortunately, considering only horizontal and vertical lines doesn't give you the full picture;
you need to also consider diagonal lines.

Because of the limits of the hydrothermal vent mapping system, the lines in your list will only
ever be horizontal, vertical, or a diagonal line at exactly 45 degrees. In other words:

    An entry like 1,1 -> 3,3 covers points 1,1, 2,2, and 3,3.
    An entry like 9,7 -> 7,9 covers points 9,7, 8,8, and 7,9.

Considering all lines from the above example would now produce the following diagram:

1.1....11.
.111...2..
..2.1.111.
...1.2.2..
.112313211
...1.2....
..1...1...
.1.....1..
1.......1.
222111....

You still need to determine the number of points where at least two lines overlap. In the above
example, this is still anywhere in the diagram with a 2 or larger - now a total of 12 points.

Consider all of the lines. At how many points do at least two lines overlap?

"""
import numpy as np


class Line:
    """Line representation"""
    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    @classmethod
    def from_puzzle_input(cls, line: str):
        x1y1, x2y2 = line.split(" -> ")
        return cls(*map(int, x1y1.split(",")), *map(int, x2y2.split(",")))

    @property
    def xmin(self):
        return min(self.x1, self.x2)

    @property
    def xmax(self):
        return max(self.x1, self.x2)

    @property
    def ymin(self):
        return min(self.y1, self.y2)

    @property
    def ymax(self):
        return max(self.y1, self.y2)


if __name__ == "__main__":

    with open("solutions/2021/day5/input.txt", "r") as f:
        lines = f.read().splitlines()

    lines = [Line.from_puzzle_input(line) for line in lines]
    straight_field = np.zeros((1000, 1000), dtype=int)
    diagonal_field = straight_field.copy()
    for line in lines:
        field_index = (slice(line.ymin, line.ymax + 1), slice(line.xmin, line.xmax + 1))
        if line.x1 == line.x2 or line.y1 == line.y2:
            straight_field[field_index] += 1
        else:
            is_identity = (line.x2 - line.x1 > 0) == (line.y2 - line.y1 > 0)
            diag_slice = slice(None, None, None if is_identity else -1)
            diagonal_field[field_index] += np.diag(np.ones((line.xmax - line.xmin + 1), dtype=int))[diag_slice]

    field = straight_field + diagonal_field
    print(f"Answer 1: {np.sum(straight_field > 1)}")
    print(f"Answer 2: {np.sum(field > 1)}")
