import random
from players.Player import Player
from Board import Board

class RandomPlayer(Player):
    def __init__(self, marker):
        super().__init__(marker)
    
    def place(self, board: Board):
        while True:
            depth = random.randint(0, board.depth - 1)
            col = random.randint(0, board.width - 1)
            row = random.randint(0, board.height - 1)

            if board.attempt_move(self._marker, depth, col, row):
                return
