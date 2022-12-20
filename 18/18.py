import argparse

ADJACENT_VOXEL_DIFFS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))


def read_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    args = parser.parse_args()
    droplet_voxels = [tuple(int(x) for x in line.strip().split(',')) for line in open(args.input_file_path)]
    return droplet_voxels


def main():
    droplet_voxels = set(read_input())
    print(f"Part 1: {get_surface_area(droplet_voxels)}")
    print(f"Part 2: {get_surface_area(droplet_voxels, False)}")


def get_surface_area(lava_voxels, count_internal_surfaces=True):
    surface_area = 0
    if count_internal_surfaces:
        for x, y, z in lava_voxels:
            for dx, dy, dz in ADJACENT_VOXEL_DIFFS:
                surface_area += 1 if (x + dx, y + dy, z + dz) not in lava_voxels else 0
    else:
        xs, ys, zs = (list(map(lambda v: v[i], lava_voxels)) for i in range(3))
        min_x, max_x, min_y, max_y, min_z, max_z = min(xs), max(xs), min(ys), max(ys), min(zs), max(zs)
        inside_layer = {(x, y, z) for x in range(min_x - 1, max_x + 2)
                      for y in range(min_y - 1, max_y + 2)
                      for z in range(min_z - 1, max_z + 2)
                      if x in (min_x - 1, max_x + 1) or y in (min_y - 1, max_y + 1) or z in (min_z - 1, max_z + 1)}
        outside_voxels = inside_layer.copy()
        while True:
            new_inside_layer = set()
            for (x, y, z) in inside_layer:
                for dx, dy, dz in ADJACENT_VOXEL_DIFFS:
                    p = (x + dx, y + dy, z + dz)
                    if p not in inside_layer and p not in outside_voxels and p not in lava_voxels\
                            and min_x <= p[0] <= max_x and min_y <= p[1] <= max_y and min_z <= p[2] <= max_z:
                        new_inside_layer.add(p)
            if len(new_inside_layer) > 0:
                print(len(new_inside_layer))
                outside_voxels.update(new_inside_layer)
                inside_layer = new_inside_layer
            else:
                break
        for x, y, z in lava_voxels:
            for dx, dy, dz in ADJACENT_VOXEL_DIFFS:
                surface_area += 1 if (x + dx, y + dy, z + dz) in outside_voxels else 0
    return surface_area


if __name__ == "__main__":
    main()
