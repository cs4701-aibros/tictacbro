import warnings

import numpy as np
from gym import spaces

from pettingzoo import AECEnv
from pettingzoo.utils import agent_selector, wrappers

from .board import BigBoard


def env():
    env = raw_env()
    env = wrappers.CaptureStdoutWrapper(env)
    env = wrappers.TerminateIllegalWrapper(env, illegal_reward=-1)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    env.reward_range = (-float("inf"), float("inf"))
    return env


class raw_env(AECEnv):
    metadata = {
        "render.modes": ["human"],
        "name": "ultimate_tictactoe_v1",
        "is_parallelizable": False,
    }

    def __init__(self):
        super().__init__()
        self.board = BigBoard()

        self.agents = ["player_1", "player_2"]
        self.possible_agents = self.agents[:]

        self.action_spaces = {i: spaces.Discrete(81) for i in self.agents}
        self.observation_spaces = {
            i: spaces.Dict(
                {
                    "observation": spaces.Box(
                        low=0, high=1, shape=(9, 9, 2), dtype=np.int8
                    ),
                    "action_mask": spaces.Box(
                        low=0, high=1, shape=(81,), dtype=np.int8
                    ),
                }
            )
            for i in self.agents
        }

        self.rewards = {i: 0 for i in self.agents}
        self.dones = {i: False for i in self.agents}
        self.infos = {
            i: {"legal_moves": [(i, j) for i in range(9) for j in range(9)]}
            for i in self.agents
        }

        self._agent_selector = agent_selector(self.agents)
        self.agent_selection = self._agent_selector.reset()

    def observe(self, agent):
        board_vals = np.array([subboard.board_status for subboard in self.board.boards])
        cur_player = self.possible_agents.index(agent)
        opp_player = (cur_player + 1) % 2

        cur_p_board = np.equal(board_vals, cur_player + 1)
        opp_p_board = np.equal(board_vals, opp_player + 1)

        observation = np.dstack([cur_p_board, opp_p_board]).astype(np.int8)
        legal_moves = self._legal_moves() if agent == self.agent_selection else []

        action_mask = np.zeros(81, "int8")
        for i in legal_moves:
            action_mask[i] = 1

        return {"observation": observation, "action_mask": action_mask}

    def observation_space(self, agent):
        return self.observation_spaces[agent]

    def action_space(self, agent):
        return self.action_spaces[agent]

    def _legal_moves(self):
        big = self.board.next_board
        if big != -1 and self.board.boards[big].won == 0:
            result = []
            for i in range(9):
                if self.board.boards[big].board_status[i] == 0:
                    result.append(big * 9 + i)
            return result
        else:
            result = []
            for i in range(9):
                if self.board.boards[i].won == 0:
                    for j in range(9):
                        if self.board.boards[i].board_status[j] == 0:
                            result.append(i * 9 + j)
            return result

    def step(self, action):
        if self.dones[self.agent_selection]:
            return self._was_done_step(action)
        action = (action // 9, action % 9)
        assert self.board.is_legal(action), "played illegal move"
        self.board.play_turn(self.agents.index(self.agent_selection) + 1, action)

        next_agent = self._agent_selector.next()

        if self.board.is_game_over():
            winner = self.board.won

            if winner == -1:
                pass
            elif winner == 1:
                self.rewards[self.agents[0]] += 1
                self.rewards[self.agents[1]] -= 1
            else:
                self.rewards[self.agents[1]] += 1
                self.rewards[self.agents[0]] -= 1

            self.dones = {i: True for i in self.agents}
        self._cumulative_rewards[self.agent_selection] = 0
        self.agent_selection = next_agent

        self._accumulate_rewards()

    def reset(self):
        self.board = BigBoard()

        self.agents = self.possible_agents[:]
        self.rewards = {i: 0 for i in self.agents}
        self._cumulative_rewards = {i: 0 for i in self.agents}
        self.dones = {i: False for i in self.agents}
        self.infos = {i: {} for i in self.agents}
        self._agent_selector.reinit(self.agents)
        self._agent_selector.reset()
        self.agent_selection = self._agent_selector.reset()

    def render(self, mode="human"):
        def get_symbol(input):
            if input == 0:
                return "-"
            elif input == 1:
                return "X"
            else:
                return "O"

        board = np.array(
            [subboard.board_status for subboard in self.board.boards]
        ).flatten()
        board = list(map(get_symbol, board))

        print(
            " " * 5
            + "|"
            + " " * 5
            + "|"
            + " " * 5
            + "||"
            + " " * 5
            + "|"
            + " " * 5
            + "|"
            + " " * 5
            + "||"
            + " " * 5
            + "|"
            + " " * 5
            + "|"
            + " " * 5
        )
        print(
            f"  {board[0]}  "
            + "|"
            + f"  {board[1]}  "
            + "|"
            + f"  {board[2]}  "
            + "||"
            + f"  {board[9]}  "
            + "|"
            + f"  {board[10]}  "
            + "|"
            + f"  {board[11]}  "
            + "||"
            + f"  {board[18]}  "
            + "|"
            + f"  {board[19]}  "
            + "|"
            + f"  {board[20]}  "
        )
        print(
            "_" * 5
            + "|"
            + "_" * 5
            + "|"
            + "_" * 5
            + "||"
            + "_" * 5
            + "|"
            + "_" * 5
            + "|"
            + "_" * 5
            + "||"
            + "_" * 5
            + "|"
            + "_" * 5
            + "|"
            + "_" * 5
        )

        print(
            " " * 5
            + "|"
            + " " * 5
            + "|"
            + " " * 5
            + "||"
            + " " * 5
            + "|"
            + " " * 5
            + "|"
            + " " * 5
            + "||"
            + " " * 5
            + "|"
            + " " * 5
            + "|"
            + " " * 5
        )
        print(
            f"  {board[3]}  "
            + "|"
            + f"  {board[4]}  "
            + "|"
            + f"  {board[5]}  "
            + "||"
            + f"  {board[12]}  "
            + "|"
            + f"  {board[13]}  "
            + "|"
            + f"  {board[14]}  "
            + "||"
            + f"  {board[21]}  "
            + "|"
            + f"  {board[22]}  "
            + "|"
            + f"  {board[23]}  "
        )
        print(
            "_" * 5
            + "|"
            + "_" * 5
            + "|"
            + "_" * 5
            + "||"
            + "_" * 5
            + "|"
            + "_" * 5
            + "|"
            + "_" * 5
            + "||"
            + "_" * 5
            + "|"
            + "_" * 5
            + "|"
            + "_" * 5
        )

        print(
            " " * 5
            + "|"
            + " " * 5
            + "|"
            + " " * 5
            + "||"
            + " " * 5
            + "|"
            + " " * 5
            + "|"
            + " " * 5
            + "||"
            + " " * 5
            + "|"
            + " " * 5
            + "|"
            + " " * 5
        )
        print(
            f"  {board[6]}  "
            + "|"
            + f"  {board[7]}  "
            + "|"
            + f"  {board[8]}  "
            + "||"
            + f"  {board[15]}  "
            + "|"
            + f"  {board[16]}  "
            + "|"
            + f"  {board[17]}  "
            + "||"
            + f"  {board[24]}  "
            + "|"
            + f"  {board[25]}  "
            + "|"
            + f"  {board[26]}  "
        )
        print(
            "=" * 5
            + "|"
            + "=" * 5
            + "|"
            + "=" * 5
            + "||"
            + "=" * 5
            + "|"
            + "=" * 5
            + "|"
            + "=" * 5
            + "||"
            + "=" * 5
            + "|"
            + "=" * 5
            + "|"
            + "=" * 5
        )

        print(
            " " * 5
            + "|"
            + " " * 5
            + "|"
            + " " * 5
            + "||"
            + " " * 5
            + "|"
            + " " * 5
            + "|"
            + " " * 5
            + "||"
            + " " * 5
            + "|"
            + " " * 5
            + "|"
            + " " * 5
        )
        print(
            f"  {board[27]}  "
            + "|"
            + f"  {board[28]}  "
            + "|"
            + f"  {board[29]}  "
            + "||"
            + f"  {board[36]}  "
            + "|"
            + f"  {board[37]}  "
            + "|"
            + f"  {board[38]}  "
            + "||"
            + f"  {board[45]}  "
            + "|"
            + f"  {board[46]}  "
            + "|"
            + f"  {board[47]}  "
        )
        print(
            "_" * 5
            + "|"
            + "_" * 5
            + "|"
            + "_" * 5
            + "||"
            + "_" * 5
            + "|"
            + "_" * 5
            + "|"
            + "_" * 5
            + "||"
            + "_" * 5
            + "|"
            + "_" * 5
            + "|"
            + "_" * 5
        )

        print(
            " " * 5
            + "|"
            + " " * 5
            + "|"
            + " " * 5
            + "||"
            + " " * 5
            + "|"
            + " " * 5
            + "|"
            + " " * 5
            + "||"
            + " " * 5
            + "|"
            + " " * 5
            + "|"
            + " " * 5
        )
        print(
            f"  {board[30]}  "
            + "|"
            + f"  {board[31]}  "
            + "|"
            + f"  {board[32]}  "
            + "||"
            + f"  {board[39]}  "
            + "|"
            + f"  {board[40]}  "
            + "|"
            + f"  {board[41]}  "
            + "||"
            + f"  {board[48]}  "
            + "|"
            + f"  {board[49]}  "
            + "|"
            + f"  {board[50]}  "
        )
        print(
            "_" * 5
            + "|"
            + "_" * 5
            + "|"
            + "_" * 5
            + "||"
            + "_" * 5
            + "|"
            + "_" * 5
            + "|"
            + "_" * 5
            + "||"
            + "_" * 5
            + "|"
            + "_" * 5
            + "|"
            + "_" * 5
        )

        print(
            " " * 5
            + "|"
            + " " * 5
            + "|"
            + " " * 5
            + "||"
            + " " * 5
            + "|"
            + " " * 5
            + "|"
            + " " * 5
            + "||"
            + " " * 5
            + "|"
            + " " * 5
            + "|"
            + " " * 5
        )
        print(
            f"  {board[33]}  "
            + "|"
            + f"  {board[34]}  "
            + "|"
            + f"  {board[35]}  "
            + "||"
            + f"  {board[42]}  "
            + "|"
            + f"  {board[43]}  "
            + "|"
            + f"  {board[44]}  "
            + "||"
            + f"  {board[51]}  "
            + "|"
            + f"  {board[52]}  "
            + "|"
            + f"  {board[53]}  "
        )
        print(
            "=" * 5
            + "|"
            + "=" * 5
            + "|"
            + "=" * 5
            + "||"
            + "=" * 5
            + "|"
            + "=" * 5
            + "|"
            + "=" * 5
            + "||"
            + "=" * 5
            + "|"
            + "=" * 5
            + "|"
            + "=" * 5
        )

        print(
            " " * 5
            + "|"
            + " " * 5
            + "|"
            + " " * 5
            + "||"
            + " " * 5
            + "|"
            + " " * 5
            + "|"
            + " " * 5
            + "||"
            + " " * 5
            + "|"
            + " " * 5
            + "|"
            + " " * 5
        )
        print(
            f"  {board[54]}  "
            + "|"
            + f"  {board[55]}  "
            + "|"
            + f"  {board[56]}  "
            + "||"
            + f"  {board[63]}  "
            + "|"
            + f"  {board[64]}  "
            + "|"
            + f"  {board[65]}  "
            + "||"
            + f"  {board[72]}  "
            + "|"
            + f"  {board[73]}  "
            + "|"
            + f"  {board[74]}  "
        )
        print(
            "_" * 5
            + "|"
            + "_" * 5
            + "|"
            + "_" * 5
            + "||"
            + "_" * 5
            + "|"
            + "_" * 5
            + "|"
            + "_" * 5
            + "||"
            + "_" * 5
            + "|"
            + "_" * 5
            + "|"
            + "_" * 5
        )

        print(
            " " * 5
            + "|"
            + " " * 5
            + "|"
            + " " * 5
            + "||"
            + " " * 5
            + "|"
            + " " * 5
            + "|"
            + " " * 5
            + "||"
            + " " * 5
            + "|"
            + " " * 5
            + "|"
            + " " * 5
        )
        print(
            f"  {board[57]}  "
            + "|"
            + f"  {board[58]}  "
            + "|"
            + f"  {board[59]}  "
            + "||"
            + f"  {board[66]}  "
            + "|"
            + f"  {board[67]}  "
            + "|"
            + f"  {board[68]}  "
            + "||"
            + f"  {board[75]}  "
            + "|"
            + f"  {board[76]}  "
            + "|"
            + f"  {board[77]}  "
        )
        print(
            "_" * 5
            + "|"
            + "_" * 5
            + "|"
            + "_" * 5
            + "||"
            + "_" * 5
            + "|"
            + "_" * 5
            + "|"
            + "_" * 5
            + "||"
            + "_" * 5
            + "|"
            + "_" * 5
            + "|"
            + "_" * 5
        )

        print(
            " " * 5
            + "|"
            + " " * 5
            + "|"
            + " " * 5
            + "||"
            + " " * 5
            + "|"
            + " " * 5
            + "|"
            + " " * 5
            + "||"
            + " " * 5
            + "|"
            + " " * 5
            + "|"
            + " " * 5
        )
        print(
            f"  {board[60]}  "
            + "|"
            + f"  {board[61]}  "
            + "|"
            + f"  {board[62]}  "
            + "||"
            + f"  {board[69]}  "
            + "|"
            + f"  {board[70]}  "
            + "|"
            + f"  {board[71]}  "
            + "||"
            + f"  {board[78]}  "
            + "|"
            + f"  {board[79]}  "
            + "|"
            + f"  {board[80]}  "
        )
        print(
            " " * 5
            + "|"
            + " " * 5
            + "|"
            + " " * 5
            + "||"
            + " " * 5
            + "|"
            + " " * 5
            + "|"
            + " " * 5
            + "||"
            + " " * 5
            + "|"
            + " " * 5
            + "|"
            + " " * 5
        )

    def close(self):
        pass
