"""
Main file for TicTacToe Python
"""
import time
from board import Board
import utils
from players.player import Player
from players.random_player import RandomPlayer
from players.input_player import InputPlayer
from players.better_opponent_player import BetterOpponentPlayer
import input_helpers

def exactly_n(n: int):
    """
    Returns a function that represents a board win condition of exactly n
    """
    def win(board: Board, player, x, y, z):
        """
        A win condition that checks for exactly n matches
        """
        return utils.column_check(board, player, x, y, z) == n or \
            utils.row_check(board, player, x, y, z) == n or \
            utils.depth_check(board, player, x, y, z) == n or \
            utils.diagonal_check(board, player, x, y, z) == n
    return win

def at_least_n(n: int):
    """
    Returns a function that represents a board win condition of at least n, this is the default for tictactoe
    """
    def win(board: Board, player, x, y, z):
        """
        A win condition that checks for at least n matches
        """
        return utils.column_check(board, player, x, y, z) >= n or \
            utils.row_check(board, player, x, y, z) >= n or \
            utils.depth_check(board, player, x, y, z) >= n or \
            utils.diagonal_check(board, player, x, y, z) >= n
    return win

def place_on_none(board: Board, player, x, y, z):
    """
    A placement policy that only allows for placing on pieces that have not been placed on
    """
    # pylint: disable=unused-argument
    return board[x][y][z] is None

def lifetime_n(n: int):
    """
    Returns a placement policy that allows for overwriting piece placements after n total turns have passed
    """
    def placement(board: Board, player, x, y, z):
        """
        A placement policy that allows allows for overwriting piece placements based off of n
        """
        # pylint: disable=unused-argument
        count = 0
        for i in range(len(board.last_moves) - 1, -1, -1):
            lx, ly, lz, _ = board.last_moves[i]
            # pylint: disable=unused-variable
            if x == lx and y == ly and z == lz:
                return False
            count += 1
            if count >= n:
                return True
        return True
    return placement

def play_game(game_board: Board, players: "list[Player]"):
    """
    Play a game with the given board and players
    """
    # Render the game board now, then render it after each player move
    game_board.print_board()
    while True:
        # Have player one go, then other players (if they exist)
        for i, player in enumerate(players):
            print(f"Player {i + 1}'s turn!")
            player.place(game_board)
            game_board.print_board()
            if game_board.has_won(player.marker):
                print(f"Player {i + 1} (with marker: {player.marker}) won after {game_board.move_count} total moves!")
                return player
            if game_board.has_ended():
                print(f"Game has ended in a draw after {game_board.move_count} total moves!")
                return None

def watch_replay(board: Board, winner: Player):
    """
    Watches the given (completed) board replay, with the provided winner that may be None
    """
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

def get_game_params():
    """
    Asks the user for the game parameters
    """
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
    return mode, width, height, depth

def get_players(placement_policy, win_condition):
    """
    Ask the user for how many players and who is playing
    """
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
    return players

def create_game():
    """
    Creates a new game of TicTacToe and returns the game and the players playing
    """
    print("Create a new TicTacToe game:")
    _, width, height, depth = get_game_params()

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
    return game_board, get_players(placement_policy, win_condition)

def main():
    """
    Runs the main game and loops
    """
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
