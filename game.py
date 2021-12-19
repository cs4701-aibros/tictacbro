from board import BigBoard
from board import Board
from monte_carlo import MCTSNode
import random
import copy

"""
Put functions for making AI moves up here
"""
def random_move(game_board):
    actions_list = game_board.get_legal_actions()
    index = random.randint(0, len(actions_list) - 1)
    action = actions_list[index]
    return action


def monte_carlo_move(game_board, player):
    # copy game board so MC can do it's game tree search on it without affecting actual board
    game_board2 = copy.deepcopy(game_board)
    root = MCTSNode(state=game_board2, player_number=player, origin=player)
    root.want_to_win = player
    mcts_move = root.best_action()
    return mcts_move


"""Initializes an ultimate tic-tac-toe board"""


def create_board():
    subboards = [Board() for i in range(9)]
    curr_board = BigBoard(subboards)
    return curr_board


"""
Makes a given move, tuple of the form (board, space), on board curr_board as player
"""


def take_turn(curr_board, player, move):
    if curr_board.is_legal(move):
        next_mov = curr_board.make_move(player, move)
        if curr_board.check_won():
            # Game ends
            return (True, None)
        # Next player has to go in a set subboard
        return (True, next_mov)
    # Move was not legal
    return (False, None)


"""Basic text-based visualization for the board"""


def visualize_board(curr_board):
    line_len = 0
    for big_row in range(0, 7, 3):
        for small_row in range(0, 7, 3):
            to_print = "{} | {} | {} || {} | {} | {} || {} | {} | {}".format(
                curr_board.boards[big_row].board_status[small_row],
                curr_board.boards[big_row].board_status[small_row + 1],
                curr_board.boards[big_row].board_status[small_row + 2],
                curr_board.boards[big_row + 1].board_status[small_row],
                curr_board.boards[big_row + 1].board_status[small_row + 1],
                curr_board.boards[big_row + 1].board_status[small_row + 2],
                curr_board.boards[big_row + 2].board_status[small_row],
                curr_board.boards[big_row + 2].board_status[small_row + 1],
                curr_board.boards[big_row + 2].board_status[small_row + 2],
            )
            line_len = len(to_print)
            print(to_print)
        if big_row != 6:
            print("=" * line_len)


"""
An example of a loop that would create a fully working ultimate tic-tac-toe game

*Important to note that the handling of which subboard is next is done here, not 
in the backend*
"""


def sample_game(p2_type=""):
    t_board = create_board()
    turn = 1
    subboard = -1
    choosing_board = False
    while t_board.won == 0:
        # Interface stuff starts here
        # (in other words, for a nicer look we would change this)
        # now makes you choose a new board if the other board is won or a draw
        if turn == 1 or p2_type not in ["random", "mcts", "minimax", "neural"]:
            visualize_board(t_board)
            if subboard == -1 or t_board.boards[subboard].won != 0:
                choosing_board = True
                subboard = input(
                    "Enter a number from 0-8 to select the board (where 0 is the top left, 1 is the top middle, and 8 is the bottom right): "
                )
            move = input(
                "Enter a number from 0-8 to select the square (where 0 is the top left, 1 is the top middle, and 8 is the bottom right): "
            )
            # Handle anything other than a number by setting it to an invalid number
            try:
                subboard = int(subboard)
            except ValueError:
                subboard = -1

            try:
                move = int(move)
            except ValueError:
                move = -1
        # Interface stuff ends here
        elif p2_type == "random":
            subboard, move = random_move(t_board)
        elif p2_type == "mcts":
            subboard, move = monte_carlo_move(t_board, 2)
        elif p2_type == "minimax":
            raise NotImplementedError
        elif p2_type == "neural":
            raise NotImplementedError
    
        valid, new_subboard = take_turn(t_board, turn, (subboard, move))
        if valid:
            # Handling of which subboard is next happens here
            if new_subboard or new_subboard == 0:
                subboard = new_subboard
                if turn == 1:
                    turn = 2
                else:
                    turn = 1
            else:
                print(valid, new_subboard)
                # Game should end here
                break
        else:
            if choosing_board:
                subboard = -1
            print("That move is invalid")
    print("The winner is {}".format(t_board.won))

def demo():
    p2_type = input("Enter who you want to play against ('mcts' for Monte Carlo player, 'random' for random player, 'minimax' for minimax player, 'neural' for adversarial neural network player, or anything else for a normal 2-player game):")
    sample_game(p2_type)

if __name__ == "__main__":
    demo()
