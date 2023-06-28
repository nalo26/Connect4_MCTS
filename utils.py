def rotate_board(board: list[list[int]]):
    """Rotate the board 90 degrees clockwise"""
    return list(zip(*board[::-1]))


def rows_to_strings(board: list[list[int]]):
    """Convert rows to strings"""
    return ["".join(map(str, row)) for row in board]


def diagonals_board(board: list[list[int]]):
    """Get the diagonals of the board"""
    h, w = len(board), len(board[0])
    return [
        [board[h - p + q - 1][q] for q in range(max(p - h + 1, 0), min(p + 1, w))]
        for p in range(h + w - 1)
    ] + [
        [board[p - q][q] for q in range(max(p - h + 1, 0), min(p + 1, w))]
        for p in range(h + w - 1)
    ]
