import numpy as np


class MCTSNode:
    """
    Code for this algorithm inspired by the tutorial given on:
    https://ai-boson.github.io/mcts/
    (Link also listed as a reference in our written report.)
    """

    def __init__(self, state, player_number, origin, parent=None, parent_action=None):
        self.state = state
        # Expects to be updated when first created
        self.want_to_win = origin
        self.player_number = player_number
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self.actions = self.state.get_legal_actions()
        self.wins = 0
        self.losses = 0
        self.num_sims = 0

    def expand(self):
        action = self.actions.pop()
        next_state = self.state.move_MTCS(self.player_number, action)
        player = 0
        if self.player_number == 1:
            player = 2
        else:
            player = 1
        child = MCTSNode(
            next_state, player, self.want_to_win, parent=self, parent_action=action
        )
        self.children.append(child)
        return child

    def rollout(self):
        while not self.state.is_game_over():
            possible_moves = self.state.get_legal_actions()
            action = self.choose_move(possible_moves)
            self.state = self.state.move_MTCS(self.player_number, action)
        return self.state.game_result(self.player_number)

    def backpropagate(self, result):
        self.num_sims += 1.0
        if result == 1:
            self.wins += 1
        elif result == -1:
            self.losses += 1
        if self.parent:
            self.parent.backpropagate(result)

    def UCT(self, N, c, good):
        UCT = good * (self.wins - self.losses / self.num_sims) + c * np.sqrt(
            (2 * np.log(N) / self.num_sims)
        )
        return UCT

    def best_child(self, c=1.4):
        good = 1 if self.player_number == self.want_to_win else -1
        # multiply weights by -1 if it isn't the player we want to win
        weights = [child.UCT(self.num_sims, c, good) for child in self.children]
        return self.children[np.argmax(weights)]

    def choose_move(self, possible_moves):
        # currently random
        return possible_moves[np.random.randint(len(possible_moves))]

    def simulate(self):
        curr_node = self
        while not curr_node.state.is_game_over():
            if not len(self.actions) == 0:
                return curr_node.expand()
            else:
                curr_node = curr_node.best_child()
        return curr_node

    def best_action(self):
        assert self.want_to_win != 0
        simulations = 100
        for i in range(simulations):
            v = self.simulate()
            reward = v.rollout()
            v.backpropagate(reward)
        return self.best_child(c=0.0).parent_action
