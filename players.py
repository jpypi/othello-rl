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

        made_move = False

        # epsilon greedy
        if np.random.random() < self.epsilon:
            # Pick random move
            while not made_move:
                pos = np.random.randint(0,8), np.random.randint(0,8)
                made_move = place_func(*pos)
        else:
            print("NN playing!")
            # Sort the possible moves lowest to highest desire
            positions = [(v,i) for i,v in enumerate(out)]
            positions.sort(key = lambda x: x[0], reverse = True)
            #scalar_play_point = np.argmax(out)

            print(positions)
            while not made_move:
                # Grab next desired move point
                scalar_play_point = positions.pop()[1]
                # Convert the scalar to a 2D coordinate to play on the board
                pos = scalar_play_point // 8, scalar_play_point % 8
                made_move = place_func(*pos)

    def updateWeights(self):
        pass
