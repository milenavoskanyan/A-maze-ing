from collections import deque
from utils import DIRECTIONS, has_wall, is_42_cell, is_valid_cell


def everything_is_okay(
        grid: list[list[int]],
        width: int,
        height: int,
        cur_r: int,
        cur_c: int,
        neigh_r: int,
        neigh_c: int,
        parent: list[list[tuple[int, int] | None]] = []
) -> bool:
    return (
        is_valid_cell(height, width, neigh_r, neigh_c)
        and not is_42_cell(width, height, neigh_r, neigh_c)
        and has_wall(cur_c, cur_r, neigh_c, neigh_r, grid[cur_r][cur_c])
        and parent[neigh_r][neigh_c] == (-1, -1)
    )


def shortest_path(
        grid: list[list[int]],
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
) -> list[tuple[int, int]]:
    q_fwd: deque[tuple[int, int]] = deque()
    parent_fwd: list[list[tuple[int, int] | None]]
    parent_fwd = [[(-1, -1) for _ in range(width)] for _ in range(height)]
    q_bwd: deque[tuple[int, int]] = deque()
    parent_bwd: list[list[tuple[int, int] | None]]
    parent_bwd = [[(-1, -1) for _ in range(width)] for _ in range(height)]

    entry_r = entry[0]
    entry_c = entry[1]
    exit_r = exit[0]
    exit_c = exit[1]

    q_fwd.append(entry)
    parent_fwd[entry_r][entry_c] = None
    q_bwd.append(exit)
    parent_bwd[exit_r][exit_c] = None

    while True:
        fwd_r, fwd_c = q_fwd.popleft()
        bwd_r, bwd_c = q_bwd.popleft()

        for dr, dc in DIRECTIONS:
            neigh_fwd_r = fwd_r + dr
            neigh_fwd_c = fwd_c + dc
            neigh_bwd_r = bwd_r + dr
            neigh_bwd_c = bwd_c + dc

            if everything_is_okay(
                grid,
                width,
                height,
                fwd_r,
                fwd_c,
                neigh_fwd_r,
                neigh_fwd_c,
                parent_fwd
            ):
                res1: tuple[int, int] = (neigh_fwd_r, neigh_fwd_c)
                q_fwd.append(res1)

            if everything_is_okay(
                grid,
                width,
                height,
                bwd_r,
                bwd_c,
                neigh_bwd_r,
                neigh_bwd_c,
                parent_bwd
            ):
                res2: tuple[int, int] = (neigh_bwd_r, neigh_bwd_c)
                q_fwd.append(res2)
