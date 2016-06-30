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

        # Variables for Q learning
        self.q_lr = q_lr
        self.discount_factor = discount_factor
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
        i = 0
        state, action = self.play_history[i]
        q = self.policy_net.getOutput(state)
        n_play_history = len(self.play_history)
        while i < n_play_history:
            i += 1

            # Last state-action is win/lose which should just be the final score
            if i == n_play_history:
                #q[action] += self.q_lr * (final_score - q[action])
                q[action] = final_score

            else:
                state_, action_ = self.play_history[i]
                q_ = self.policy_net.getOutput(state_)
                #q[action] += self.q_lr * (self.discount_factor * np.max(q_) - q[action])
                q[action] += self.discount_factor * np.max(q_)

            self.policy_net.backProp(state, self.policy_net.mkVec(q))

            if i != n_play_history:
                action, q = action_, q_

#        print(len(self.play_history))
#        for i in range(len(self.play_history)-1, -1, -1):
#            print(i)
#            t = self.policy_net.mkVec(targets[i])
#            self.policy_net.backProp(state, t)


class HumanPlayer:
    def play(self, place_func, board_state, me, _):
        try:
            pos = map(int, map(str.strip, input().split(" ")))
            place_func(*pos)
            return True
        except ValueError:
            return False


def OneHot(index, dim):
    """
    Converts an index into a one-hot encoded column vector.
    """
    a = np.zeros((dim,1))
    a[index] = 1
    return a

