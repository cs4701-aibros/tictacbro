from game import create_board
import numpy as np
from collections import defaultdict
from board import BigBoard
from board import Board

class MonteCarloTreeSearchNode():
  """
  Code for this algorithm greatly inspired by the tutorial given on:
  https://ai-boson.github.io/mcts/ 
  (Link also listed as a reference in our written report.)
  """
  def __init__(self, state, player_number=2, parent=None, parent_action=None):
    self.state = state
    self.player_number = player_number
    self.parent = parent
    self.parent_action = parent_action
    self.children = []
    self._number_of_visits = 0
    self._results = defaultdict(int)
    self._results[1] = 0
    self._results[-1] = 0
    self._untried_actions = None
    self._untried_actions = self.untried_actions()
    return

  def untried_actions(self):
    self._untried_actions = self.state.get_legal_actions()
    return self._untried_actions

  def q(self):
    wins = self._results[1]
    loses = self._results[-1]
    return wins - loses

  def n(self):
    return self._number_of_visits

  def expand(self):

    action = self._untried_actions.pop()
    next_state = self.state.move(action)
    child_node = MonteCarloTreeSearchNode(
    next_state, parent=self, parent_action=action)

    self.children.append(child_node)
    return child_node     

  def is_terminal_node(self):
    return self.state.is_game_over()

  def rollout(self):
    current_rollout_state = self.state
    
    while not current_rollout_state.is_game_over():
        
      possible_moves = current_rollout_state.get_legal_actions()
        
      action = self.rollout_policy(possible_moves)
      current_rollout_state = current_rollout_state.move(action)
    return current_rollout_state.game_result()

  def backpropagate(self, result):
    self._number_of_visits += 1.
    self._results[result] += 1.
    if self.parent:
      self.parent.backpropagate(result)

  def is_fully_expanded(self):
    return len(self._untried_actions) == 0


  def best_child(self, c_param=0.1):
    
    choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
    return self.children[np.argmax(choices_weights)]

  def rollout_policy(self, possible_moves):
    
    return possible_moves[np.random.randint(len(possible_moves))]

  def tree_policy(self):

    current_node = self
    while not current_node.is_terminal_node():
        
      if not current_node.is_fully_expanded():
        return current_node.expand()
      else:
        current_node = current_node.best_child()
    return current_node

  def best_action(self):
    simulation_no = 100
    for i in range(simulation_no):
    
      v = self.tree_policy()
      reward = v.rollout()
      v.backpropagate(reward)

    return self.best_child(c_param=0.)

  # def get_legal_actions(self): 
  #   """
  #   Constructs a list of all
  #   possible actions from current state.
  #   Returns a list of moves in the form (big, small).
  #   """
  #   curr_board = self.state.curr_board
  #   _, big = curr_board.prev_move
  #   if big != -1 and curr_board.boards[big].won == 0:
  #     result = []
  #     for i in range(9):
  #       if curr_board.boards[big].board_status[i] == 0:
  #         result.append((big, i))
  #     return result
  #   else: 
  #     result = []
  #     for i in range(9):
  #       if curr_board.boards[i].won == 0:
  #         for j in range(9):
  #             if curr_board.boards[i].board_status[j] == 0:
  #               result.append((i, j))
  #     return result

  # def is_game_over(self):
  #   """
  #   Returns true if the game is over, false otherwise.
  #   """
  #   curr_board = self.state.curr_board
  #   return curr_board.check_won() or curr_board.check_draw()

  # def game_result(self):
  #   """
  #   Returns 1 or 0 or -1 depending
  #   on your state corresponding to win,
  #   tie or a loss.
  #   """
  #   curr_board = self.state.curr_board
  #   if curr_board.check_draw():
  #     return 0
  #   elif curr_board.check_won():
  #     if curr_board.won == self.player_number:
  #       return 1
  #     else:
  #       return -1
  #   return 0

  # def move(self,action):
  #   """
  #   Returns the new state after making a move.
  #   """
  #   curr_board = self.state.curr_board
  #   curr_board.make_move(self.player_number, action)
  #   return self.state.curr_board

def create_board():
    subboards = [Board() for i in range(9)]
    curr_board = BigBoard(subboards)
    return curr_board

def main():
  initial_state = create_board()
  root = MonteCarloTreeSearchNode(state = initial_state)
  result = root.best_action()
  print(result)

if __name__ == "__main__":
  main()