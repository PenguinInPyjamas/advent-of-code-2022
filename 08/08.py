import argparse


def read_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    args = parser.parse_args()
    tree_heights = [[int(c) for c in line.strip()] for line in open(args.input_file_path)]
    return tree_heights


def main():
    tree_heights = read_input()

    visible_trees_map = make_visible_trees_map(tree_heights)
    print(f"Part 1: {sum(1 if v else 0 for row in visible_trees_map for v in row)}")

    scenic_score_map = make_scenic_score_map(tree_heights)
    print(f"Part 2: {max(s for row in scenic_score_map for s in row)}")


# The implementation of this function is an abomination wrought by hubris
def make_visible_trees_map(tree_heights):
    map_width = len(tree_heights[0])
    map_height = len(tree_heights)

    visible_trees_from_west = [list(get_visible_trees_from_list(row)) for row in tree_heights]
    visible_trees_from_east = [list(get_visible_trees_from_list(reversed(row))) for row in tree_heights]
    visible_trees_from_north = [list(get_visible_trees_from_list(
        tree_heights[y][x] for y in range(map_height))) for x in range(map_width)]
    visible_trees_from_south = [list(get_visible_trees_from_list(
        tree_heights[y][x] for y in reversed(range(map_height)))) for x in range(map_width)]

    visible_trees = [[False for _ in range(map_width)] for _ in range(map_height)]
    for x in range(map_width):
        for y in range(map_height):
            visible_from_west = visible_trees_from_west[y][x]
            visible_from_east = visible_trees_from_east[y][-x-1]
            visible_from_north = visible_trees_from_north[x][y]
            visible_from_south = visible_trees_from_south[x][-y-1]
            visible_trees[y][x] = visible_from_west or visible_from_east or visible_from_north or visible_from_south
    return visible_trees


def get_visible_trees_from_list(heights):
    highest_recorded_tree = -1
    for h in heights:
        if h > highest_recorded_tree:
            highest_recorded_tree = h
            yield True
        else:
            yield False


def make_scenic_score_map(tree_heights):
    score_map = [[0 for _ in row] for row in tree_heights]
    map_width = len(tree_heights[0])
    map_height = len(tree_heights)
    for target_y in range(map_height):
        for target_x in range(map_width):
            score = 1
            sight_lines = (((target_x, y) for y in range(target_y+1, map_height)),
                           ((target_x, y) for y in range(target_y-1, -1, -1)),
                           ((x, target_y) for x in range(target_x+1, map_width)),
                           ((x, target_y) for x in range(target_x-1, -1, -1)))
            for line in sight_lines:
                tree_count = 0
                for x, y in line:
                    tree_count += 1
                    if tree_heights[y][x] >= tree_heights[target_y][target_x]:
                        break
                score *= tree_count
                score_map[target_y][target_x] = score
    return score_map


if __name__ == "__main__":
    main()
