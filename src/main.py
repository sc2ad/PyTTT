from email.policy import default
from random import Random
from venv import create
from Board import Board
from players.Player import Player
from players.RandomPlayer import RandomPlayer
from utils import *
from players.InputPlayer import InputPlayer
from players.BetterOpponentPlayer import BetterOpponentPlayer
import input_helpers
import time

def exactly_n(n: int):
    def win(board: Board, player, x, y, z):
        return column_check(board, player, x, y, z) == n or \
            row_check(board, player, x, y, z) == n or \
            depth_check(board, player, x, y, z) == n or \
            diagonal_check(board, player, x, y, z) == n
    return win

def at_least_n(n: int):
    def win(board: Board, player, x, y, z):
        return column_check(board, player, x, y, z) >= n or \
            row_check(board, player, x, y, z) >= n or \
            depth_check(board, player, x, y, z) >= n or \
            diagonal_check(board, player, x, y, z) >= n
    return win

def place_on_none(board: Board, player, x, y, z):
    return board[x][y][z] == None

def lifetime_n(n: int):
    def placement(board: Board, player, x, y, z):
        count = 0
        for i in range(len(board.last_moves) - 1, -1, -1):
            lx, ly, lz, lp = board.last_moves[i]
            if x == lx and y == ly and z == lz:
                return False
            count += 1
            if count >= n:
                return True
        return True
    return placement

def play_game(game_board: Board, players: "list[Player]"):
    # Render the game board now, then render it after each player move
    game_board.print_board()
    while True:
        # Have player one go, then other players (if they exist)
        for i in range(len(players)):
            print(f"Player {i + 1}'s turn!")
            players[i].place(game_board)
            game_board.print_board()
            if game_board.has_won(players[i].marker):
                print(f"Player {i + 1} (with marker: {players[i].marker}) won after {game_board.move_count} total moves!")
                return players[i]
            elif game_board.has_ended():
                print(f"Game has ended in a draw after {game_board.move_count} total moves!")
                return None

def watch_replay(board: Board, winner: Player):
    board.reset()
    board.print_board()
    for x, y, z, player in board.last_moves:
        board[x][y][z] = player
        time.sleep(1)
        print(f"Player with marker: {player}'s turn!")
        board.print_board()
    if winner:
        print(f"Player with marker: {winner.marker} won after {board.move_count} total moves!")
    else:
        print(f"The game ended in a draw after: {board.move_count} total moves!")

def create_game():
    print("Create a new TicTacToe game:")
    # Select mode of play
    input_not_valid = True
    while input_not_valid:
        mode = input_helpers.selector("Select your mode of play", ["versus", "puzzle"], "versus")
        if mode == "puzzle":
            print("This mode is not yet available! Please select a different mode!")
        elif mode == "versus":
            input_not_valid = False
    
    width = input_helpers.number("Enter the width of the game board", 2, 50, 3)
    height = input_helpers.number("Enter the height of the game board", 2, 50, 3)
    depth = input_helpers.number("Enter the depth of the game board (3rd dimension)", 1, 5, 1)

    # Select win condition
    win_condition = input_helpers.selector("Select the win condition for your versus game", ["exact", "at least"], "at least")
    if win_condition == "exact":
        win_amount = min(width, height, depth)
        win_amount = input_helpers.number("Select the quantity to win by", win_amount, max(width, height, depth), win_amount)
        win_condition = exactly_n(win_amount)
    elif win_condition == "at least":
        win_amount = min(width, height)
        win_amount = input_helpers.number("Select the quantity to win by", min(width, height, depth), max(width, height, depth), win_amount)
        win_condition = at_least_n(win_amount)
    
    # Select placement policy
    placement_policy = input_helpers.selector("Specify the placement policy", ["empty tiles only", "lifetime"], "empty tiles only")
    if placement_policy == "lifetime":
        placement_policy = lifetime_n(input_helpers.number("Select the lifetime of any given piece in turns", win_amount // 2, width * height * depth - 1, 4))
        max_moves = input_helpers.number("Enter the maximum number of moves", width * height * depth, 10000, width * height * depth)
    elif placement_policy == "empty tiles only":
        placement_policy = place_on_none
        max_moves = width * height * depth

    # Create game board
    game_board = Board(win_condition, placement_policy, max_moves, width, height, depth)

    # Ask for players
    player_count = input_helpers.number("Select the total number of players", 2, 10, 2)
    players = []
    markers = []
    for i in range(player_count):
        if i == 0:
            default_marker = "X"
            default_player = "human"
        elif i == 1:
            default_marker = "O"
            default_player = None
        else:
            default_marker = None
            default_player = None
        player_type = input_helpers.selector(f"Select the player type for player {i + 1}", ["human", "novice", "easy"], default_player)
        player_marker = input_helpers.get_marker(i + 1, markers, default_marker)
        markers.append(player_marker)
        if player_type == "human":
            players.append(InputPlayer(player_marker))
        elif player_type == "novice":
            players.append(RandomPlayer(player_marker))
        elif player_type == "easy":
            players.append(BetterOpponentPlayer(player_marker, markers, placement_policy, win_condition))
    return game_board, players

def main():
    print("==============================")
    print("Welcome to TicTacToe!")
    print("==============================")
    
    replay = True
    while replay:
        game_board, players = create_game()
        print("==============================")
        print("BEGIN!")
        winner = play_game(game_board, players)
        while True:
            response = input_helpers.selector("Would you like to watch the replay, play again, or exit", ["watch replay", "play again", "exit"], "exit")
            if response == "watch replay":
                watch_replay(game_board, winner)
            elif response == "exit":
                print("Thank you for playing! :-)")
                return
            else:
                break
        

if __name__ == "__main__":
    main()