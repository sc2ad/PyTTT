"""
Represents a generic player type
"""
from board import Board

class Player:
    """
    An arbitrary TicTacToe player
    """
    def __init__(self, marker):
        self._marker = marker

    def place(self, board: Board):
        """
        Places a piece on the board
        """
        raise NotImplementedError

    @property
    def marker(self):
        """
        The marker for this player
        """
        return self._marker
