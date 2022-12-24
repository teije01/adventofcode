"""
https://adventofcode.com/2022/day/20
"""
from dataclasses import dataclass


@dataclass
class CoordinateSequence:
    sequence: list[int]

    def decrypt(self, multiply: int = 1, iterations: int = 1):
        decrypted_sequence = [i * multiply for i in self.sequence]
        ordering = list(range(len(decrypted_sequence)))
        for iteration in range(iterations):
            for turn in range(len(decrypted_sequence)):
                i_to_move = ordering.index(turn)
                value, rank = decrypted_sequence.pop(i_to_move), ordering.pop(i_to_move)
                new_position = (i_to_move + value) % len(decrypted_sequence)
                decrypted_sequence.insert(new_position, value)
                ordering.insert(new_position, rank)
        return decrypted_sequence


if __name__ == "__main__":

    with open("solutions/2022/day20/input.txt", "r") as f:
        sequence = list(map(int, f.read().rstrip("\n").split("\n")))

    cs = CoordinateSequence(sequence)
    decrypted_sequence_1 = cs.decrypt()
    decrypted_sequence_2 = cs.decrypt(multiply=811589153, iterations=10)

    zero_index_1 = decrypted_sequence_1.index(0)
    coordinate_sum_1 = sum(
        decrypted_sequence_1[(zero_index_1 + i) % len(decrypted_sequence_1)]
        for i in [1000, 2000, 3000]
    )

    zero_index_2 = decrypted_sequence_2.index(0)
    coordinate_sum_2 = sum(
        decrypted_sequence_2[(zero_index_2 + i) % len(decrypted_sequence_2)]
        for i in [1000, 2000, 3000]
    )

    print(f"Solution 1: {coordinate_sum_1}")
    print(f"Solution 2: {coordinate_sum_2}")
