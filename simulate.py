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

def make_monte_carlo_move(game_board):
    game_board2 = copy.deepcopy(game_board)
    root = MCTSNode(state = game_board2)
    mcts_move = root.best_action().parent_action
    game_board.move(mcts_move)

# how many games to run
num_games = 100

# need try except block because some runs of montecarlo give a random value error
# other than that, (in the games where montecarlo works) it wins about 96% 
# and ties 4% of the time
def simulate():
    mc_win_count = 0
    random_win_count = 0
    error_count = 0
    draw_count = 0

    i = 0
    while i < num_games + error_count:
        i += 1
        game_board = create_board()
        try:
            while not game_board.is_game_over():
                # alternate between random move and monte carlo move
                make_random_move(1, game_board)
                make_monte_carlo_move(game_board)
            if game_board.won == 2:
                mc_win_count += 1
            elif game_board.won == -1:
                draw_count += 1
            else:
                random_win_count += 1
        except:
            error_count += 1
        
    print("MCTS Win Number: ", mc_win_count)
    print("Random Win Number: ", random_win_count)
    print("Tie Game Number: ", draw_count)


if __name__ == "__main__":
  simulate()