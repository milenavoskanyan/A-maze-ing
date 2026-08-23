PATTERN_42 = [
    [1, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1, 1]
]

def is_42_cell(width: int, height: int, r: int, c: int) -> bool:
    if width < 9 or height < 7:
        return False

    start_row = (height - 5) // 2
    start_col = (width - 7) // 2

    pattern_r = r - start_row
    pattern_c = c - start_col

    if not (0 <= pattern_r < 5 and 0 <= pattern_c < 7):
        return False

    return PATTERN_42[pattern_r][pattern_c] == 1
