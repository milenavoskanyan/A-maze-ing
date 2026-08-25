#!/usr/bin/env python3

import sys
from my_exceptions import ConfigError
from parse_validate import read_maze_file, parse_to_dict
from mazegen import MazeGenerator, shortest_path, path_to_directions

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]

    try:
        file_content = read_maze_file(config_file)
        config_dict = parse_to_dict(file_content)
        maze_generator = MazeGenerator(config_dict)
        maze = maze_generator.generate()
    except ConfigError as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

    path = shortest_path(
        maze,
        config_dict["WIDTH"],
        config_dict["HEIGHT"],
        config_dict["ENTRY"],
        config_dict["EXIT"]
    )

    with open(config_dict["OUTPUT_FILE"], "w") as f:
        f.write(path_to_directions(path))
    print("Path written to file.")
