import argparse
from collections import namedtuple

Monkey = namedtuple("Monkey", ["items", "operation", "test", "throw_to_if_true", "throw_to_if_false"])
Operation = namedtuple("Operation", ["operator", "lhs_is_int", "lhs", "rhs_is_int", "rhs"])


def read_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    args = parser.parse_args()
    monkeys = [parse_monkey_string(m.strip()) for m in ''.join(open(args.input_file_path)).split('\n\n')]
    return monkeys


def parse_monkey_string(s):
    lines = [x.strip() for x in s.split('\n')]
    items = [int(x) for x in lines[1][16:].split(", ")]
    operation = parse_operation(lines[2][17:])
    test = int(lines[3][19:])
    throw_to_if_true = int(lines[4][25:])
    throw_to_if_false = int(lines[5][26:])
    return Monkey(items, operation, test, throw_to_if_true, throw_to_if_false)


def parse_operation(s):
    lhs_string, operator, rhs_string = s.split(' ')
    if lhs_string == "old":
        lhs_is_int = False
        lhs = None
    else:
        lhs_is_int = True
        lhs = int(lhs_string)
    if rhs_string == "old":
        rhs_is_int = False
        rhs = None
    else:
        rhs_is_int = True
        rhs = int(rhs_string)
    return Operation(operator, lhs_is_int, lhs, rhs_is_int, rhs)


def main():
    monkeys = read_input()
    worried_inspection_counts = get_inspection_counts(monkeys, 20)
    print(f"Part 1: {worried_inspection_counts[-1] * worried_inspection_counts[-2]}")
    fearless_inspection_counts = get_inspection_counts(monkeys, 10000, False)
    print(f"Part 2: {fearless_inspection_counts[-1] * fearless_inspection_counts[-2]}")


def get_inspection_counts(monkeys, num_turns, worried=True):
    keep_away_results = play_keep_away(list(monkeys), worried)
    monkey_inspection_counts = [0 for _ in monkeys]
    for _ in range(num_turns):
        new_inspection_counts = next(keep_away_results)
        for i in range(len(new_inspection_counts)):
            monkey_inspection_counts[i] += new_inspection_counts[i]
    return sorted(monkey_inspection_counts)


def play_keep_away(initial_state, worried=True):
    monkeys = [copy_monkey(m) for m in initial_state]
    maximum_worry = 1
    for m in monkeys:
        maximum_worry *= m.test
    while True:
        monkey_inspection_counts = [0 for _ in monkeys]
        for i, m in enumerate(monkeys):
            for worry in m.items:
                monkey_inspection_counts[i] += 1
                worry = monkey_inspect(m.operation, worry)
                if worried:
                    worry = int(worry / 3)
                else:
                    worry = worry % maximum_worry
                if worry % m.test == 0:
                    monkeys[m.throw_to_if_true].items.append(worry)
                else:
                    monkeys[m.throw_to_if_false].items.append(worry)
            m.items.clear()
        yield list(monkey_inspection_counts)


def monkey_inspect(operation, old):
    lhs = operation.lhs if operation.lhs_is_int else old
    rhs = operation.rhs if operation.rhs_is_int else old
    if operation.operator == '+':
        return lhs + rhs
    elif operation.operator == '*':
        return lhs * rhs
    else:
        raise Exception(f"Unknown operator '{operation.operator}'")


def copy_monkey(monkey):
    return Monkey(list(monkey.items), monkey.operation, monkey.test, monkey.throw_to_if_true, monkey.throw_to_if_false)


if __name__ == "__main__":
    main()
