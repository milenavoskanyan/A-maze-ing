#!/usr/bin/env python3

import sys
from my_exceptions import ConfigError
from parse_validate import read_maze_file, parse_to_dict
from mazegen import MazeGenerator, shortest_path, path_to_directions

import os
from typing import List, Tuple, Optional
from utils import is_42_cell

# ANSI Color Definitions
COLORS = {
    "BLUE": "\033[94m",
    "CYAN": "\033[96m",
    "MAGENTA": "\033[95m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[33m",
    "RED": "\033[91m",
    "RESET": "\033[0m",
}

def print_maze(
    grid: list[list[int]],
    width: int,
    height: int,
    path: Optional[list[tuple[int, int]]] = None,
    entry: Optional[tuple[int, int]] = None,
    exit_: Optional[tuple[int, int]] = None,
    show_path: bool = True,
    wall_color_name: str = "BLUE",
    pattern_color_name: str = "YELLOW",
) -> None:
    wall_c = COLORS.get(wall_color_name, COLORS["BLUE"])
    pattern_c = COLORS.get(pattern_color_name, COLORS["YELLOW"])
    green_c = COLORS["GREEN"]
    red_c = COLORS["RED"]
    magenta_c = COLORS["MAGENTA"]
    reset = COLORS["RESET"]

    path_set = set(path) if (path and show_path) else set()
    lines: list[str] = []

    for r in range(height):
        # Top wall of this row (North bit = 1)
        top = ""
        for c in range(width):
            top += f"{wall_c}+{reset}"
            top += f"{wall_c}---{reset}" if (grid[r][c] & 1) else "   "
        top += f"{wall_c}+{reset}"
        lines.append(top)

        # Cell row: left wall (West bit = 8) + content + right wall (East bit = 2, last col only)
        mid = ""
        for c in range(width):
            mid += f"{wall_c}|{reset}" if (grid[r][c] & 8) else " "
            cell = (r, c)
            
            is_pattern = is_42_cell(width, height, r, c)

            if cell == entry:
                mid += f"{red_c} S {reset}"
            elif cell == exit_:
                mid += f"{red_c} E {reset}"
            elif cell in path_set:
                mid += f"{magenta_c} · {reset}"
            elif is_pattern:
                mid += f"{pattern_c} 42 {reset}"  # Highlights the 42 pattern cells
            else:
                mid += "   "
                
        mid += f"{wall_c}|{reset}" if (grid[r][width - 1] & 2) else " "
        lines.append(mid)

    # Bottom border (South bit = 4 of last row)
    bottom = ""
    for c in range(width):
        bottom += f"{wall_c}+{reset}"
        bottom += f"{wall_c}---{reset}" if (grid[height - 1][c] & 4) else "   "
    bottom += f"{wall_c}+{reset}"
    lines.append(bottom)

    print("\n".join(lines))

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
    print_maze(
        maze,
        config_dict["WIDTH"],
        config_dict["HEIGHT"],
        path,
        config_dict["ENTRY"],
        config_dict["EXIT"]
    )
    with open(config_dict["OUTPUT_FILE"], "w") as f:
        f.write(path_to_directions(path))
    print("Path written to file.")
