import itertools
import random

import numpy as np

import nn


class RLPlayer:
    def __init__(self, q_lr, discount_factor, net_lr = 0.01):
        # We ougth to use softmax in this
        self.policy_net = nn.NN([64, 128, 128, 64, 64], net_lr)
        # This ought to decay
        self.epsilon = 0.6

        # Variables for Q learning discount reward
        self.q_lr = q_lr
        self.discount_factor = discount_factor

        self.prepForNewGame()

    def prepForNewGame(self):
        self.play_history = []
        self.wins = 0

    def play(self, place_func, board_state, me, log_history = True):
        # Transform all of "this player's" tokens to 1s and the other player's
        # to -1s
        input_state = np.apply_along_axis(lambda x: int((x==me and 1) or (x!=0 and -1)),
                                          1, board_state.reshape((64, 1))).reshape((64,1))
        made_move = False
        pos = None

        # epsilon greedy to pick random move
        if np.random.random() < self.epsilon:
            positions = list(itertools.product(range(8), repeat = 2))
            random.shuffle(positions)
            while not made_move and positions:
                pos = positions.pop()
                made_move = place_func(*pos)

            # If we can make no move... pass
            if not made_move and not positions:
                return False

        else:
            out = self.policy_net.getOutput(input_state)
            # Sort the possible moves lowest to highest desire
            positions = [(v,i) for i,v in enumerate(out)]
            positions.sort(key = lambda x: x[0], reverse = True)
            #scalar_play_point = np.argmax(out)

            #print(positions)
            while not made_move and positions:
                # Grab next desired move point
                scalar_play_point = positions.pop()[1]
                # Convert the scalar to a 2D coordinate to play on the board
                pos = scalar_play_point // 8, scalar_play_point % 8
                made_move = place_func(*pos)

            # If we can make no move... pass
            if not made_move and not positions:
                return False

        if log_history:
            self.play_history.append((np.copy(input_state), pos[0]*8 + pos[1]))

        return True

    def updateWeights(self, final_score):
        #for i, (state, action) in enumerate(self.play_history):
        #    self.policy_net.backProp(state, final_score * OneHot(action, 64))

        i = 0
        state, action = self.play_history[i]
        q = self.policy_net.getOutput(state)
        targets = []
        while i+1 < len(self.play_history):
            i += 1
            state_, action_ = self.play_history[i]
            q_ = self.policy_net.getOutput(state_)

            r = final_score if i+1 == len(self.play_history) else 0
            target = np.zeros(64)
            target[action] = q[action] + self.q_lr * (r + self.discount_factor * np.max(q_) - q[action])
            targets.append(target)
            action, q = action_, q_

        target = np.zeros(64)
        target[self.play_history[-1][1]] = final_score
        targets.append(target)

        for i in range(len(play_history)-1, -1, -1)
            t = self.policy_net.mkVec(targets[i])
            self.policy_net.backProp(state, t)


def OneHot(index, dim):
    """
    Converts an index into a one-hot encoded column vector.
    """
    a = np.zeros((dim,1))
    a[index] = 1
    return a

