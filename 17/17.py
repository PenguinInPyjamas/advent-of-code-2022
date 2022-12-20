import argparse
from itertools import cycle
from collections import defaultdict

MINUS_SHAPE = ((0, 0), (1, 0), (2, 0), (3, 0))
CROSS_SHAPE = ((0, 1), (1, 0), (1, 1), (1, 2), (2, 1))
L_SHAPE = ((0, 0), (1, 0), (2, 0), (2, 1), (2, 2))
I_SHAPE = ((0, 0), (0, 1), (0, 2), (0, 3))
SQUARE_SHAPE = ((0, 0), (0, 1), (1, 0), (1, 1))


def read_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    args = parser.parse_args()
    jet_directions = [c for c in next(open(args.input_file_path)).strip()]
    return jet_directions


def main():
    jet_directions = read_input()
    print(f"Part 1: {simulate_rocks(jet_directions, 2022)}")
    print(f"Part 2: {simulate_rocks(jet_directions, 1000000000000)}")


def simulate_rocks(jet_directions, num_shapes_to_simulate):
    num_shapes_simulated = 0
    num_jets_simulated = 0
    rock_locations = set()
    column_heights = [0 for _ in range(7)]
    height_offset = 0
    known_formations = defaultdict(lambda: [])
    shapes_cycle = cycle((MINUS_SHAPE, CROSS_SHAPE, L_SHAPE, I_SHAPE, SQUARE_SHAPE))
    directions_cycle = cycle(jet_directions)
    for shape in shapes_cycle:
        num_shapes_simulated += 1
        new_rocks = [(x + 2, y + 3 + max(column_heights)) for x, y in shape]
        for direction in directions_cycle:
            # The new shape of rocks moves and falls until it can't fall any more
            num_jets_simulated += 1
            if direction is '>' and all(can_move_right(x, y, rock_locations) for x, y in new_rocks):
                for i in range(len(new_rocks)):
                    new_rocks[i] = (new_rocks[i][0] + 1, new_rocks[i][1])
            elif direction is '<' and all(can_move_left(x, y, rock_locations) for x, y in new_rocks):
                for i in range(len(new_rocks)):
                    new_rocks[i] = (new_rocks[i][0] - 1, new_rocks[i][1])

            if all(can_move_down(x, y, rock_locations) for x, y in new_rocks):
                for i in range(len(new_rocks)):
                    new_rocks[i] = (new_rocks[i][0], new_rocks[i][1] - 1)
            else:
                rock_locations.update(new_rocks)
                for x in range(7):
                    column_heights[x] = max(map(lambda p: p[1], filter(lambda p: p[0] == x, rock_locations)),
                                            default=-1) + 1
                if num_shapes_simulated >= num_shapes_to_simulate:
                    return height_offset + max(column_heights)
                break
        if num_shapes_simulated % 5 == 0:
            # Optimise the set of occupied spaces by removing those that are inaccessible
            chamber_shape = set()
            x = 0
            y = column_heights[0]
            maze_directions = cycle(((1, 0), (0, -1), (-1, 0), (0, 1)))
            current_direction = next(maze_directions)
            next_direction = next(maze_directions)
            while x < 7:
                fx, fy = x + current_direction[0], y + current_direction[1]
                rx, ry = x + next_direction[0], y + next_direction[1]
                if (rx, ry) not in rock_locations and 0 <= rx <= 6 and 0 <= ry:
                    x = rx
                    y = ry
                    current_direction = next_direction
                    next_direction = next(maze_directions)
                elif (fx, fy) not in rock_locations and 0 <= fx and 0 <= fy:
                    chamber_shape.add((rx, ry))
                    x = fx
                    y = fy
                else:
                    chamber_shape.add((rx, ry))
                    chamber_shape.add((fx, fy))
                    next(maze_directions)
                    current_direction = next(maze_directions)
                    next_direction = next(maze_directions)
            # Normalise the floor level to make comparing formations easier
            floor_level = min(map(lambda p: p[1], chamber_shape))
            rock_locations.clear()
            for x, y in chamber_shape:
                rock_locations.add((x, y - floor_level))
            height_offset += floor_level
            for i, x in enumerate(column_heights):
                column_heights[i] = column_heights[i] - floor_level

            # If the formation loops, it will happen when the shape and jet inputs reach the same position twice
            jet_index = num_jets_simulated % len(jet_directions)
            found_existing_formation = False
            for rocks, old_shape_index, old_height_offset in known_formations[jet_index]:
                if len(rock_locations) == len(rocks) and len(rock_locations.difference(rocks)) == 0:
                    found_existing_formation = True
                    shape_num_step = num_shapes_simulated - old_shape_index
                    height_step = height_offset - old_height_offset
                    num_skips = int((num_shapes_to_simulate - num_shapes_simulated) / shape_num_step)
                    num_shapes_simulated += num_skips * shape_num_step
                    height_offset += num_skips * height_step
                    break
            if not found_existing_formation:
                known_formations[jet_index].append((rock_locations.copy(), num_shapes_simulated, height_offset))


def can_move_right(x, y, rocks):
    return (x + 1, y) not in rocks and x < 6


def can_move_left(x, y, rocks):
    return (x - 1, y) not in rocks and x > 0


def can_move_down(x, y, rocks):
    return (x, y - 1) not in rocks and y > 0


if __name__ == "__main__":
    main()
