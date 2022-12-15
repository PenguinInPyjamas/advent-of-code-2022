import argparse


def read_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    args = parser.parse_args()
    paths = [[tuple(int(x) for x in p.split(',')) for p in s.split(" -> ")] for s in open(args.input_file_path)]
    return paths


def main():
    paths = read_input()
    cavern_map = create_cavern_map(paths)
    print(f"Part 1: {sum(1 if x == '+' else 0 for x in run_sand_simulation(cavern_map).values())}")
    print(f"Part 2: {sum(1 if x == '+' else 0 for x in run_sand_simulation(cavern_map, True).values())}")


def create_cavern_map(paths):
    cavern_map = dict()
    for p in paths:
        for i in range(len(p) - 1):
            start_x, start_y = p[i]
            end_x, end_y = p[i + 1]
            if start_x == end_x:
                ys = range(start_y, end_y + 1) if start_y < end_y else range(start_y, end_y - 1, -1)
                for y in ys:
                    cavern_map.update({(start_x, y): '#'})
            elif start_y == end_y:
                xs = range(start_x, end_x + 1) if start_x < end_x else range(start_x, end_x - 1, -1)
                for x in xs:
                    cavern_map.update({(x, start_y): '#'})
            else:
                raise NotImplementedError(f"Bendy path ({start_y},{start_y})=>({end_x},{end_y})")
    return cavern_map


def run_sand_simulation(initial_cavern_map, add_floor=False):
    cavern_map = initial_cavern_map.copy()
    lowest_rock_y = max(y for x, y in cavern_map.keys() if cavern_map[(x, y)] == '#')
    if add_floor:
        rock_xs = set(x for x, _ in cavern_map.keys())
        cavern_map.update({((x, lowest_rock_y + 2), '#') for x in range(min(rock_xs) - 500, max(rock_xs) + 501)})
        lowest_rock_y += 2
    while (500, 0) not in cavern_map:
        sand_x = 500
        sand_y = 0
        while True:
            if sand_y >= lowest_rock_y:
                return cavern_map
            if (sand_x, sand_y + 1) not in cavern_map:
                sand_y += 1
            elif (sand_x - 1, sand_y + 1) not in cavern_map:
                sand_x -= 1
                sand_y += 1
            elif (sand_x + 1, sand_y + 1) not in cavern_map:
                sand_x += 1
                sand_y += 1
            else:
                cavern_map.update({(sand_x, sand_y): '+'})
                break
    return cavern_map


if __name__ == "__main__":
    main()
