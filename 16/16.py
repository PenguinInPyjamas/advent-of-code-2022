import argparse
from collections import defaultdict
import time


def read_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    args = parser.parse_args()
    valves = dict(parse_valve_info(s.strip()) for s in open(args.input_file_path))
    return valves


def parse_valve_info(s):
    label = s.split(' ')[1]
    flow_rate = int(s[23:].split(';')[0])
    nearby_tunnels = " ".join(s.split(' ')[9:]).split(', ')
    return label, (flow_rate, nearby_tunnels)


def main():
    valves = read_input()
    valve_distances = get_valve_distances(valves)

    print(f"Part 1: {maximise_pressure_solo(valves, valve_distances, 'AA')}")

    print("Note: part 2 may take a long time to complete")
    start_time = time.time()
    print(f"Part 2: {maximise_pressure_multiple_agents(valves, valve_distances)}")
    elapsed_time = int(time.time() - start_time)
    if elapsed_time > 20:
        print(f"Wow! That took {elapsed_time} seconds!")


def maximise_pressure_solo(valves, valve_distances, current_valve, time_remaining=30, released_valves=None):
    if released_valves is None:
        released_valves = set(filter(lambda x: valves[x][0] == 0, valves.keys()))

    max_potential_pressure = 0
    for v in valve_distances[current_valve]:
        if v in released_valves:
            continue
        new_time = time_remaining - valve_distances[current_valve][v] - 1
        if new_time > 0:
            potential_pressure = (valves[v][0] * new_time) + \
                                 maximise_pressure_solo(valves, valve_distances, v,
                                                        new_time, released_valves.union({v}))
            if potential_pressure > max_potential_pressure:
                max_potential_pressure = potential_pressure
    return max_potential_pressure


def maximise_pressure_multiple_agents(valves, valve_distances, agents=None, released_valves=None):
    if agents is None:
        agents = (("AA", 26), ("AA", 26))
    if released_valves is None:
        released_valves = set(filter(lambda x: valves[x][0] == 0, valves))

    active_agent_index = None
    time_of_next_action = 0
    for index, (valve, time) in enumerate(agents):
        if time > time_of_next_action:
            active_agent_index = index
            time_of_next_action = time
    if time_of_next_action < 1:
        return 0

    max_potential_pressure = 0
    for v in valve_distances[agents[active_agent_index][0]]:
        if v in released_valves:
            continue
        time_after_valve_opening = time_of_next_action - valve_distances[agents[active_agent_index][0]][v] - 1
        if time_after_valve_opening > 0:
            new_agents = tuple(x if i is not active_agent_index else (v, time_after_valve_opening)
                               for i, x in enumerate(agents))
            potential_pressure = (valves[v][0] * time_after_valve_opening) + \
                                 maximise_pressure_multiple_agents(valves, valve_distances,
                                                                   new_agents, released_valves.union({v}))
            if potential_pressure > max_potential_pressure:
                max_potential_pressure = potential_pressure
    new_agents = tuple(x if i is not active_agent_index else ("", 0) for i, x in enumerate(agents))
    pressure_if_lazy = maximise_pressure_multiple_agents(valves, valve_distances, new_agents, released_valves)
    return max(max_potential_pressure, pressure_if_lazy)


def get_valve_distances(valves):
    valve_distances = defaultdict(lambda: dict())
    for a in valves:
        for b in valves:
            valve_distances[a][b] = find_distance_to_valve(valves, a, b, valve_distances)
    return valve_distances


def find_distance_to_valve(valves, starting_point, goal, valve_distances=None, valves_to_ignore=None):
    if valve_distances is not None and goal in valve_distances[starting_point]:
        return valve_distances[starting_point][goal]
    if starting_point == goal:
        return 0
    if valves_to_ignore is None:
        valves_to_ignore = {starting_point}
    shortest_distance_to_goal = len(valves)
    for v in filter(lambda x: x not in valves_to_ignore, valves[starting_point][1]):
        distance = find_distance_to_valve(valves, v, goal, valve_distances, valves_to_ignore.union({starting_point}))
        if distance < shortest_distance_to_goal:
            shortest_distance_to_goal = distance
    return 1 + shortest_distance_to_goal


if __name__ == "__main__":
    main()
