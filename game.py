import copy

# Directions for flipping: eight directions
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),          (0, 1),
    (1, -1),  (1, 0),  (1, 1)
]


def opponent(color):
    return 'W' if color == 'B' else 'B'


class ReversiGame:
    def __init__(self, game_id, players):
        self.id = game_id
        # players: dict mapping 'B' or 'W' to 'human', 'random', or 'ab'
        self.players = players
        # Initialize 8x8 board: None for empty, 'B' or 'W' for stones
        self.board = [[None for _ in range(8)] for _ in range(8)]
        # Starting position
        self.board[3][3] = 'W'
        self.board[3][4] = 'B'
        self.board[4][3] = 'B'
        self.board[4][4] = 'W'
        self.current_player = 'B'
        # Graceful end flags
        self.ended = False
        self.ended_by = None

    def clone(self):
        # Deep copy the game state
        return copy.deepcopy(self)

    def in_bounds(self, r, c):
        return 0 <= r < 8 and 0 <= c < 8

    def get_valid_moves(self, color):
        moves = []
        for r in range(8):
            for c in range(8):
                if self.board[r][c] is not None:
                    continue
                if self._would_flip(r, c, color):
                    moves.append((r, c))
        return moves

    def _would_flip(self, r, c, color):
        # Check if placing at (r,c) would flip at least one opponent piece
        opp = opponent(color)
        for dr, dc in DIRECTIONS:
            rr, cc = r + dr, c + dc
            found_opp = False
            while self.in_bounds(rr, cc) and self.board[rr][cc] == opp:
                found_opp = True
                rr += dr
                cc += dc
            if found_opp and self.in_bounds(rr, cc) and self.board[rr][cc] == color:
                return True
        return False

    def apply_move(self, color, r, c):
        # Assumes move is valid
        flips = []
        opp = opponent(color)
        for dr, dc in DIRECTIONS:
            rr, cc = r + dr, c + dc
            path = []
            while self.in_bounds(rr, cc) and self.board[rr][cc] == opp:
                path.append((rr, cc))
                rr += dr
                cc += dc
            if path and self.in_bounds(rr, cc) and self.board[rr][cc] == color:
                flips.extend(path)
        # Place piece
        self.board[r][c] = color
        # Flip pieces
        for fr, fc in flips:
            self.board[fr][fc] = color
        # Switch turn
        self.current_player = opponent(color)

    def has_valid_move(self, color):
        return bool(self.get_valid_moves(color))

    def is_game_over(self):
        # Game over if gracefully ended or neither player has a valid move
        return self.ended or (not self.has_valid_move('B') and not self.has_valid_move('W'))

    def get_score(self):
        counts = {'B': 0, 'W': 0}
        for row in self.board:
            for cell in row:
                if cell in counts:
                    counts[cell] += 1
        return counts
    
    def end(self, by):
        """Gracefully end the game, e.g. by a human player"""
        self.ended = True
        self.ended_by = by

