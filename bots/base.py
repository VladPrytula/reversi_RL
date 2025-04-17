"""
Base classes for players and bots in Reversi.
"""

class Player:
    """Abstract base class for any player."""
    def is_human(self):
        """Return True if this player is human."""
        return False

    def move(self, game, color):
        """Return the move for this player: (row, col) or None."""
        raise NotImplementedError("Bot must implement move method")


class Human(Player):
    """Represents a human player."""
    def is_human(self):
        return True

    def move(self, game, color):
        """Human players do not auto-move."""
        raise NotImplementedError("Human players do not auto-move")


class Bot(Player):
    """Base class for AI bots."""
    pass