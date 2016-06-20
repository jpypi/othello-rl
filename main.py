#!/usr/bin/env python3
from pprint import pprint

from game import Game
from players import RLPlayer

players = [RLPlayer(), RLPlayer()]

match_size = 10
n_epochs = 100

player_wins = []
for e in range(n_epochs):
    print("Epoch: %d"%e)

    for p in players:
        p.prepForNewGame()

    for g in range(match_size):
        print("Game: %d"%g)
        # Initialize a new game
        g = Game()
        for p in players:
            g.addPlayer(p)
        g.run()

        final_score = list(g.getScore().items())
        final_score.sort()
        ttl = sum(map(lambda x: x[1], final_score))

        for i, p in enumerate(players):
            if final_score[i][1]/ttl > 0.5:
                p.wins += 1
            p.updateWeights(final_score[i][1]/ttl)

    player_wins.append(tuple(map(lambda x: x.wins, players)))

pprint(player_wins)
