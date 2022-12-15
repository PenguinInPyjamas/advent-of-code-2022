import argparse


def read_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    args = parser.parse_args()
    message_string = "".join(open(args.input_file_path)).strip()
    return message_string


def main():
    message_string = read_input()

    comparisons = [compare_packets(a, b) for a, b in parse_message_pairs(message_string)]
    print(f"Part 1: {sum(i + 1 if x > 0 else 0 for i, x in enumerate(comparisons))}")

    sorted_message = list(sort_packets(parse_message_with_dividers(message_string)))
    print(f"Part 2: {(sorted_message.index([[6]]) + 1) * (sorted_message.index([[2]]) + 1)}")


def parse_message_pairs(message_string):
    for pair in message_string.split("\n\n"):
        left, right = (parse_packet(s.strip()) for s in pair.split("\n"))
        yield left, right


def parse_message_with_dividers(message_string):
    return [[[2]], [[6]]] + [parse_packet(s.strip()) for s in message_string.split('\n') if len(s) > 0]


def parse_packet(s):
    if s == "[]":
        return []
    if s[0] == '[' and s[-1] == ']':
        items = []
        start_of_item = 1
        items_deep = 0
        for i in range(1, len(s) - 1):
            if s[i] == '[':
                items_deep += 1
            elif s[i] == ']':
                items_deep -= 1
            elif s[i] == ',' and items_deep == 0:
                items.append(parse_packet(s[start_of_item:i]))
                start_of_item = i + 1
        items.append(parse_packet(s[start_of_item:-1]))
        return items
    return int(s)


def compare_packets(lhs, rhs):
    if isinstance(lhs, int) and isinstance(rhs, int):
        # print(f"int comparison: {rhs} - {lhs}")
        return rhs - lhs
    if isinstance(lhs, int):
        lhs = [lhs]
    if isinstance(rhs, int):
        rhs = [rhs]
    if isinstance(lhs, list) and isinstance(rhs, list):
        for i in range(max(len(lhs), len(rhs))):
            if len(lhs) <= i:
                return 1
            if len(rhs) <= i:
                return -1
            comparison = compare_packets(lhs[i], rhs[i])
            if comparison != 0:
                return comparison
    return 0


def sort_packets(packets):
    while len(packets) > 0:
        shortest_packet_index = 0
        for i in range(1, len(packets)):
            if compare_packets(packets[shortest_packet_index], packets[i]) < 0:
                shortest_packet_index = i
        yield packets[shortest_packet_index]
        packets = packets[:shortest_packet_index] + packets[shortest_packet_index + 1:]


if __name__ == "__main__":
    main()
