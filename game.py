import numpy as np

import board


class Game:
    def __init__(self):
        self.players = []
        self.board = board.Board()

    def addPlayer(self, player, log_move_history = True):
        self.players.append((player, log_move_history))

    def getScore(self):
        return self.board.getScore()

    def run(self):
        n_passed = 0
        # Run until both players have passed
        while n_passed < 2:
            n_passed = 0
            for i, player in enumerate(self.players):
                # Pass the player a function it can use to make a move
                # i*2-1 rescales index as if it were an interval
                # (0, 1) -> (-1, 1)
                # Player id
                pid = i*2-1
                did_move = player[0].play(lambda r,c: self.board.updateBoard(pid,r,c),
                                   self.board.getState(), pid, player[1])

                #self.board.printBoard()

                if not did_move:
                    n_passed += 1
