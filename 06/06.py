import argparse


def read_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    args = parser.parse_args()
    signals = [s.strip() for s in open(args.input_file_path)]
    return signals


def main():
    signals = read_input()
    print(f"Part 1: {', '.join(str(get_marker_position(s, 4)) for s in signals)}")
    print(f"Part 1: {', '.join(str(get_marker_position(s, 14)) for s in signals)}")


def get_marker_position(signal, marker_length):
    position = marker_length
    while position <= len(signal):
        recent_characters = set(signal[position - marker_length:position])
        if len(recent_characters) == marker_length:
            return position
        position += 1
    raise Exception(f"No marker of length {marker_length} was found in signal '{signal}'")


if __name__ == "__main__":
    main()
