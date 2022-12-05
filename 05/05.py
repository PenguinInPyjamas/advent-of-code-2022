import argparse
from collections import namedtuple
from copy import deepcopy

Instruction = namedtuple("Instruction", ["qty", "move_from", "move_to"])


def read_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    args = parser.parse_args()
    raw_stacks_string, raw_moves_string = "".join(open(args.input_file_path)).split("\n\n")

    moves = [Instruction(int(qty), int(move_from), int(move_to)) for _, qty, _, move_from, _, move_to
             in [s.strip().split(" ") for s in raw_moves_string.split("\n") if len(s) > 0]]
    return parse_stacks_input(raw_stacks_string), moves


def parse_stacks_input(stacks_string):
    stack_strings = list(stacks_string.split("\n"))[:-1]
    stack_strings.reverse()
    stacks = [[] for _ in range(1, len(stack_strings[0]), 4)]
    for layer in stack_strings:
        for stack_num, char_pos in enumerate(range(1, len(layer), 4)):
            if 'A' <= layer[char_pos] <= 'Z':
                stacks[stack_num] += [layer[char_pos]]
    return stacks


def main():
    initial_stacks, instructions = read_input()

    part_1_stacks = deepcopy(initial_stacks)
    follow_instructions_cm9000(part_1_stacks, instructions)
    print(f"Part 1: {''.join(s[-1] for s in part_1_stacks)}")

    part_2_stacks = deepcopy(initial_stacks)
    follow_instructions_cm9001(part_2_stacks, instructions)
    print(f"Part 2: {''.join(s[-1] for s in part_2_stacks)}")


def follow_instructions_cm9000(box_stacks, instructions):
    for qty, move_from, move_to in instructions:
        for _ in range(qty):
            box_stacks[move_to - 1] += box_stacks[move_from - 1][-1:]
            box_stacks[move_from - 1] = box_stacks[move_from - 1][:-1]


def follow_instructions_cm9001(box_stacks, instructions):
    for qty, move_from, move_to in instructions:
        box_stacks[move_to - 1] += box_stacks[move_from - 1][-qty:]
        box_stacks[move_from - 1] = box_stacks[move_from - 1][:-qty]


if __name__ == "__main__":
    main()