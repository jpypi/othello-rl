#!/usr/bin/env python3

from game import Game
from players import RLPlayer


g = Game()
players = [RLPlayer(), RLPlayer()]
for p in players:
    g.addPlayer(p)

g.run()

g.getScore()


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
