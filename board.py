import pygame
import numpy as np
# import menu
import hoverable

from termcolor import colored
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
    elif  item == 0 :
        return Fore.WHITE + "| "
    else :
        return Fore.WHITE + "|" + Fore.WHITE + "O"

class Board(object):
    #player colors
    BLACK = 1 #player 1
    WHITE = -1 #player 2

    def __init__(self):
        self.board = np.array([ [0]*8 ] * 8, dtype=int)
        self.newGame()
        return

    def newGame(self):
        """
        Load board with init conditions
        And sync virtual board
        """
        self.board[3][3] = 1
        self.board[4][4] = 1
        self.board[4][3] = -1
        self.board[3][4] = -1

        self.nextTurn = self.BLACK
        self.syncVirtualBoard()

        return

    def syncVirtualBoard(self):
        """
        Syncronize virtual and current board
        """
        self.virtualBoard = np.copy(self.board)
        self.virtualNextTurn = self.nextTurn
        return

    def getBoard(self):
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
        print( "TYPE", type )
        result = self.isValidMove(board, tile, row, col)
        if result != False:
            if board == 'live' :
                self.nextTurn = self.BLACK if self.nextTurn == self.BLACK else self.WHITE
            else:
                self.virtualNextTurn = self.BLACK if self.virtualNextTurn == self.BLACK else self.WHITE

            board[row][col] = tile
            # for row in result:
            #     board[ row[0] ][ row[1] ] = tile

            return True
        else:
            return False


    def printBoard(self, type):
        """
        Print board to terminal for debugging
        @param string type 'virtual' or 'live'
        """
        board = self.board if type == 'live' else self.virtualBoard

        print(Back.GREEN +              "\t      BOARD      ")
        print(Back.GREEN + Fore.WHITE + "\t |0|1|2|3|4|5|6|7")
        print(Back.GREEN + Fore.WHITE + "\t0" + getRow(board[0]))
        print(Back.GREEN + Fore.WHITE + "\t1" + getRow(board[1]))
        print(Back.GREEN + Fore.WHITE + "\t2" + getRow(board[2]))
        print(Back.GREEN + Fore.WHITE + "\t3" + getRow(board[3]))
        print(Back.GREEN + Fore.WHITE + "\t4" + getRow(board[4]))
        print(Back.GREEN + Fore.WHITE + "\t5" + getRow(board[5]))
        print(Back.GREEN + Fore.WHITE + "\t6" + getRow(board[6]))
        print(Back.GREEN + Fore.WHITE + "\t7" + getRow(board[7]))
        print(Style.RESET_ALL)

        return

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
        If it is a valid move, returns a list of spaces that would become the player's if they made a move here.
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
                    if not self.isOnBoard(x, y): # break out of while loop, then continue in for loop
                        break
                if not self.isOnBoard(x, y):
                    continue
                if board[x][y] == tile:
                    # There are pieces to flip over. Go in the reverse direction until we reach the original space, noting all the tiles along the way.
                    while True:
                        x -= xdirection
                        y -= ydirection
                        if x == xstart and y == ystart:
                            break
                        tilesToFlip.append([x, y])

        board[xstart][ystart] = 0 # restore the empty space
        if len(tilesToFlip) == 0: # If no tiles were flipped, this is not a valid move.
            return False
        else:
            return tilesToFlip

if __name__ == "__main__":
    board = Board()
    print("================INIT================")
    board.printBoard( 'live' )
    # print("Is valid[3,4]? ", board.isValidMove(None, 1, 3,4))
    # print("Is valid[2,4]? ", board.isValidMove(None, 1, 2,4))
    # print("Is valid[1,4]? ", board.isValidMove(None, -1, 1,4))
    # print("Is valid[0,4]? ", board.isValidMove(None, 1, 0,4))
    #board.updateBoard( board.virtualBoard, board.BLACK, 2,4 )
    board.updateBoard( 'live', board.BLACK, 2,4 )
    print("================VIRTUAL================")
    board.printBoard( "virtual" )
    print("================LIVE================")
    board.printBoard( "live" )
