from players.Player import Player
from Board import Board
import random

class BetterOpponentPlayer(Player):
    def __init__(self, marker, player_markers, placement_policy, win_condition):
        super().__init__(marker)
        self._placement_policy = placement_policy
        self._win_condition = win_condition
        self._player_markers = player_markers
    def place(self, board: Board):
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
                        else:
                            # Check if other opponents can win anywhere
                            for player_marker in self._player_markers:
                                board[x][y][z] = player_marker
                                if self._win_condition(board, player_marker, x, y, z):
                                    board[x][y][z] = prev
                                    board.attempt_move(self._marker, x, y, z)
                                    return
                            board[x][y][z] = prev
        # If we cannot win or avoid losing anywhere, play somewhere random
        while True:
            depth = random.randint(0, board.depth - 1)
            col = random.randint(0, board.width - 1)
            row = random.randint(0, board.height - 1)

            if board.attempt_move(self._marker, depth, col, row):
                return
