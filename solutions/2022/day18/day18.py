"""
https://adventofcode.com/2022/day/18
"""
import numpy as np
from scipy.signal import convolve
from scipy.ndimage import binary_fill_holes


if __name__ == "__main__":

    x, y, z = np.loadtxt("solutions/2022/day18/input.txt", dtype=int, delimiter=",").T

    a = np.zeros((z.max() + 1, y.max() + 1, x.max() + 1), dtype=int)
    a[z, y, x] = 1

    k1 = np.array([[[1, -1]]])
    k2 = np.array([[[1], [-1]]])
    k3 = np.array([[[1]], [[-1]]])

    sides1 = (
        np.abs(convolve(a, k1, "full")).sum()
        + np.abs(convolve(a, k2, "full")).sum()
        + np.abs(convolve(a, k3, "full")).sum()
    )

    b = binary_fill_holes(a, structure=None).astype(int)
    sides2 = (
            np.abs(convolve(b, k1, "full")).sum()
            + np.abs(convolve(b, k2, "full")).sum()
            + np.abs(convolve(b, k3, "full")).sum()
    )

    print(f"Solution 1: {sides1}")
    print(f"Solution 2: {sides2}")
