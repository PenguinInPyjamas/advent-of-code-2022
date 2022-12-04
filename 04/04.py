import argparse


def read_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    args = parser.parse_args()
    assignments = [tuple(tuple(int(s.strip())
                               for s in sections.strip().split("-"))
                         for sections in line.strip().split(","))
                   for line in open(args.input_file_path)]
    return assignments


def main():
    assignments = read_input()
    print(f"Part 1: {count_complete_overlaps(assignments)}")
    print(f"Part 2: {count_partial_overlaps(assignments)}")


def count_complete_overlaps(assignments):
    num_overlaps = 0
    for (a_start, a_end), (b_start, b_end) in assignments:
        a = set(range(a_start, a_end + 1))
        b = set(range(b_start, b_end + 1))
        if len(a.intersection(b)) in (len(a), len(b)):
            num_overlaps += 1
    return num_overlaps


def count_partial_overlaps(assignments):
    num_overlaps = 0
    for (a_start, a_end), (b_start, b_end) in assignments:
        a = set(range(a_start, a_end + 1))
        b = set(range(b_start, b_end + 1))
        if len(a.intersection(b)) > 0:
            num_overlaps += 1
    return num_overlaps


if __name__ == "__main__":
    main()
