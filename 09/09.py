import argparse
from collections import Counter
from collections import namedtuple

Position = namedtuple("Position", ["x", "y"])


def read_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    args = parser.parse_args()
    instructions = [(line[0], int(line[2:])) for line in open(args.input_file_path)]
    return instructions


def main():
    instructions = read_input()

    bridge_tail_locations = Counter()
    for positions in follow_instructions(instructions, 2):
        bridge_tail_locations.update({positions[-1]})
    print(f"Part 1: {len(bridge_tail_locations.values())}")

    broken_bridge_tail_locations = Counter()
    for positions in follow_instructions(instructions, 10):
        broken_bridge_tail_locations.update({positions[-1]})
    print(f"Part 2: {len(broken_bridge_tail_locations.values())}")


def follow_instructions(instructions, num_knots):
    head = Position(0, 0)
    tails = [Position(0, 0) for _ in range(num_knots - 1)]
    for direction, distance in instructions:
        for _ in range(distance):
            if direction == "R":
                head = Position(head.x + 1, head.y)
            if direction == "U":
                head = Position(head.x, head.y - 1)
            if direction == "L":
                head = Position(head.x - 1, head.y)
            if direction == "D":
                head = Position(head.x, head.y + 1)
            for i in range(len(tails)):
                follower = tails[i]
                if i == 0:
                    leader = head
                else:
                    leader = tails[i - 1]
                new_position = follower
                if leader.x == follower.x + 2 and leader.y == follower.y:
                    new_position = Position(follower.x + 1, follower.y)
                elif leader.x == follower.x - 2 and leader.y == follower.y:
                    new_position = Position(follower.x - 1, follower.y)
                elif leader.y == follower.y + 2 and leader.x == follower.x:
                    new_position = Position(follower.x, follower.y + 1)
                elif leader.y == follower.y - 2 and leader.x == follower.x:
                    new_position = Position(follower.x, follower.y - 1)
                elif follower.x not in range(leader.x - 1, leader.x + 2) or follower.y not in range(leader.y - 1, leader.y + 2):
                    if leader.x > follower.x and leader.y > follower.y:
                        new_position = Position(follower.x + 1, follower.y + 1)
                    elif leader.x < follower.x and leader.y > follower.y:
                        new_position = Position(follower.x - 1, follower.y + 1)
                    elif leader.x > follower.x and leader.y < follower.y:
                        new_position = Position(follower.x + 1, follower.y - 1)
                    elif leader.x < follower.x and leader.y < follower.y:
                        new_position = Position(follower.x - 1, follower.y - 1)
                tails[i] = new_position
            yield [head] + tails


if __name__ == "__main__":
    main()
