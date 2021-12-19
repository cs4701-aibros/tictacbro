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
        (0 meaning still in progress, -1 meaning all squares are full with no
        winner (ie. a draw))

    Methods
    -------
    make_move(player, move)
        Marks the spot referenced by int move as taken by player. If this move
        is illegal will return None, but this can (and should) be avoided
        by checking if moves are legal to begin with.
        Returns the spot taken (the next big board used in ultimate tic-tac-toe)
        and a bool which indicates whether the board is done.
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
            return
        self.board_status[move] = player
        if self.check_won() or self.check_draw():
            return (move, True)
        else:
            return (move, False)

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
            return rows
        if cols:
            self.won = cols
            return cols
        if diags:
            self.won = diags
            return diags
        return 0

    def check_draw(self):
        if not self.check_won():
            for i in range(9):
                if self.board_status[i] == 0:
                    return False
            self.won = -1
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
    prev_move : 3-int tuple of the form (big, small, player_number) with
        big representing the subboard and small representing the spot on the
        subboard (-1, -1, 1) if there is no previous move (initial state and
        player 1 goes first)
    won : int
        an integer representing which player has won the ultimate tic-tac-toe
        game (0 meaning still in progress, -1 meaning all squares are full with
        no winner (ie. a draw))

    Methods
    -------
    make_move(agent, move)
        Marks the spot referenced by tuple move as taken by agent. If this move
        is illegal will raise InvalidMove, but this can (and should) be avoided
        by checking if moves are legal to begin with.
        Returns the spot taken (which will be the next big board used in
        ultimate tic-tac-toe)
    is_legal(move)
        Checks if the spot referenced by int move is available to be taken by a
        agent.
    check_won
        Checks to see if an agent has won the board.
        Returns winning agent if so.
    """

    def __init__(self):
        super(BigBoard, self).__init__()
        self.boards = [Board() for i in range(9)]
        self.next_board = -1
        self.prev_move = (-1, -1, 1)

    def play_turn(self, agent, move):
        big, small = move
        subboard = big
        if self.next_board != -1:
            subboard = self.next_board
        if self.boards[subboard].won == 0:
            move, finished = self.boards[subboard].make_move(agent, small)
            if finished:
                self.board_status[subboard] = self.boards[subboard].won
            self.prev_move = (big, small, agent)
            if self.boards[move].won == 0:
                self.next_board = move
                return
            self.next_board = -1
            return
        else:
            return

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

    def check_draw(self):
        return super(BigBoard, self).check_draw()

    # these are functions needed for MCTS

    def get_legal_actions(self):
        """
        Constructs a list of all
        possible actions from current state.
        Returns a list of moves in the form (big, small).
        """
        _, big, _ = self.prev_move
        if big != -1 and self.boards[big].won == 0:
            result = []
            for i in range(9):
                if self.boards[big].board_status[i] == 0:
                    result.append((big, i))
            return result
        else:
            result = []
            for i in range(9):
                if self.boards[i].won == 0:
                    for j in range(9):
                        if self.boards[i].board_status[j] == 0:
                            result.append((i, j))
            return result

    def is_game_over(self):
        """
        Returns true if the game is over, false otherwise.
        """
        return self.check_won() or self.check_draw()

    def game_result(self, player):
        """
        Returns 1 or 0 or -1 depending
        on state corresponding to win,
        tie or a loss.
        """
        if self.check_draw():
            return 0
        elif self.check_won():
            # if the winner is whoever went last
            if self.won == player:
                return 1
            else:
                return -1
        assert False

    def move_MTCS(self, player, move):
        """
        Returns new state after 'move' has been made by 'player'
        """
        self.play_turn(player, move)
        return self

    def __str__(self):
        return str(self.board_status)
