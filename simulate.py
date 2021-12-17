from board import BigBoard
from board import Board
from game import *
from monte_carlo import MCTSNode
import random
import copy

"""
Just so I can put a random player vs. Monte Carlo Player and compare
win percentages.
"""


def make_random_move(player_number, game_board):
    actions_list = game_board.get_legal_actions()
    index = random.randint(0, len(actions_list) - 1)
    action = actions_list[index]
    game_board.make_move(player_number, action)


def monte_carlo_move(game_board, player):
    # copy game board so MC can do it's game tree search on it without affecting actual board
    game_board2 = copy.deepcopy(game_board)
    root = MCTSNode(state=game_board2, player_number=player, origin=player)
    root.want_to_win = player
    mcts_move = root.best_action()
    return mcts_move


"""
Simulates num_games games of p1 vs. p2 and outputs win/draw percentages.
p1_type and p2_type (for now) are either "Random" for random player or "MCTS" for 
Monte Carlo player.
"""


def simulate(num_games, p1_type, p2_type):
    p1_win_count = 0
    p2_win_count = 0
    draw_count = 0

    # need try except block because some runs of montecarlo give a value error
    # due to self.children being empty in the one case I can't figure out
    # other than that, (in the games where montecarlo works) it wins about 96%
    # and ties 4% of the time
    i = 0
    while i < num_games:
        i += 1
        game_board = create_board()
        turn = 1
        while not game_board.is_game_over():
            # p1 move
            if turn == 1:
                if p1_type == "Random":
                    make_random_move(player_number=1, game_board=game_board)
                else:
                    action = monte_carlo_move(game_board, 1)
                    game_board.make_move(1, action)
                turn = 2
            # p2 move
            else:
                if p2_type == "Random":
                    make_random_move(player_number=2, game_board=game_board)
                else:
                    action = monte_carlo_move(game_board, 2)
                    game_board.make_move(2, action)
                turn = 1

        if game_board.won == 2:
            p2_win_count += 1
        elif game_board.won == -1:
            draw_count += 1
        else:
            p1_win_count += 1

    print("=" * 50)
    print(p1_type + " vs. " + p2_type + " Win Pcts")
    print("Games Played: ", num_games)
    print("P1 (" + p1_type + ") Win %: ", p1_win_count / num_games)
    print("P2 (" + p2_type + ") Win %: ", p2_win_count / num_games)
    print("Draw %: ", draw_count / num_games)
    print("=" * 50)


if __name__ == "__main__":
    simulate(num_games=1000, p1_type="MCTS", p2_type="Random")
