#!/usr/bin/env python3
from pprint import pprint

from game import Game
from players import RLPlayer

player = RLPlayer()

match_size = 10
n_epochs = 100

player_wins = []
for e in range(n_epochs):
    print("Epoch: %d"%e)

    player.prepForNewGame()

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

        # Only deal with 1 of the players (The one we're updating the
        # weights for)
        player_score = final_score[0][1]/ttl
        player.wins += player_score > 0.5
        player.updateWeights(player_score)

    player_wins.append(player.wins)

pprint(player_wins)
