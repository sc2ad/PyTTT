from Board import Board

class Player:
    def __init__(self, marker):
        self._marker = marker

    def place(self, board: Board):
        raise NotImplementedError

    @property
    def marker(self):
        return self._marker
