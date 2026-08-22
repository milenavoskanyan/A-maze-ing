import random
from typing import Tuple, List, Set


class MazeGenerator:
    PATTERN_42 = [
        [1, 0, 0, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1],
        [0, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 1, 1]
    ]

    def __init__(
            self,
            width: int,
            height: int,
            entry: Tuple[int, int],  # unused. do we need these here?
            exit: Tuple[int, int],  # default values?
            perfect=True,
            seed=None
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.seed = seed

    def generate(self) -> List[List[int]]:
        grid = [[15] * self.width for _ in range(self.height)]
        visited = [[False] * self.width for _ in range(self.height)]

        if not self._has_42():
            print("Error: Maze size is too small to fit the '42' pattern.")
        else:
            self._place_42_pattern(grid, visited)

        while True:
            start_r = random.randrange(self.height)
            start_c = random.randrange(self.width)

            if not visited[start_r][start_c]:
                break  # exclude the 42 path

        visited[start_r][start_c] = True

        frontier: Set[Tuple[int, int]] = set()
        frontier.update(self._get_neighbors(start_r, start_c, visited, False))

        while frontier:
            cur_r, cur_c = random.choice(tuple(frontier))
            frontier.remove((cur_r, cur_c))
            visited_neighbors = self._get_neighbors(
                cur_r, cur_c, visited, True
                )
            valid_neighbors = self._get_valid_neighbors(visited_neighbors)
            if valid_neighbors:
                connect_to_r, connect_to_c = random.choice(valid_neighbors)
                self._remove_wall(
                    cur_r, cur_c, connect_to_r, connect_to_c, grid
                    )
            visited[cur_r][cur_c] = True
            unvisited_neighbors = self._get_neighbors(
                cur_r, cur_c, visited, False
                                                      )
            frontier.update(self._get_valid_neighbors(unvisited_neighbors))

        return grid

    def _remove_wall(
        self,
        r1: int,
        c1: int,
        r2: int,
        c2: int,
        grid: List[List[int]]
    ) -> None:
        if r2 == r1 - 1:  # north
            grid[r1][c1] &= ~1
            grid[r2][c2] &= ~4
        elif r2 == r1 + 1:  # south
            grid[r1][c1] &= ~4
            grid[r2][c2] &= ~1
        elif c2 == c1 - 1:  # west
            grid[r1][c1] &= ~8
            grid[r2][c2] &= ~2
        elif c2 == c1 + 1:  # east
            grid[r1][c1] &= ~2
            grid[r2][c2] &= ~8

    def _get_neighbors(
        self,
        r: int,
        c: int,
        visited: List[List[bool]],
        want_visited: bool
    ) -> List[Tuple[int, int]]:
        neighbors: List[Tuple[int, int]] = []

        directions = (
            (0, 1),
            (1, 0),
            (0, -1),
            (-1, 0)
        )

        for dr, dc in directions:
            neighbor_r = r + dr
            neighbor_c = c + dc

            if (self._is_valid_cell(neighbor_r, neighbor_c) and
                    visited[neighbor_r][neighbor_c] == want_visited):
                neighbors.append((neighbor_r, neighbor_c))

        return neighbors

    def _place_42_pattern(
            self,
            grid: List[List[int]],
            visited: List[List[bool]]
    ) -> None:
        start_row = (self.height - 5) // 2
        start_col = (self.width - 7) // 2

        for r_idx, row_vals in enumerate(self.PATTERN_42):
            for c_idx, val in enumerate(row_vals):
                r = start_row + r_idx
                c = start_col + c_idx

                if val == 1:
                    visited[r][c] = True

                    if (r_idx > 0 and
                            self.PATTERN_42[r_idx - 1][c_idx] == 1):
                        grid[r][c] &= ~1      # Remove North wall (1)
                        grid[r - 1][c] &= ~4  # neighbor wall
                    if (r_idx < 4 and
                            self.PATTERN_42[r_idx + 1][c_idx] == 1):
                        grid[r][c] &= ~4      # Remove South wall (4)
                        grid[r + 1][c] &= ~1  # neighbor wall
                    if (c_idx > 0 and
                            self.PATTERN_42[r_idx][c_idx - 1] == 1):
                        grid[r][c] &= ~8      # Remove West wall (8)
                        grid[r][c - 1] &= ~2  # neighbor wall
                    if (c_idx < 6 and
                            self.PATTERN_42[r_idx][c_idx + 1] == 1):
                        grid[r][c] &= ~2      # Remove East wall (2)
                        grid[r][c + 1] &= ~8  # neighbor wall

    def _has_42(self) -> bool:
        return self.width >= 9 and self.height >= 7

    def _is_42_cell(self, r: int, c: int) -> bool:
        if not self._has_42():
            return False

        start_row = (self.height - 5) // 2
        start_col = (self.width - 7) // 2

        pattern_r = r - start_row
        pattern_c = c - start_col

        if not (0 <= pattern_r < 5 and 0 <= pattern_c < 7):
            return False

        return self.PATTERN_42[pattern_r][pattern_c] == 1

    def _is_valid_cell(self, r: int, c: int) -> bool:
        return 0 <= r < self.height and 0 <= c < self.width

    def _get_valid_neighbors(
        self,
        neighbors: List[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        return [
            (r, c)
            for r, c in neighbors
            if not self._is_42_cell(r, c)
        ]
