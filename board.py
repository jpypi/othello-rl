import sys
import numpy as np
from colorama import Fore, Back, Style
from colorama import init
init(autoreset=True)


def getRow(row):
    ret = ""
    for i in np.nditer(row):
        ret += getItem(i)
    return ret


def getItem(item):
    if item == 1 :
        return Fore.WHITE + "|" + Fore.BLACK + "O"
    elif item == 0 :
        return Fore.WHITE + "| "
    else:
        return Fore.WHITE + "|" + Fore.WHITE + "O"


class Board(object):
    #player colors
    BLACK = 1 #player 1
    WHITE = -1 #player 2

    def __init__(self):
        self.board = np.array([ [0]*8 ] * 8, dtype=int)
        self.newGame()

    def newGame(self):
        """
        Load board with init conditions
        And sync virtual board
        """
        self.remaining_moves = 0

        self.board[3][3] = 1
        self.board[4][4] = 1
        self.board[4][3] = -1
        self.board[3][4] = -1

        self.nextTurn = self.BLACK
        self.syncVirtualBoard()

    def syncVirtualBoard(self):
        """
        Syncronize virtual and current board
        """
        self.virtualBoard = np.copy(self.board)

    def getRemainingMoves(self):
        return self.remaining_moves

    def getState(self):
        return self.board

    def updateBoard(self, type, tile, row, col):
        """
        @param string type
            either 'virtual' or 'live'
        @param int tile
            either 1 or -1
                1 for player 1 (black)
                -1 for player 2 (white)
        @param int row
            0-7 which row
        @param int col
            0-7 which col
        @return bool
            true if valid
            false if invalid move - doesn't update board
        """
        board = self.board if type == 'live' else self.virtualBoard
        result = self.isValidMove(board, tile, row, col)
        if result != False:
            board[row][col] = tile
            for row in result:
                board[ row[0] ][ row[1] ] = tile
            if type == 'live':
                self.syncVirtualBoard()

            return True
        else:
            return False


    def printBoard(self, type):
        """
        Print board to terminal for debugging
        @param string type 'virtual' or 'live'
        """
        board = self.board if type == 'live' else self.virtualBoard

        print("\t" + Back.GREEN +              "      BOARD      ")
        print("\t" + Back.GREEN + Fore.WHITE + " |0|1|2|3|4|5|6|7")
        for i in range(8):
            print("\t" + Back.GREEN + Fore.WHITE + "{}{}".format(i, getRow(board[i])))
            sys.stdout.write(Style.RESET_ALL)

    def isOnBoard(self, x, y):
        """
        Returns True if the coordinates are located on the board.
        """
        return x >= 0 and x <= 7 and y >= 0 and y <= 7

    def isValidMove(self, type, tile, xstart, ystart):
        """
        From https://inventwithpython.com/reversi.py
        @param String type 'live' or 'virtual'
        @param int tile
            self.BLACK or self.WHITE
        @param int xstart
        @param int ystart
        Returns False if the player's move on space xstart, ystart is invalid.
        If it is a valid move, returns a list of spaces that would become the
        player's if they made a move here.
        """
        board = self.board if type == 'live' else self.virtualBoard

        if not self.isOnBoard(xstart, ystart) or board[xstart][ystart] != 0:
            return False

        # temporarily set the tile on the board.
        board[xstart][ystart] = tile

        otherTile = tile * -1

        tilesToFlip = []
        # loop through all directions around flipped tile
        for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x, y = xstart, ystart
            x += xdirection # first step in the direction
            y += ydirection # first step in the direction
            if self.isOnBoard(x, y) and board[x][y] == otherTile:
                # There is a piece belonging to the other player next to our piece.
                x += xdirection
                y += ydirection
                if not self.isOnBoard(x, y):
                    continue
                while board[x][y] == otherTile:
                    x += xdirection
                    y += ydirection
                    if not self.isOnBoard(x, y):
                        # break out of while loop, then continue in for loop
                        break
                if not self.isOnBoard(x, y):
                    continue
                if board[x][y] == tile:
                    # There are pieces to flip over. Go in the reverse direction
                    # until we reach the original space, noting all the tiles
                    # along the way.
                    while True:
                        x -= xdirection
                        y -= ydirection
                        if x == xstart and y == ystart:
                            break
                        tilesToFlip.append([x, y])

        # restore the empty space
        board[xstart][ystart] = 0

        # If no tiles were flipped, this is not a valid move.
        if len(tilesToFlip) == 0:
            return False
        else:
            return tilesToFlip


if __name__ == "__main__":
    board = Board()
    print("================INIT================")
    board.printBoard("live")
    print("================VIRTUAL================")
    board.updateBoard("vitrual", board.BLACK, 4, 2)
    board.printBoard("virtual")
    print("IS VALID MOVE[4,4]?", board.updateBoard("virtual", board.BLACK, 4, 4))
    print("================LIVE================")
    board.updateBoard("live", board.BLACK, 2, 4)
    board.printBoard("live")
