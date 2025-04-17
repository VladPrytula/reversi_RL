"""
Game logic for Reversi using modular board and rule-checking components.
"""

from board import Board
from checks import opponent, get_valid_moves, has_valid_move

class ReversiGame:
    """
    Represents a Reversi game, managing players, board state, and turn logic.
    """
    def __init__(self, game_id, players):
        """
        Initialize a new Reversi game.

        Args:
            game_id: Unique identifier for the game.
            players: Dict mapping 'B' and 'W' to Player instances.
        """
        self.id = game_id
        self.players = players
        self.board = Board()
        self.current_player = 'B'
        self.ended = False
        self.ended_by = None

    def clone(self):
        """
        Return a deep copy of the game state for simulation.
        """
        new = ReversiGame.__new__(ReversiGame)
        new.id = self.id
        new.players = self.players
        new.board = self.board.clone()
        new.current_player = self.current_player
        new.ended = self.ended
        new.ended_by = self.ended_by
        return new

    def get_valid_moves(self, color):
        """
        Return a list of valid moves (r, c) for the given color.
        """
        return get_valid_moves(self.board, color)

    def apply_move(self, color, r, c):
        """
        Apply a move for 'color' at (r, c), flipping pieces and switching turn.
        """
        self.board.apply_move(color, r, c)
        self.current_player = opponent(color)

    def has_valid_move(self, color):
        """
        Return True if 'color' has any valid moves remaining.
        """
        return has_valid_move(self.board, color)

    def is_game_over(self):
        """
        Return True if the game is over due to no valid moves or graceful end.
        """
        return self.ended or (not self.has_valid_move('B') and not self.has_valid_move('W'))

    def get_score(self):
        """
        Return current score as a dict {'B': count, 'W': count}.
        """
        return self.board.get_score()

    def end(self, by):
        """
        Gracefully end the game by the human player 'by'.
        """
        self.ended = True
        self.ended_by = by