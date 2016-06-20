import numpy as np

import board


class Game:
    def __init__(self):
        self.players = []
        self.board = board.Board()

    def addPlayer(self, player):
        self.players.append(player)

    def getScore(self):
        return self.board.getScore()

    def run(self):
        while self.board.getRemainingMoves() > 0:
            for i, player in enumerate(self.players):
                # Pass the player a function it can use to make a move
                # i*2-1 rescales index as if it were an interval
                # (0, 1) -> (-1, 1)
                did_move = player.play(lambda r,c: self.board.updateBoard(i*2-1, r, c),
                                   self.board.getState(), i*2-1)
                self.board.printBoard()
                if not did_move:
                    print("Someone is stuck")
