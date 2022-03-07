from enum import Enum, auto
from Board import Board

def column_check(board: Board, player, x, y, z):
    # Start at item, go left to start
    count = 0
    for i in range(z, -1, -1):
        if board[x][y][i] != player:
            break
        count += 1
    for i in range(z + 1, board.height):
        if board[x][y][i] != player:
            break
        count += 1
    return count
def row_check(board: Board, player, x, y, z):
    count = 0
    for i in range(y, -1, -1):
        if board[x][i][z] != player:
            break
        count += 1
    for i in range(y + 1, board.width):
        if board[x][i][z] != player:
            break
        count += 1
    return count
def depth_check(board: Board, player, x, y, z):
    count = 0
    for i in range(x, -1, -1):
        if board[i][y][z] != player:
            break
        count += 1
    for i in range(x + 1, board.depth):
        if board[i][y][z] != player:
            break
        count += 1
    return count

class DiagonalPlane(Enum):
    XY = auto()
    YZ = auto()
    XZ = auto()

def diagonal_check_plane_pair(lhs, max_lhs, rhs_valid, board_accessor, player):
    count = 0
    # Subtract from lhs and rhs until we hit 0 on both
    for delta in range(0, -lhs - 1, -1):
        if not rhs_valid(delta) or board_accessor(delta) != player:
            break
        count += 1
    for delta in range(1, max_lhs - lhs):
        if not rhs_valid(delta) or board_accessor(delta) != player:
            break
        count += 1
    return count

def diagonal_check_xy_plane_pair(board: Board, player, x, y, z, alternate_diagonals: bool):
    def rhs_valid(delta):
        if alternate_diagonals:
            if delta < 0:
                return y - delta < board.width
            return y - delta >= 0
        if delta < 0:
            return y + delta >= 0
        return y + delta < board.width
    def board_accessor(delta):
        if alternate_diagonals:
            return board[x + delta][y - delta][z]
        return board[x + delta][y][z]
    return diagonal_check_plane_pair(x, board.depth, rhs_valid, board_accessor, player)

def diagonal_check_xz_plane_pair(board: Board, player, x, y, z, alternate_diagonals):
    def rhs_valid(delta):
        if alternate_diagonals:
            if delta < 0:
                return z - delta < board.height
            return z - delta >= 0
        if delta < 0:
            return z + delta >= 0
        return z + delta < board.height
    def board_accessor(delta):
        if alternate_diagonals:
            return board[x + delta][y][z - delta]
        return board[x + delta][y][z + delta]
    return diagonal_check_plane_pair(x, board.depth, rhs_valid, board_accessor, player)

def diagonal_check_yz_plane_pair(board: Board, player, x, y, z, alternate_diagonals: bool):
    def rhs_valid(delta):
        if alternate_diagonals:
            if delta < 0:
                return z - delta < board.height
            return z - delta >= 0
        if delta < 0:
            return z + delta >= 0
        return z + delta < board.height
    def board_accessor(delta):
        if alternate_diagonals:
            return board[x][y + delta][z - delta]
        return board[x][y + delta][z + delta]
    return diagonal_check_plane_pair(y, board.width, rhs_valid, board_accessor, player)

def diagonal_check_plane(board: Board, player, x, y, z, plane: DiagonalPlane):
    # Each of these planes consist of two diagonals, so lets apply each of those in turn
    if plane == DiagonalPlane.XY:
        return max(diagonal_check_xy_plane_pair(board, player, x, y, z, False), diagonal_check_xy_plane_pair(board, player, x, y, z, True))
    elif plane == DiagonalPlane.XZ:
        return max(diagonal_check_xz_plane_pair(board, player, x, y, z, False), diagonal_check_xz_plane_pair(board, player, x, y, z, True))
    elif plane == DiagonalPlane.YZ:
        return max(diagonal_check_yz_plane_pair(board, player, x, y, z, False), diagonal_check_yz_plane_pair(board, player, x, y, z, True))
    return 0
        
def diagonal_check(board: Board, player, x, y, z):
    # There exist three planes and their opposites:
    # +xy, +xz, +yz
    return max(
        diagonal_check_plane(board, player, x, y, z, DiagonalPlane.XY),
        diagonal_check_plane(board, player, x, y, z, DiagonalPlane.XZ),
        diagonal_check_plane(board, player, x, y, z, DiagonalPlane.YZ)
    )
