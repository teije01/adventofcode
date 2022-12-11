"""
https://adventofcode.com/2022/day/10
"""
from dataclasses import dataclass, field
from functools import partial


@dataclass
class CRT:
    shape: tuple[int, int]
    line: int = field(default=0)
    x: int = field(default=0)
    monitor: list[list[str]] = field(init=False, repr=False)

    def __post_init__(self):
        self.monitor = [[' '] * self.shape[1] for _line in range(self.shape[0])]

    def __str__(self):
        return '\n'.join([''.join(line) for line in self.monitor])

    def draw(self, char: str):
        self.monitor[self.line][self.x] = char
        self.x = (self.x + 1) % self.shape[1]
        if self.x == 0:
            self.line += 1


@dataclass
class ClockCircuit:
    X: int = field(default=1)
    cycles: int = field(default=0)
    crt: CRT = field(default_factory=partial(CRT, (6, 40)), repr=False)

    def _tick(self, addx: int | None = None):
        self.cycles += 1
        yield self.cycles
        if addx is not None:
            self.cycles += 1
            yield self.cycles
            self.X += addx

    @property
    def signal_strength(self) -> int:
        return self.cycles * self.X

    @property
    def sprite(self) -> range:
        return range(self.X - 1, self.X + 2)

    def run(self, instruction_list: list[str], yield_for: range):
        for instruction in instruction_list:
            match instruction.split(' '):
                case ['noop']:
                    cycler = self._tick()
                case ['addx', value]:
                    cycler = self._tick(addx=int(value))
                case _:
                    raise ValueError(f"Unknown instruction: {instruction}")
            for cycle in cycler:
                char = '#' if self.crt.x in self.sprite else " "
                self.crt.draw(char)
                if cycle in yield_for:
                    yield self.signal_strength


if __name__ == "__main__":

    with open("solutions/2022/day10/input.txt", "r") as f:
        instructions = [instruction for instruction in f.read().rstrip("\n").split("\n")]

    cc = ClockCircuit()
    signal_strengths = [ss for ss in cc.run(instructions, yield_for=range(20, 221, 40))]

    print(f"Solution 1: {sum(signal_strengths)}")
    print(f"Solution 2: \n{cc.crt}")
