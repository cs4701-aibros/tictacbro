import ultimate_tictactoe_v1
import random
import numpy as np


def p_random(observation, agent):
    action = random.choice(np.flatnonzero(observation["action_mask"]))
    return action


if __name__ == "__main__":
    env = ultimate_tictactoe_v1.env()
    env.reset()
    env.render()
    for agent in env.agent_iter():
        observation, reward, done, info = env.last()
        action = p_random(observation, agent)
        _ = input("press any key to continue")
        env.step(action)
        env.render()
