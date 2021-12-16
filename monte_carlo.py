from game import create_board
import numpy as np
from collections import defaultdict
from board import BigBoard
from board import Board
from game import *

class MCTSNode():
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
    child_node = MCTSNode(
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


  def best_child(self, c_param=0.5):
    
    choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
    # can't figure out why self.children is empty sometimes
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

    return self.best_child(c_param=0.5)

def main():
  initial_state = create_board()
  root = MCTSNode(state = initial_state)
  result = root.best_action()
  # visualize_board(result.state)
  # print("board_status: ", result.state.board_status)
  # print("won: ", result.state.won)
  # print("current: ", result.player_number)
  # print("parent_action: ", result.parent_action)
  # print("untried_actions: ", result._untried_actions)
  return result

if __name__ == "__main__":
  main()