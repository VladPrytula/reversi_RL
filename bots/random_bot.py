"""
Random selection bot for Reversi.
"""
import random

from bots.base import Bot


class RandomBot(Bot):
    """Bot that selects a move uniformly at random."""
    def move(self, game, color):
        moves = game.get_valid_moves(color)
        if not moves:
            return None
        return random.choice(moves)