"""
Represents a player that chooses its moves randomly
"""

import random
from players.player import Player
from board import Board

class RandomPlayer(Player):
    """
    A player that plays randomly
    """
    def place(self, board: Board):
        """
        Places a piece on the board
        """
        while True:
            depth = random.randint(0, board.depth - 1)
            col = random.randint(0, board.width - 1)
            row = random.randint(0, board.height - 1)

            if board.attempt_move(self._marker, depth, col, row):
                return
