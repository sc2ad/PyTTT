"""
Represents a player that can take input from a human
"""

from players.player import Player
from board import Board

def _parse_input(input_string: str, max_length: int) -> int:
    output = 0
    while output < 1 or output > max_length:
        val = input(f"Enter a {input_string} to place your piece: ").strip()
        if not val.isnumeric():
            print(f"{val} is not a number!")
        else:
            output = int(val)
        if output < 1 or output > max_length:
            print(f"Input must be 1 or more, and less than {max_length}!")
    return output - 1

class InputPlayer(Player):
    """
    A player that can take input from the console
    """
    def place(self, board: Board):
        while True:
            if board.depth > 1:
                depth = _parse_input("depth", board.depth)
            else:
                depth = 0
            row = _parse_input("row", board.height)
            col = _parse_input("column", board.width)
            if board.attempt_move(self._marker, depth, col, row):
                break
            print("Invalid move!")
