class InvalidMove:
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return "Invalid move with sequence: {0}".format(self.message)
        else:
            return "Invalid move played"


class Board(object):
    """
    A class used to represent a normal tic-tac-toe board

    Attributes
    ----------
    board_status : int list
        a list of ints representing a flattened out tic-tac-toe board
        visually:
                0 | 1 | 2
                ---------
                3 | 4 | 5
                ---------
                6 | 7 | 8
    won : int
        an integer representing which player has won the board
        (0 meaning neither)

    Methods
    -------
    make_move(player, move)
        Marks the spot referenced by int move as taken by player. If this move
        is illegal will raise InvalidMove, but this can (and should) be avoided
        by checking if moves are legal to begin with.
        Returns the spot taken (which will be the next big board used in
        ultimate tic-tac-toe), or -1 if the move has won the board.
    is_legal(move)
        Checks if the spot referenced by int move is available to be taken by a
        player.
    check_won
        Checks to see if a player has won the board.
        Returns winning player if so.
    """

    def __init__(self):
        self.board_status = [0 for i in range(9)]
        self.won = 0

    def make_move(self, player, move):
        if self.board_status[move] != 0:
            raise InvalidMove
        else:
            self.board_status[move] = player
            if self.check_won():
                return -1
            else:
                return move

    def is_legal(self, move):
        return self.board_status[move] == 0

    def check_rows(self):
        for i in range(3):
            row = i * 3
            if (
                self.board_status[row]
                == self.board_status[row + 1]
                == self.board_status[row + 2]
                and self.board_status[row] != 0
            ):
                return self.board_status[row]

    def check_columns(self):
        for i in range(3):
            if (
                self.board_status[i]
                == self.board_status[i + 3]
                == self.board_status[i + 6]
                and self.board_status[i] != 0
            ):
                return self.board_status[i]

    def check_diags(self):
        if (
            self.board_status[0] == self.board_status[4] == self.board_status[8]
            and self.board_status[0] != 0
        ):
            return self.board_status[0]
        if (
            self.board_status[2] == self.board_status[4] == self.board_status[6]
            and self.board_status[2] != 0
        ):
            return self.board_status[2]

    def check_won(self):
        rows, cols, diags = self.check_rows(), self.check_columns(), self.check_diags()
        if rows:
            self.won = rows
            return True
        if cols:
            self.won = cols
            return True
        if diags:
            self.won = diags
            return True
        return False


class BigBoard(Board):
    """
    A class used to represent an ultimate tic-tac-toe board

    Attributes
    ----------
    boards : Board list
        a list of the subboards that make up the ultimate tic-tac-toe board
    board_status : int list
        a list of ints representing the won status of the subboards
        Ex. if board_status[0] = 1, then player 1 has won board 0
    won : int
        an integer representing which player has won the ultimate tic-tac-toe
        game (0 meaning neither)

    Methods
    -------
    make_move(player, move)
        Marks the spot referenced by tuple move as taken by player. If this move
        is illegal will raise InvalidMove, but this can (and should) be avoided
        by checking if moves are legal to begin with.
        Returns the spot taken (which will be the next big board used in
        ultimate tic-tac-toe), or -1 if the move has won the board.
    is_legal(move)
        Checks if the spot referenced by int move is available to be taken by a
        player.
    check_won
        Checks to see if a player has won the board.
        Returns winning player if so.
    """

    def __init__(self, subboards):
        super(BigBoard, self).__init__()
        self.boards = subboards

    def make_move(self, player, move):
        big, small = move
        if self.boards[big].won == 0:
            result = self.boards[big].make_move(player, small)
            if result == -1:
                self.board_status[big] = player
            return result
        else:
            raise InvalidMove(move)

    def is_legal(self, move):
        big, small = move
        if big >= 0 and big < 9 and small >= 0 and small < 9:
            return self.boards[big].won == 0 and self.boards[big].is_legal(small)
        else:
            return False

    def check_rows(self):
        return super(BigBoard, self).check_rows()

    def check_columns(self):
        return super(BigBoard, self).check_columns()

    def check_diags(self):
        return super(BigBoard, self).check_diags()

    def check_won(self):
        return super(BigBoard, self).check_won()