"""
https://adventofcode.com/2022/day/9
"""
from dataclasses import dataclass


@dataclass
class Position:
    x: int
    y: int

    @property
    def xy(self):
        return self.x, self.y

    def move(self, x: int, y: int):
        self.x += x
        self.y += y


class HeadTails:
    _MOVE_X = {"L": -1, "R": 1}
    _MOVE_Y = {"D": -1, "U": 1}

    def __init__(self, n=1):
        self.head = Position(0, 0)
        self.head_positions = [self.head.xy]
        self.tails = [Position(0, 0) for _ in range(n)]
        self.tail_positions = {i: [tail.xy] for i, tail in enumerate(self.tails, 1)}

    def move_head(self, direction: str, steps: int):
        x_step = self._MOVE_X.get(direction, 0)
        y_step = self._MOVE_Y.get(direction, 0)
        for _i_step in range(steps):
            self.head.move(x_step, y_step)
            self._update_tails()
            self.head_positions.append(self.head.xy)
            for i, tail in enumerate(self.tails, 1):
                self.tail_positions[i].append(tail.xy)

    def _update_tails(self):
        head = self.head
        for tail in self.tails:
            if abs(head.x - tail.x) == 2 and abs(head.y - tail.y) == 2:
                tail.x = head.x - 1 + 2 * (head.x < tail.x)
                tail.y = head.y - 1 + 2 * (head.y < tail.y)
            elif abs(head.x - tail.x) == 2:
                tail.x = head.x - 1 + 2 * (head.x < tail.x)
                tail.y = head.y
            elif abs(head.y - tail.y) == 2:
                tail.x = head.x
                tail.y = head.y - 1 + 2 * (head.y < tail.y)
            head = tail


if __name__ == "__main__":

    with open("solutions/2022/day9/input.txt", "r") as f:
        instructions = [instruction.split(' ') for instruction in f.read().rstrip("\n").split("\n")]

    ht_1 = HeadTails()
    ht_10 = HeadTails(n=9)
    for direction, steps in instructions:
        ht_1.move_head(direction, int(steps))
        ht_10.move_head(direction, int(steps))

    print(f"Solution 1: {len(set(ht_1.tail_positions[1]))}")
    print(f"Solution 2: {len(set(ht_10.tail_positions[9]))}")
