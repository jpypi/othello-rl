import numpy as np

import nn


class RLPlayer:
    def __init__(self):
        # We ougth to softmax this
        self.policy_net = nn.NN([64, 128, 64], 0.02)
        self.play_history = []

        # We should anneal this
        self.epsilon = 0.8

    def play(self, place_func, board_state):
        input_state = board_state.reshape((64, 1))
        out = self.policy_net.getOutput(input_state)

        # epsilon greedy
        if True: #np.random.random() < self.epsilon:
            # Pick random move
            made_move = False
            while not made_move:
                pos = np.random.randint(0,8), np.random.randint(0,8)
                made_move = place_func(*pos)
        else:
            # Pick best move from
            pass

    def updateWeights(self):
        pass
