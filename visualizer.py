#!/usr/bin/env python3
from game import Game
from players import *

h = HumanPlayer()
ai = RLPlayer(1,1,1)
ai.policy_net.load("best.weights")

g = Game()
g.addPlayer(ai)
g.addPlayer(h)
g.run(True)
