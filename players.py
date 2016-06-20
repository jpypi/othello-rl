import itertools
import random

import numpy as np

import nn


class RLPlayer:
    def __init__(self):
        # We ougth to softmax this
        self.policy_net = nn.NN([64, 128, 64], 0.02)
        self.play_history = []

        # This ought to decay
        self.epsilon = 0.8

    def play(self, place_func, board_state, me):
        input_state = board_state.reshape((64, 1))
        out = self.policy_net.getOutput(input_state)

        made_move = False
        pos = None

        # epsilon greedy to pick random move
        if np.random.random() < self.epsilon:
            positions = list(itertools.product(range(8), repeat = 2))
            random.shuffle(positions)
            while not made_move:
                pos = positions.pop()
                made_move = place_func(*pos)
        else:
            print("NN playing!")
            # Sort the possible moves lowest to highest desire
            positions = [(v,i) for i,v in enumerate(out)]
            positions.sort(key = lambda x: x[0], reverse = True)
            #scalar_play_point = np.argmax(out)

            #print(positions)
            while not made_move:
                # Grab next desired move point
                scalar_play_point = positions.pop()[1]
                # Convert the scalar to a 2D coordinate to play on the board
                pos = scalar_play_point // 8, scalar_play_point % 8
                made_move = place_func(*pos)

        self.play_history.append((np.copy(input_state), pos[0]*8 + pos[1]))

    def updateWeights(self, final_score):
        for i, (state, output) in enumerate(self.play_history):
            self.policy_net.backProp(state, final_score * OneHot(output, 64))


def OneHot(index, dim):
    """
    Converts an index into a one-hot encoded column vector.
    """
    a = np.zeros((dim,1))
    a[index] = 1
    return a

