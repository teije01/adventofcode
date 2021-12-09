"""
--- Day 9: Smoke Basin ---

These caves seem to be lava tubes. Parts are even still volcanically active; small hydrothermal
vents release smoke into the caves that slowly settles like rain.

If you can model how the smoke flows through the caves, you might be able to avoid it and be that
much safer. The submarine generates a heightmap of the floor of the nearby caves for you (your
puzzle input).

Smoke flows to the lowest point of the area it's in. For example, consider the following heightmap:

2199943210
3987894921
9856789892
8767896789
9899965678

Each number corresponds to the height of a particular location, where 9 is the highest and 0 is the
lowest a location can be.

Your first goal is to find the low points - the locations that are lower than any of its adjacent
locations. Most locations have four adjacent locations (up, down, left, and right); locations on
the edge or corner of the map have three or two adjacent locations, respectively. (Diagonal
locations do not count as adjacent.)

In the above example, there are four low points, all highlighted: two are in the first row (a 1 and
a 0), one is in the third row (a 5), and one is in the bottom row (also a 5). All other locations
on the heightmap have some lower adjacent location, and so are not low points.

The risk level of a low point is 1 plus its height. In the above example, the risk levels of the
low points are 2, 1, 6, and 6. The sum of the risk levels of all low points in the heightmap is
therefore 15.

Find all of the low points on your heightmap. What is the sum of the risk levels of all low points
on your heightmap?

--- Part Two ---

Next, you need to find the largest basins so you know what areas are most important to avoid.

A basin is all locations that eventually flow downward to a single low point. Therefore, every low
point has a basin, although some basins are very small. Locations of height 9 do not count as being
in any basin, and all other locations will always be part of exactly one basin.

The size of a basin is the number of locations within the basin, including the low point. The
example above has four basins.

The top-left basin, size 3:

2199943210
3987894921
9856789892
8767896789
9899965678

The top-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678

The middle basin, size 14:

2199943210
3987894921
9856789892
8767896789
9899965678

The bottom-right basin, size 9:

2199943210
3987894921
9856789892
8767896789
9899965678

Find the three largest basins and multiply their sizes together. In the above example, this is
9 * 14 * 9 = 1134.

What do you get if you multiply together the sizes of the three largest basins?

"""
from scipy import ndimage
import numpy as np

with open("solutions/2021/day9/input.txt", "r") as f:
    dem = np.array([[*map(int, line)] for line in f.read().splitlines()])

adjacent = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
lowest_neighbor = ndimage.rank_filter(dem, 1, footprint=adjacent, mode="constant", cval=9.0)
low_points_mask = dem < lowest_neighbor

basins_mask = ndimage.binary_dilation(low_points_mask, structure=adjacent, iterations=-1, mask=dem != 9)
basins, n_basins = ndimage.label(basins_mask, structure=adjacent)
basin_nrs, basin_sizes = np.unique(basins[basins>0], return_counts=True)

print(f"Answer 1: {np.sum(dem[low_points_mask] + 1)}")
print(f"Answer 2: {np.product(basin_sizes[np.argsort(basin_sizes)[-3:]])}")
