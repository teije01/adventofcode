"""
--- Day 14: Extended Polymerization ---

The incredible pressures at this depth are starting to put a strain on your submarine. The
submarine has polymerization equipment that would produce suitable materials to reinforce the
submarine, and the nearby volcanically-active caves should even have the necessary input elements
in sufficient quantities.

The submarine manual contains instructions for finding the optimal polymer formula; specifically,
it offers a polymer template and a list of pair insertion rules (your puzzle input). You just need
to work out what polymer would result after repeating the pair insertion process a few times.

For example:

NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C

The first line is the polymer template - this is the starting point of the process.

The following section defines the pair insertion rules. A rule like AB -> C means that when
elements A and B are immediately adjacent, element C should be inserted between them. These
insertions all happen simultaneously.

So, starting with the polymer template NNCB, the first step simultaneously considers all three
pairs:

    The first pair (NN) matches the rule NN -> C, so element C is inserted between the first N and
    the second N.

    The second pair (NC) matches the rule NC -> B, so element B is inserted between the N and the C.

    The third pair (CB) matches the rule CB -> H, so element H is inserted between the C and the B.

Note that these pairs overlap: the second element of one pair is the first element of the next
pair. Also, because all pairs are considered simultaneously, inserted elements are not considered
to be part of a pair until the next step.

After the first step of this process, the polymer becomes NCNBCHB.

Here are the results of a few steps using the above rules:

Template:     NNCB
After step 1: NCNBCHB
After step 2: NBCCNBBBCBHCB
After step 3: NBBBCNCCNBBNBNBBCHBHHBCHB
After step 4: NBBNBNBBCCNBCNCCNBBNBBNBBBNBBNBBCBHCBHHNHCBBCBHCB

This polymer grows quickly. After step 5, it has length 97; After step 10, it has length 3073.
After step 10, B occurs 1749 times, C occurs 298 times, H occurs 161 times, and N occurs 865 times;
taking the quantity of the most common element (B, 1749) and subtracting the quantity of the least
common element (H, 161) produces 1749 - 161 = 1588.

Apply 10 steps of pair insertion to the polymer template and find the most and least common
elements in the result. What do you get if you take the quantity of the most common element and
subtract the quantity of the least common element?

"""
from collections import Counter
import itertools
from typing import Dict, Tuple


def mutate_polymer(polymer, pattern_mapper):
    """
    Sequence new polymer based on the previous polymer (slow for large polymers)
    """
    polymer_list = [polymer[0]] + [None] * (len(polymer) * 2 - 2)
    for position in range(1, len(polymer)):
        polymer_list[position * 2 - 1] = pattern_mapper.get(polymer[position - 1 : position + 1])
        polymer_list[position * 2] = polymer[position]

    return str.join("", polymer_list)


def update_polymer_counters(
    triple_counts: Counter,
    mutation_mapper: Dict[str, str],
    inverse_mutation_mapper: Dict[str, Tuple[str, str]],
) -> Tuple[Counter, Counter]:
    """Polymer update duo counts"""
    duo_counts = Counter()
    for triple, count in triple_counts.items():
        duo_counts.update({duo: count for duo in inverse_mutation_mapper[triple]})
    triple_counts = Counter({mutation_mapper[duo]: count for duo, count in duo_counts.items()})
    return duo_counts, triple_counts


def distill_final_count(duo_counter: Counter, polymer: str) -> Counter:
    """Distill final counter"""
    double_final_count = Counter(polymer[0] + polymer[-1])
    for chars, count in duo_counter.items():
        for char in chars:
            double_final_count.update({char: count})
    final_counter = Counter({char: count//2 for char, count in double_final_count.items()})
    return final_counter


if __name__ == "__main__":

    with open("solutions/2021/day14/input.txt", "r") as f:
        template, pattern_mapper_txt = f.read().split("\n\n")

    pattern_combinations = [pattern.split(" -> ") for pattern in pattern_mapper_txt.splitlines()]
    pattern_mapper_ = {pattern[0]: pattern[1] for pattern in pattern_combinations}
    mutation_mapper_ = {key: key[0] + val + key[1] for key, val in pattern_mapper_.items()}
    inverse_mutation_mapper_ = {val: (val[:2], val[1:]) for val in mutation_mapper_.values()}

    # step 0
    duo_counts_ = Counter("".join(pair) for pair in itertools.pairwise(template))
    triple_counts_ = Counter({mutation_mapper_[duo]: count for duo, count in duo_counts_.items()})

    for step in range(1, 10+1):
        duo_counts_, triple_counts_ = update_polymer_counters(triple_counts_, mutation_mapper_, inverse_mutation_mapper_)
    polymer_counter_10 = distill_final_count(duo_counts_, template)
    for step in range(11, 40+1):
        duo_counts_, triple_counts_ = update_polymer_counters(triple_counts_, mutation_mapper_, inverse_mutation_mapper_)
    polymer_counter_40 = distill_final_count(duo_counts_, template)

    print(f"Answer 1: {max(polymer_counter_10.values()) - min(polymer_counter_10.values())}")
    print(f"Answer 2: {max(polymer_counter_40.values()) - min(polymer_counter_40.values())}")
