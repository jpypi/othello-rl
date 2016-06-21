import numpy as np
from math import floor
from random import random, randint
import os


replayMemory = list()


def sig(wSum):
    return 1/(1 + np.exp(-wSum))


def dSig(a):
    return a * (1 - a)


def validateActions(board, t, color, actions):
    validMoves = list()
    for a in range(actions.shape[0]):
        r = floor(a/board.size)
        c = a % board.size
        if board.isValidMove(t, color, r, c):
            validMoves.append(a)

    return validMoves


def adaptExperience(color, experience):
    if experience.color != color:
        for i in range(experience.state.shape[0]):
            experience.state[i] *= -1
        for i in range(experience.postState.shape[0]):
            experience.postState[i] *= -1
        experience.color = color
    return experience


class Experience():
    def __init__(self, color, state, action, reward, postAction):
        self.color = color  # Color of player who made the action
        self.state = state  # Board matrix flattened to a vector
        self.action = action  # Coordinates to play
        self.reward = reward  # Board control after action
        self.postState = postAction  # Board state after action


class Player():
    hSizes = [100, 100]
    explore = 1
    lr = .5
    discount = .5

    def __init__(self, board, color):
        self.color = color
        self.board = board
        # Get bounding sizes of weight matrices
        wSize = max(self.hSizes)
        if wSize < self.board.size*self.board.size:
            wSize = self.board.size*self.board.size
        self.qw = list()
        self.b = list()

        # Init weights and biases
        for i in range(len(self.hSizes)):
            self.b.append(np.ones(self.hSizes[i]))
            if i == 0:
                self.qw.append(np.random.rand(self.hSizes[i], self.board.size*self.board.size))
            else:
                self.qw.append(np.random.rand(self.hSizes[i], self.hSizes[i-1]))
        self.b.append(np.ones(self.board.size*self.board.size))
        self.qw.append(np.random.rand(self.board.size*self.board.size, self.hSizes[-1]))

    def getAction(self, state, t='live'):
        '''
        Returns x, y, r. Coordinates and estimated reward.
        '''
        # Feed state forward through network
        s = state
        wSum = list()
        self.a = list()

        # Input
        wSum.append(np.dot(self.qw[0], s) + self.b[0])
        self.a.append(sig(wSum[0]))

        for l in range(len(self.qw))[1:]:
            wSum.append(np.dot(self.qw[l], self.a[-1]) + self.b[l])
            self.a.append(sig(wSum[l]))

        # Get a list of actions the player can make that are valid
        # The actions are in the form of output indices
        # Note that the output layer is dimensionally equivalent to a flattened board matrix
        # So an action's coordinates can be found by division and the modulus operator
        validActions = validateActions(self.board, t, self.color, self.a[-1])
        if not validActions:
            print("My turn should be skipped if I have no valid actions.")
            return None
        if random() < self.explore:
            # Random choice of action
            act = validActions[randint(0, len(validActions)-1)]
        else:
            validActionActivations = list()
            # Get activations of the valid actions
            for i in range(len(validActions)):
                validActionActivations.append(self.a[-1][validActions[i]])
            aIndex = np.argmax(validActionActivations)
            act = validActions[aIndex]
        return (int(floor(act/self.board.size)), int(act%self.board.size)), self.a[-1][act]

    def train(self, experience):
        # Get target reward
        self.board.loadFromState('virtual', experience.postState)
        if self.board.isGameOver('virtual'):
            t = experience.reward
        else:
            action, reward = self.getAction(experience.postState, 'virtual')
            # board.getOwnership(self.color)
            t = experience.reward + self.discount * reward
        self.board.syncVirtualBoard()

        # Backprop using an error of (t - Q(experience.state))^2
        action, reward = self.getAction(experience.state)
        d = list()
        # Compute output deltas
        d.append((t - reward)*dSig(self.a[-1]))

        # Loop backwards through network layers to calculate all deltas
        for l in range(len(self.qw))[-2::-1]:
            # d[0] is the previously added delta
            # which is the delta for layer l+1
            d.insert(0, dSig(self.a[l]) * np.dot(self.qw[l+1].T, d[0]))

        # Modify weights and biases starting with first layer
        self.qw[0] += self.lr * np.dot(np.atleast_2d(d[0]).T, np.atleast_2d(experience.state))
        self.b[0] += self.lr * d[0]

        for l in range(len(self.qw))[1:]:
            self.qw[l] += self.lr * np.dot(np.atleast_2d(d[l]).T, np.atleast_2d(self.a[l-1]))
            self.b[l] += self.lr * d[l]

    def takeTurn(self):
        state = self.board.board.flatten()

        action, reward = self.getAction(state)

        if not action:
            print("Cannot move")
        elif not self.board.updateBoard('live', self.color, action[0], action[1]):
            print("FAILED MOVE")

            experience = Experience(self.color, state, action, reward, self.board.board.flatten())
            replayMemory.append(experience)

        # Train on experience sampled from replay memory
        if len(replayMemory) > 0:
            sampExp = adaptExperience(self.color, replayMemory[randint(0, len(replayMemory)-1)])
            self.train(sampExp)

    def saveWeights(self, filename):
        if '.npy' in filename:
            filename = filename.replace('.npy', '')
        np.save(filename, self.qw)
        np.save(filename + '_bias', self.b)
        print('Weights and biases saved.')

    def loadWeights(self, filename):
        if '.npy' in filename:
            filename = filename.replace('.npy', '')
        if os.path.exists(filename + '.npy'):
            self.qw = np.load(filename + '.npy')
            print('Weights loaded.')
        if os.path.exists(filename + '_bias.npy'):
            self.b = np.load(filename + '_bias.npy')
            print('Biases loaded.')
