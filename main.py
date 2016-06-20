#!/usr/bin/env python3
from pprint import pprint

import numpy as np

from game import Game
from players import RLPlayer

player = RLPlayer()

match_size = 10
n_epochs = 100

player_wins = []
for e in range(n_epochs):
    print("Epoch: %d"%e)

    player.prepForNewGame()
    # Anneal the exploration rate
    player.epsilon = np.exp(0.04*(-e+11))+0.2
    player_gameplay_history = []

    for g in range(match_size):
        print("Game: %d"%g)

        # Initialize a new game
        g = Game()
        g.addPlayer(player)
        # Adds a player that won't log to it's move history
        g.addPlayer(player, False)
        g.run()

        final_score = list(g.getScore().items())
        final_score.sort()
        ttl = sum(map(lambda x: x[1], final_score))
        print(ttl)

        # Only deal with 1 of the players (The one we're updating the
        # weights for)
        player_score = final_score[0][1]/ttl
        player.wins += player_score > 0.5
        print(player_score)
        player_gameplay_history.append((player.play_history, player_score))

    player_wins.append(player.wins)
    for game, score in player_gameplay_history:
        player.play_history = game
        player.updateWeights(score)


pprint(player_wins)
