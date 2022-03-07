from Board import Board
from utils import *

def exactly_n(n: int):
    def win(board: Board, player, x, y, z):
        return column_check(board, player, x, y, z) == n or \
            row_check(board, player, x, y, z) == n or \
            depth_check(board, player, x, y, z) == n or \
            diagonal_check(board, player, x, y, z) == n
    return win

def place_on_none(board: Board, player, x, y, z):
    return board[x][y][z] == None

game_board = Board(exactly_n(3), place_on_none, 4, 3, 1)
game_board.attempt_move("X", 0, 0, 0)
game_board.attempt_move("X", 0, 1, 1)
game_board.attempt_move("X", 0, 2, 2)
game_board.print_board()
print(game_board.has_won("X"))
game_board.attempt_move("X", 0, 1, 0)
game_board.print_board()
print(game_board.has_won("X"))
game_board.attempt_move("X", 0, 2, 0)
game_board.print_board()
print(game_board.has_won("X"))
game_board.attempt_move("X", 0, 3, 0)
game_board.print_board()
print(game_board.has_won("X"))
