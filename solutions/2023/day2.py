"""
https://adventofcode.com/2023/day/2
"""
import re
from dataclasses import dataclass
from aocd.models import Puzzle


@dataclass
class CubeSet:
    red: int = 0
    green: int = 0
    blue: int = 0

    def __contains__(self, item: "CubeSet") -> bool:
        return (
            self.red >= item.red and self.green >= item.green and self.blue >= item.blue
        )

    def product(self) -> int:
        return (self.red or 1) * (self.blue or 1) * (self.green or 1)


@dataclass
class Game:
    game_id: int
    cube_sets: list[CubeSet]

    def max_cubes_used(self) -> CubeSet:
        max_red = max(cs.red for cs in self.cube_sets)
        max_green = max(cs.green for cs in self.cube_sets)
        max_blue = max(cs.blue for cs in self.cube_sets)
        return CubeSet(red=max_red, green=max_green, blue=max_blue)


def parse_game(game_line: str) -> Game:
    game_id_part, games_str = game_line.split(":")
    game_id = int(re.match(r"Game (\d+)", game_id_part).group(1))
    cube_sets = [
        CubeSet(
            **{
                m["color"]: int(m["amount"])
                for m in re.finditer(r"(?P<amount>\d+) (?P<color>\w+)", cube_set_part)
            }
        )
        for cube_set_part in games_str.split(";")
    ]
    game = Game(game_id, cube_sets)
    return game


def part_1_and_2(input_data: str) -> tuple[int, int]:
    games = [parse_game(game_line) for game_line in input_data.split("\n")]

    available_cubes = CubeSet(12, 13, 14)
    answer_1 = sum(
        game.game_id for game in games if game.max_cubes_used() in available_cubes
    )
    answer_2 = sum(game.max_cubes_used().product() for game in games)
    return answer_1, answer_2


def main():
    puzzle = Puzzle(day=2, year=2023)

    example, = puzzle.examples
    assert part_1_and_2(example.input_data) == (int(example.answer_a), int(example.answer_b))

    input_data = puzzle.input_data
    puzzle.answer_a, puzzle.answer_b = part_1_and_2(input_data)
    print(f"{puzzle.answer_a=}, {puzzle.answer_b=}")


if __name__ == "__main__":
    main()
