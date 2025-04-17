"""
Rule checking and utility functions for Reversi.
"""

# Directions for flipping: eight directions
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),          (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]

def opponent(color):
    """
    Return the opponent's color.
    """
    return 'W' if color == 'B' else 'B'

def get_flips(board, color, r, c):
    """
    Return a list of positions that would be flipped if 'color' plays at (r, c).
    """
    flips = []
    opp = opponent(color)
    for dr, dc in DIRECTIONS:
        rr, cc = r + dr, c + dc
        path = []
        while board.in_bounds(rr, cc) and board.grid[rr][cc] == opp:
            path.append((rr, cc))
            rr += dr
            cc += dc
        if path and board.in_bounds(rr, cc) and board.grid[rr][cc] == color:
            flips.extend(path)
    return flips

def would_flip(board, color, r, c):
    """
    Check if placing at (r, c) would flip at least one opponent piece.
    """
    return bool(get_flips(board, color, r, c))

def get_valid_moves(board, color):
    """
    Return a list of valid moves (r, c) for 'color' on the given board.
    """
    moves = []
    for r in range(8):
        for c in range(8):
            if board.grid[r][c] is not None:
                continue
            if would_flip(board, color, r, c):
                moves.append((r, c))
    return moves

def has_valid_move(board, color):
    """
    Return True if 'color' has at least one valid move remaining.
    """
    return bool(get_valid_moves(board, color))