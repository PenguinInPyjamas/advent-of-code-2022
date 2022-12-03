import argparse


def read_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    args = parser.parse_args()
    rucksacks = [s.strip() for s in open(args.input_file_path)]
    return rucksacks


def main():
    rucksacks = read_input()

    duplicated_items = [get_duplicated_item(r) for r in rucksacks]
    duplicated_item_priorities_sum = sum(get_priority(item) for item in duplicated_items)
    print(f"Part 1: {duplicated_item_priorities_sum}")

    elf_groups = [rucksacks[x:x+3] for x in range(0, len(rucksacks), 3)]
    badge_priorities_sum = sum(get_priority(get_badge(group)) for group in elf_groups)
    print(f"Part 2: {badge_priorities_sum}")


def get_duplicated_item(rucksack):
    if len(rucksack) % 2 != 0:
        raise Exception(f"There must be an even number of items in the rucksack, found {len(rucksack)}")
    compartment_size = int(len(rucksack) / 2)
    lhs = rucksack[:compartment_size]
    rhs = rucksack[compartment_size:]
    duplicated_items = set(lhs).intersection(set(rhs))
    if len(duplicated_items) != 1:
        raise Exception(f"Invalid number of duplicate items found: {list(duplicated_items)}")
    return list(duplicated_items)[0]


def get_badge(rucksacks):
    if len(rucksacks) != 3:
        raise Exception(f"Expected exactly 3 rucksacks, got {len(rucksacks)}")
    rucksack_a, rucksack_b, rucksack_c = rucksacks
    common_items = set(rucksack_a).intersection(set(rucksack_b)).intersection(set(rucksack_c))
    if len(common_items) != 1:
        raise Exception(f"Invalid number of common items found: {list(common_items)}")
    return list(common_items)[0]


def get_priority(c):
    if 'a' <= c <= 'z':
        return ord(c) - ord('a') + 1
    if 'A' <= c <= 'Z':
        return ord(c) - ord('A') + 27
    raise Exception(f"Invalid character to fetch priority: '{c}'")


if __name__ == "__main__":
    main()
