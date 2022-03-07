
def _pretty_print_item(item):
    if item != None:
        return item
    return "-"

class Board:
    def __init__(self, win_condition, valid_move, max_moves: int, width: int, height: int, depth: int = 1):
        self.width = width
        self.height = height
        self.depth = depth
        self._move_count = 0
        self._winning_player = None
        self._check_winning_functor = win_condition
        self._valid_move_functor = valid_move
        self._last_moves = []
        self._max_moves = max_moves
        self.reset()

    def initialize_board(self, initializer_functor):
        for x in range(self.depth):
            for y in range(self.width):
                for z in range(self.height):
                    self.board[x][y][z] = initializer_functor(x, y, z)

    def reset(self):
        self.board = [[[None for _ in range(self.height)] for _ in range(self.width)] for _ in range(self.depth)]
    
    @property
    def move_count(self):
        return self._move_count
    @property
    def last_moves(self):
        return self._last_moves
    @property
    def max_moves(self):
        return self._max_moves

    def _check_win(self, player, x, y, z):
        """
        Assigns _winning_player if the given player has won after placing a piece at the given coordinates.
        If remove_current_winner is True, the current winner is replaced with the result.
        Otherwise does nothing.
        """
        result = self._check_winning_functor(self, player, x, y, z)
        if result:
            # this player has won
            self._winning_player = player
        else:
            # if the current player was winning, they are no longer winning:
            if self._winning_player == player:
                self._winning_player = None
        # Otherwise, whoever was currently winning still should be winning, so don't touch _winning_player

    def has_won(self, player) -> bool:
        """
        Returns true if the given player has won.
        This value must be checked, since a given player could win on one piece placement, but no longer be winning on the next.
        """
        return self._winning_player == player
    
    def has_ended(self) -> bool:
        return self._move_count >= self._max_moves

    def attempt_move(self, player, x, y, z) -> bool:
        # Check that the move is valid (satisfies the overwrite condition)
        # Increment move count if success
        if self._valid_move_functor(self, player, x, y, z):
            self.board[x][y][z] = player
            # If we have a success, check to see who won
            self._check_win(player, x, y, z) 
            self._move_count += 1
            self._last_moves.append((x, y, z, player))
            return True
        return False

    def __getitem__(self, depth):
        return self.board[depth]

    def print_board(self):
        for board in range(self.depth):
            if board > 0:
                print(f"Depth: {board}")
            for row in range(self.height):
                st = ""
                for col in range(self.width):
                    st += _pretty_print_item(self.board[board][col][row])
                print(st)
