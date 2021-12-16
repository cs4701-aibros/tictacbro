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

"""
Simulates num_games games of p1 vs. p2 and outputs win/draw percentages.
p1_type and p2_type (for now) are either "Random" for random player or "MCTS" for 
Monte Carlo player.
"""
def simulate(num_games, p1_type, p2_type):
    p1_win_count = 0
    p2_win_count = 0
    error_count = 0
    draw_count = 0

    # need try except block because some runs of montecarlo give a random value error
    # other than that, (in the games where montecarlo works) it wins about 96% 
    # and ties 4% of the time
    i = 0
    while i < num_games + error_count:
        i += 1
        game_board = create_board()
        try:
            while not game_board.is_game_over():
                #p1 move
                if p1_type == "Random":
                    make_random_move(player_number = 1, game_board = game_board)
                else:
                    make_monte_carlo_move(game_board)

                #p2 move
                if p2_type == "Random":
                    make_random_move(player_number = 2, game_board = game_board)
                else:
                    make_monte_carlo_move(game_board)
                
            if game_board.won == 2:
                p2_win_count += 1
            elif game_board.won == -1:
                draw_count += 1
            else:
                p1_win_count += 1
        except:
            error_count += 1
    
    print("="*50)
    print(p1_type + " vs. " + p2_type + " Win Pcts")
    print("Games Played: ", num_games)
    print("P1 (" + p1_type + ") Win %: ", p1_win_count/num_games)
    print("P2 (" + p2_type + ") Win %: ", p2_win_count/num_games)
    print("Draw %: ", draw_count/num_games)
    print("="*50)



if __name__ == "__main__":
  simulate(num_games = 50, p1_type = "Random", p2_type="MCTS")