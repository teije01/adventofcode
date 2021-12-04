"""
--- Day 2: Dive! ---

Now, you need to figure out how to pilot this thing.

It seems like the submarine can take a series of commands like forward 1, down 2, or up 3:

    forward X increases the horizontal position by X units.
    down X increases the depth by X units.
    up X decreases the depth by X units.

Note that since you're on a submarine, down and up affect your depth, and so they have the opposite
result of what you might expect.

The submarine seems to already have a planned course (your puzzle input). You should probably
figure out where it's going. For example:

forward 5
down 5
forward 8
up 3
down 8
forward 2

Your horizontal position and depth both start at 0. The steps above would then modify them as
follows:

    forward 5 adds 5 to your horizontal position, a total of 5.
    down 5 adds 5 to your depth, resulting in a value of 5.
    forward 8 adds 8 to your horizontal position, a total of 13.
    up 3 decreases your depth by 3, resulting in a value of 2.
    down 8 adds 8 to your depth, resulting in a value of 10.
    forward 2 adds 2 to your horizontal position, a total of 15.

After following these instructions, you would have a horizontal position of 15 and a depth of 10.
(Multiplying these together produces 150.)

Calculate the horizontal position and depth you would have after following the planned course. What
do you get if you multiply your final horizontal position by your final depth?

"""
from operator import add, sub


class SubmarinePosition:
    """SubmarinePosition position tracker"""

    _directional_update = {
        "forward": add,
        "down": add,
        "up": sub,
    }

    def __init__(self, horizontal: int = 0, depth: int = 0, aim: int = 0):
        self.horizontal = horizontal
        self.depth = depth
        self.aim = aim

    def move(self, direction: str, units: int, aiming: bool = False):
        """Move units amount into direction"""
        update = self._directional_update[direction]
        if direction == "forward":
            self.horizontal = update(self.horizontal, units)
            if aiming:
                self.depth = update(self.depth, self.aim * units)
        elif aiming:
            self.aim = update(self.aim, units)
        else:
            self.depth = update(self.depth, units)

    @property
    def product(self):
        """Multiplication of horizontal position and depth"""
        return self.horizontal * self.depth


if __name__ == "__main__":

    with open("solutions/2021/day2/input.txt", "r") as f:
        controls = f.read().splitlines()

    position1 = SubmarinePosition()
    position2 = SubmarinePosition()
    for step in controls:
        step_direction, step_units = step.split(" ")
        position1.move(step_direction, int(step_units))
        position2.move(step_direction, int(step_units), aiming=True)
    print(f"Answer 1 should be: {position1.product}")
    print(f"Answer 2 should be: {position2.product}")
