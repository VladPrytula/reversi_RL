"""
Alpha-Beta pruning bot for Reversi.
"""
import math

from bots.base import Bot
from game import opponent


class AlphaBetaBot(Bot):
    """Bot that uses alpha-beta pruning to choose moves."""
    def __init__(self, max_depth=3):
        self.max_depth = max_depth

    def move(self, game, color):
        """Compute best move using alpha-beta search."""
        def evaluate(g):
            score = g.get_score()
            return score[color] - score[opponent(color)]

        def ab_search(g, depth, maximizing_color, current_color, alpha, beta):
            if depth == 0 or g.is_game_over():
                return evaluate(g), None
            moves = g.get_valid_moves(current_color)
            if not moves:
                g2 = g.clone()
                g2.current_player = opponent(current_color)
                return ab_search(g2, depth - 1, maximizing_color, opponent(current_color), alpha, beta)[0], None
            best_move = None
            if current_color == maximizing_color:
                value = -math.inf
                for move in moves:
                    g2 = g.clone()
                    g2.apply_move(current_color, move[0], move[1])
                    score, _ = ab_search(g2, depth - 1, maximizing_color, opponent(current_color), alpha, beta)
                    if score > value:
                        value = score
                        best_move = move
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
                return value, best_move
            else:
                value = math.inf
                for move in moves:
                    g2 = g.clone()
                    g2.apply_move(current_color, move[0], move[1])
                    score, _ = ab_search(g2, depth - 1, maximizing_color, opponent(current_color), alpha, beta)
                    if score < value:
                        value = score
                        best_move = move
                    beta = min(beta, value)
                    if beta <= alpha:
                        break
                return value, best_move

        _, move = ab_search(game.clone(), self.max_depth, color, color, -math.inf, math.inf)
        return move