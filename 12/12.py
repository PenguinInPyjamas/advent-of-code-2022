import argparse


def read_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    args = parser.parse_args()
    height_map = [[c for c in s.strip()] for s in open(args.input_file_path)]
    return height_map


def main():
    height_map = read_input()

    shortest_steps_map = make_shortest_steps_map(height_map, find_start(height_map))
    print(f"Part 1: {max(shortest_steps_map.values())}")

    shortest_steps_maps = (make_shortest_steps_map(height_map, p).values()
                           for p in find_all_possible_starts(height_map))
    print(f"Part 2: {min(max(m) if len(m) > 0 else 999999 for m in shortest_steps_maps)}")


def make_shortest_steps_map(height_map, start_point):
    shortest_steps_map = {}
    points_to_check = {(start_point, 0)}
    current_step_count = 0
    while len(points_to_check) > 0:
        new_points_to_check = set()
        for (x, y), max_height in points_to_check:
            height = get_height(height_map[y][x])
            if (x, y) not in shortest_steps_map.keys() and height <= max_height:
                shortest_steps_map.update({(x, y): current_step_count})
                if height_map[y][x] == 'E':
                    return shortest_steps_map
                adjacent_points = ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
                for ax, ay in adjacent_points:
                    if ay in range(len(height_map)) and ax in range(len(height_map[ay])):
                        new_points_to_check.add(((ax, ay), height + 1))
        current_step_count += 1
        points_to_check = new_points_to_check
    return {}


def find_start(height_map):
    for y in range(len(height_map)):
        for x in range(len(height_map[y])):
            if height_map[y][x] == 'S':
                return x, y
    raise Exception("Couldn't find start")


def find_all_possible_starts(height_map):
    for y in range(len(height_map)):
        for x in range(len(height_map[y])):
            if get_height(height_map[y][x]) == 0:
                yield x, y


def get_height(c):
    if c == 'S':
        return 0
    if c == 'E':
        return ord('z') - ord('a')
    if 'a' <= c <= 'z':
        return ord(c) - ord('a')
    raise Exception(f"Height character cannot be '{c}'")


if __name__ == "__main__":
    main()
