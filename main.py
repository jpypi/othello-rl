#!/usr/bin/env python3

from game import Game
from players import RLPlayer


g = Game()
players = [RLPlayer(), RLPlayer()]
for p in players:
    g.addPlayer(p)

g.run()

final_score = list(g.getScore().items())
final_score.sort()
print(final_score)
ttl = sum(map(lambda x: x[1], final_score))
print(ttl)

for i, p in enumerate(players):
    print(final_score[i][1]/ttl)
    p.updateWeights(final_score[i][1]/ttl)


#import pygame
#import board
#game = othello()
#player = game.menu.show_menu("Choose Who Begins:")
# try:
#     while True:
#         board.drawSample()
#         #player = game.play_game(1 - player)
# finally:
#     pygame.quit()


# TODO:
#- Pass (no available moves)
