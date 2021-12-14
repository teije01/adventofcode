"""
--- Day 13: Transparent Origami ---

You reach another volcanically active part of the cave. It would be nice if you could do some kind
of thermal imaging so you could tell ahead of time which caves are too hot to safely enter.

Fortunately, the submarine seems to be equipped with a thermal camera! When you activate it, you
are greeted with:

Congratulations on your purchase! To activate this infrared thermal imaging
camera system, please enter the code found on page 1 of the manual.

Apparently, the Elves have never used this feature. To your surprise, you manage to find the
manual; as you go to open it, page 1 falls out. It's a large sheet of transparent paper! The
transparent paper is marked with random dots and includes instructions on how to fold it up (your
puzzle input). For example:

6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5

The first section is a list of dots on the transparent paper. 0,0 represents the top-left
coordinate. The first value, x, increases to the right. The second value, y, increases downward.
So, the coordinate 3,0 is to the right of 0,0, and the coordinate 0,7 is below 0,0. The coordinates
in this example form the following pattern, where # is a dot on the paper and . is an empty,
unmarked position:

...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
...........
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........

Then, there is a list of fold instructions. Each instruction indicates a line on the transparent
paper and wants you to fold the paper up (for horizontal y=... lines) or left (for vertical x=...
lines). In this example, the first fold instruction is fold along y=7, which designates the line
formed by all of the positions where y is 7 (marked here with -):

...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
-----------
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........

Because this is a horizontal line, fold the bottom half up. Some of the dots might end up
overlapping after the fold is complete, but dots will never appear exactly on a fold line. The
result of doing this fold looks like this:

#.##..#..#.
#...#......
......#...#
#...#......
.#.#..#.###
...........
...........

Now, only 17 dots are visible.

Notice, for example, the two dots in the bottom left corner before the transparent paper is folded;
after the fold is complete, those dots appear in the top left corner (at 0,0 and 0,1). Because the
paper is transparent, the dot just below them in the result (at 0,3) remains visible, as it can be
seen through the transparent paper.

Also notice that some dots can end up overlapping; in this case, the dots merge together and become
a single dot.

The second fold instruction is fold along x=5, which indicates this line:

#.##.|#..#.
#...#|.....
.....|#...#
#...#|.....
.#.#.|#.###
.....|.....
.....|.....

Because this is a vertical line, fold left:

#####
#...#
#...#
#...#
#####
.....
.....

The instructions made a square!

The transparent paper is pretty big, so for now, focus on just completing the first fold. After the
first fold in the example above, 17 dots are visible - dots that end up overlapping after the fold
is completed count as a single dot.

How many dots are visible after completing just the first fold instruction on your transparent
paper?

--- Part Two ---

Finish folding the transparent paper according to the instructions. The manual says the code is
always eight capital letters.

What code do you use to activate the infrared thermal imaging camera system?

"""
import re
from collections import namedtuple
from typing import List

import numpy as np

Coord = namedtuple("Coord", ["x", "y"])
Fold = namedtuple("Fold", ["direction", "value"])
fold_pattern = re.compile(r"fold along (?P<direction>[xy])=(?P<value>\d{1,4})")


def create_coord_mask(coordinates: List[Coord]) -> np.ndarray:
    """Create coordinate mask from list of coordinates"""
    x_max = max(coordinates, key=lambda c: c.x).x
    y_max = max(coordinates, key=lambda c: c.y).y
    image = np.full((y_max + 1, x_max + 1), False, dtype=bool)
    for coordinate in coordinates:
        image[coordinate.y, coordinate.x] = True
    return image


def fold_paper(image: np.ndarray, direction: str, value: int) -> np.ndarray:
    """Fold dotted paper"""
    match direction:
        case "x":
            left = image[:, :value].copy()
            right = image[:, :value:-1].copy()  # flipped
            if left.shape[1] >= right.shape[1]:
                folded_image = left
                folded_image[:, right.shape[1]-left.shape[1]:] |= right[:, :]
            else:
                folded_image = right[:, ::-1]
                folded_image[:, right.shape[1]-left.shape[1]:] |= left[:, :]

        case "y":
            top = image[:value, :].copy()
            bottom = image[:value:-1, :].copy()  # flipped
            if top.shape[0] >= bottom.shape[0]:
                folded_image = top
                folded_image[top.shape[0]-bottom.shape[0]:, :] |= bottom[:, :]
            else:
                folded_image = bottom[::-1]
                folded_image[bottom.shape[0]-top.shape[0]:, :] |= top[:, :]

        case _:
            raise ValueError("direction can only be 'x' or 'y'")
    return folded_image


if __name__ == "__main__":

    with open("solutions/2021/day13/input.txt", "r") as f:
        coords_txt, folds_txt = f.read().split("\n\n")

    coords = [Coord(*map(int, coord.split(","))) for coord in coords_txt.splitlines()]
    folds = [
        Fold(match["direction"], int(match["value"])) for match in fold_pattern.finditer(folds_txt)
    ]
    dotted_transparent_paper = create_coord_mask(coords)
    first_folded_paper = fold_paper(
        dotted_transparent_paper,
        direction=folds[0].direction,
        value=folds[0].value,
    )
    folded_paper = first_folded_paper
    for fold in folds[1:]:
        folded_paper = fold_paper(
            folded_paper,
            direction=fold.direction,
            value=fold.value,
        )

    folded_letters = "\n".join(
        ("".join("$$" if char else "  " for char in line) for line in folded_paper)
    )
    print(f"Answer 1: {np.sum(first_folded_paper)}")
    print(f"Answer 2:\n{folded_letters}")
