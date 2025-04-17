"""
Represents the Reversi game board with basic operations.
"""

import copy
from checks import get_flips

class Board:
    def __init__(self):
        # 8x8 board grid: None for empty, 'B' or 'W' for pieces
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        # Starting position
        self.grid[3][3] = 'W'
        self.grid[3][4] = 'B'
        self.grid[4][3] = 'B'
        self.grid[4][4] = 'W'

    def clone(self):
        """
        Return a deep copy of the board.
        """
        new = Board.__new__(Board)
        new.grid = copy.deepcopy(self.grid)
        return new

    def __iter__(self):
        return iter(self.grid)

    def __getitem__(self, idx):
        return self.grid[idx]

    def in_bounds(self, r, c):
        """
        Check if (r, c) is within the board boundaries.
        """
        return 0 <= r < 8 and 0 <= c < 8

    def apply_move(self, color, r, c):
        """
        Apply a move for 'color' at (r, c), flipping the appropriate pieces.
        """
        flips = get_flips(self, color, r, c)
        self.grid[r][c] = color
        for fr, fc in flips:
            self.grid[fr][fc] = color

    def get_score(self):
        """
        Count and return the score as a dict {'B': count, 'W': count}.
        """
        counts = {'B': 0, 'W': 0}
        for row in self.grid:
            for cell in row:
                if cell in counts:
                    counts[cell] += 1
        return counts