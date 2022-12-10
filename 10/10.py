import argparse


def read_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    args = parser.parse_args()
    instructions = [line.strip() for line in open(args.input_file_path)]
    return instructions


def main():
    instructions = read_input()
    x_register_values = list(perform_instructions(instructions))

    signal_strengths = [(i + 1) * v for i, v in enumerate(x_register_values)]
    final_strength_value = signal_strengths[19] + signal_strengths[59] + signal_strengths[99] + \
        signal_strengths[139] + signal_strengths[179] + signal_strengths[219]
    print(f"Part 1: {final_strength_value}")

    print(f"Part 2:")
    for pos, reg_val in enumerate(x_register_values):
        print('█' if reg_val - 1 <= (pos % 40) <= reg_val + 1 else ' ', end='\n' if (pos + 1) % 40 == 0 else '')


def perform_instructions(instructions):
    x_register = 1
    for command in instructions:
        if command == "noop":
            yield x_register
        elif command[:4] == "addx":
            yield x_register
            yield x_register
            x_register += int(command[5:])
        else:
            raise Exception(f"Unknown command: '{command}'")
    yield x_register


if __name__ == "__main__":
    main()
