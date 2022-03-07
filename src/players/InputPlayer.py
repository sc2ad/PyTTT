from players.Player import Player
from Board import Board

class InputPlayer(Player):
    def __init__(self, marker):
        super().__init__(marker)

    def _parse_input(self, input_string: str, max_length: int) -> int:
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

    def place(self, board: Board):
        while True:
            if board.depth > 1:
                depth = self._parse_input("depth", board.depth)
            else:
                depth = 0
            row = self._parse_input("row", board.height)
            col = self._parse_input("column", board.width)
            if board.attempt_move(self._marker, depth, col, row):
                break
            print("Invalid move!")
