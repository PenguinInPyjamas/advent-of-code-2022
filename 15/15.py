import argparse


def read_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    parser.add_argument("--example_input", "-e", default=False, action='store_true')
    args = parser.parse_args()
    sensor_readings = [parse_sensor_reading(s.strip()) for s in open(args.input_file_path)]
    return sensor_readings, args.example_input


def parse_sensor_reading(s):
    _, sensor_x_raw, sensor_y_raw, beacon_x_raw, beacon_y_raw = s.split('=')
    sensor_x = int(sensor_x_raw.split(',')[0])
    sensor_y = int(sensor_y_raw.split(':')[0])
    beacon_x = int(beacon_x_raw.split(',')[0])
    beacon_y = int(beacon_y_raw.split(':')[0])
    return (sensor_x, sensor_y), (beacon_x, beacon_y)


def main():
    sensor_readings, example_input = read_input()
    if example_input:
        initial_row_to_check = 10
        distress_beacon_range = 20
    else:
        initial_row_to_check = 2000000
        distress_beacon_range = 4000000
    beacon_locations = set((x, y) for _, (x, y) in sensor_readings)

    unavailable_ranges_in_row = get_unavailable_ranges(sensor_readings, initial_row_to_check)
    unavailable_positions_in_row = set(x for start, end in unavailable_ranges_in_row for x in range(start, end + 1))
    beacons_in_row = list(filter(lambda l: l[1] == initial_row_to_check, beacon_locations))
    print(f"Part 1: {len(unavailable_positions_in_row) - len(beacons_in_row)}")

    potential_beacon_locations = find_potential_beacons(sensor_readings, distress_beacon_range)
    print(f"Part 2: {','.join(str(x*4000000 + y) for x,y in potential_beacon_locations.difference(beacon_locations))}")


def get_unavailable_ranges(sensor_readings, row_y):
    unavailable_ranges = []
    for (sx, sy), (bx, by) in sensor_readings:
        sensor_to_beacon_distance = abs(sx - bx) + abs(sy - by)
        row_to_sensor_distance = abs(sy - row_y)
        range_start = sx - sensor_to_beacon_distance + row_to_sensor_distance
        range_end = sx + sensor_to_beacon_distance - row_to_sensor_distance
        if range_start <= range_end:
            unavailable_ranges.append((range_start, range_end))

    unavailable_ranges.sort()
    optimised_available_ranges = []
    combined_start, combined_end = unavailable_ranges[0]
    for start, end in unavailable_ranges[1:]:
        if combined_end < start:
            optimised_available_ranges.append((combined_start, combined_end))
            combined_start = start
            combined_end = end
        elif combined_end < end:
            combined_end = end
    optimised_available_ranges.append((combined_start, combined_end))
    return optimised_available_ranges


def find_potential_beacons(sensor_readings, beacon_range):
    potential_beacon_locations = set()
    for y in range(beacon_range + 1):
        next_x_to_check = 0
        for start, end in get_unavailable_ranges(sensor_readings, y):
            potential_beacon_locations.update((x, y) for x in range(next_x_to_check, start))
            next_x_to_check = end + 1
        potential_beacon_locations.update((x, y) for x in range(next_x_to_check, beacon_range + 1))
    return potential_beacon_locations


if __name__ == "__main__":
    main()
