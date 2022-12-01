import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    args = parser.parse_args()
    input_string = "".join(open(args.input_file_path))
    calorie_groups = [[int(x.strip()) for x in calorie_counts_list.split("\n") if len(x) > 0]
                      for calorie_counts_list in input_string.split("\n\n") if len(calorie_counts_list)]
    return calorie_groups


def main():
    calorie_groups = parse_args()

    calorie_totals = list(reversed(sorted([sum(x) for x in calorie_groups])))
    highest_calorie_total = calorie_totals[0]
    highest_3_calorie_totals = sum(calorie_totals[:3])
    print(f"Part 1:\n{highest_calorie_total}\n\nPart 2:\n{highest_3_calorie_totals}\n")


if __name__ == "__main__":
    main()