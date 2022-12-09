import argparse
from collections import namedtuple

FS_NODE = namedtuple("FS_NODE", ["type", "filename", "content"])
DIRECTORY = "dir"
FILE = "file"


def read_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    args = parser.parse_args()
    raw_terminal_string = "".join(s for s in open(args.input_file_path))
    return raw_terminal_string


def main():
    raw_terminal_string = read_input()

    fs_tree = build_fs_tree(raw_terminal_string)
    dir_sizes = report_dir_sizes(fs_tree)
    print(f"Part 1: {sum(x for x in dir_sizes if x <= 100000)}")

    required_space = 30000000 - (70000000 - sorted(dir_sizes)[-1])
    print(f"Part 2: {sorted(x for x in dir_sizes if x >= required_space)[0]}")


def build_fs_tree(terminal_string):
    root = FS_NODE(DIRECTORY, "~", [])
    node_path = [root]
    for command_and_result in terminal_string.split("$ "):
        lines = command_and_result.strip().split("\n")
        command = list(lines[0].split(" "))
        if command[0] == "ls":
            node_path[-1].content.clear()
            for ls_line in lines[1:]:
                size, filename = ls_line.split(" ")
                if size == "dir":
                    node_path[-1].content.append(FS_NODE(DIRECTORY, filename, []))
                else:
                    node_path[-1].content.append(FS_NODE(FILE, filename, int(size)))
        if command[0] == "cd":
            if command[1] == "/":
                node_path = [root]
            elif command[1] == "..":
                node_path = node_path[:-1]
            else:
                for node in node_path[-1].content:
                    if node.type == DIRECTORY and node.filename == command[1]:
                        node_path.append(node)
                        break
                else:
                    raise Exception(f"Could not find dir called '{command[1]}'")
    return root


def report_dir_sizes(root_node):
    directory_sizes = []
    root_node_size = 0
    for node in root_node.content:
        if node.type == DIRECTORY:
            directory_sizes += report_dir_sizes(node)
            root_node_size += directory_sizes[-1]
        elif node.type == FILE:
            root_node_size += node.content
        else:
            raise Exception(f"Unexpected file system type: '{node.type}'")
    directory_sizes.append(root_node_size)
    return directory_sizes


if __name__ == "__main__":
    main()
