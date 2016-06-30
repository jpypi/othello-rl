#!/usr/bin/env python3
from pprint import pprint

import numpy as np

from game import Game
from players import RLPlayer

#from matplotlib import pyplot as plt
#plt.ion()

                 #qlr,gamma,netlr (0.03)
player = RLPlayer(0.07, 0.99, 0.03)
rp = RLPlayer(0, 0)

match_size = 10
n_epochs = 2000

player_wins = []
for e in range(n_epochs):
    print("Epoch: %d"%e)

    player.wins = 0
    # Anneal the exploration rate
    player.epsilon = (np.exp(-0.017*e)+0.11)/1.1
    player_gameplay_history = []

    for _ in range(match_size):
        #print("Game: %d"%g)
        player.play_history = []

        # Initialize a new game
        g = Game()
        g.addPlayer(player)
        # Adds a player that won't log to it's move history
        g.addPlayer(rp, False)
        #g.addPlayer(player, False)
        g.run()
        #pprint(player.play_history)

        final_score = list(g.getScore().items())
        final_score.sort()
        ttl = sum(map(lambda x: x[1], final_score))
        #print(ttl)

        # Only deal with 1 of the players (The one we're updating the
        # weights for)
        #player_score = int(final_score[0][1]/ttl >= 0.5)
        player_score =  (final_score[0][1]/ttl - 0.5)*2
        player.wins += player_score > 0
        #print(player_score)
        player_gameplay_history.append((player.play_history, player_score))

    print(player.epsilon, player.wins)
    player_wins.append(player.wins)
    for game, score in player_gameplay_history:
        player.play_history = game
        player.updateWeights(score)

suffix = "linear-0.03"
player.policy_net.save("best-%s.weights"%suffix)
print(sum(player_wins))
with open("%d-%d-%s.csv"%(n_epochs, match_size, suffix), "w") as f:
    f.write("\n".join(map(str, player_wins)))

#plt.plot(player_wins)
#plt.draw()
#plt.ioff()
#plt.show()
