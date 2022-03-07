"""
Represents the BetterOpponentPlayer type
"""
from board import Board
from players.random_player import RandomPlayer

class BetterOpponentPlayer(RandomPlayer):
    """
    A player that performs random piece placement unless it can win or lose, in which case, will attempt to block.
    """
    def __init__(self, marker, player_markers, placement_policy, win_condition):
        super().__init__(marker)
        self._placement_policy = placement_policy
        self._win_condition = win_condition
        self._player_markers = player_markers
    def place(self, board: Board):
        """
        Places a piece on the board
        """
        for x in range(board.depth):
            for y in range(board.width):
                for z in range(board.height):
                    if self._placement_policy(board, self._marker, x, y, z):
                        # Check if we can win anywhere
                        # Pseudo-place the piece so that win condition (which is dependent on board state) works behaves just fine
                        prev = board[x][y][z]
                        board[x][y][z] = self._marker
                        if self._win_condition(board, self._marker, x, y, z):
                            board[x][y][z] = prev
                            board.attempt_move(self._marker, x, y, z)
                            return
                        # Check if other opponents can win anywhere
                        for player_marker in self._player_markers:
                            board[x][y][z] = player_marker
                            if self._win_condition(board, player_marker, x, y, z):
                                board[x][y][z] = prev
                                board.attempt_move(self._marker, x, y, z)
                                return
                        board[x][y][z] = prev
        # If we cannot win or avoid losing anywhere, play somewhere random
        super().place(board)
