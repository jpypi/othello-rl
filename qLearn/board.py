import numpy as np
from reinforce import Player

from colorama import Fore, Back, Style
from colorama import init
init(autoreset=True)

board = None


def getRow(row):
    ret = ""
    for i in np.nditer(row):
        ret += getItem(i)
    return ret


def getItem(item):
    if item == 1:
        return Fore.WHITE + "|" + Fore.BLACK + "O"
    elif item == 0:
        return Fore.WHITE + "| "
    else:
        return Fore.WHITE + "|" + Fore.WHITE + "O"


class Board(object):
    # player colors
    BLACK = 1  # player 1
    WHITE = -1  # player 2

    def __init__(self, size=8):
        size = int(size)
        if size % 2 != 0:
            size += 1
        self.size = size
        self.newGame()
        return

    def newGame(self):
        """
        Load board with init conditions
        And sync virtual board
        """
        self.board = np.array([[0]*self.size] * self.size, dtype=int)
        mL = int(self.board.shape[0]/2 - 1)
        mR = int(self.board.shape[0]/2)
        self.board[mL][mL] = 1
        self.board[mR][mR] = 1
        self.board[mR][mL] = -1
        self.board[mL][mR] = -1

        self.nextTurn = self.BLACK
        self.syncVirtualBoard()
        self.gameOver = False

        return

    def loadFromState(self, t, state):
        if t == 'live':
            tBoard = self.board
        else:
            tBoard = self.virtualBoard

        for x in range(self.size):
            for y in range(self.size):
                tBoard[x][y] = state[x * self.size + y]

    def syncVirtualBoard(self):
        """
        Syncronize virtual and current board
        """
        self.virtualBoard = np.copy(self.board)
        self.virtualNextTurn = self.nextTurn
        return

    def getBoard(self):
        return self.board

    def validateBoard(self, t='live'):
        '''
        Determines if players can still make moves.
        If a player cannot move, their turn is automatically skipped.
        If neither player can move, the game has ended.
        Returns False if the game continues, -1 or 1 if the game has ended.
        '''
        if self.isGameOver(t):
            print("Game Over")
            wOwn = self.getOwnership(self.WHITE)
            bOwn = self.getOwnership(self.BLACK)
            if wOwn > bOwn:
                print("White wins with", wOwn, "territory to black's", bOwn, ".")
                return self.WHITE
            else:
                print("Black wins with", bOwn, "territory to white's", wOwn, ".")
                return self.BLACK

        nt = self.nextTurn if t == 'live' else self.virtualNextTurn
        if not self.canMove(t, nt):
            if nt == self.BLACK:
                print("Black cannot move, turn passed.")
                if t == 'live':
                    self.nextTurn = self.WHITE
                else:
                    self.virtualNextTurn = self.WHITE
            else:
                print("White cannot move, turn passed.")
                if t == 'live':
                    self.nextTurn = self.BLACK
                else:
                    self.virtualNextTurn = self.BLACK
        return False

    def isGameOver(self, t):
        for x in range(self.size):
            for y in range(self.size):
                valid = self.isValidMove(t, self.BLACK, x, y) or self.isValidMove(t, self.WHITE, x, y)
                if valid:
                    return False
        return True

    def canMove(self, t, color):
        for x in range(self.size):
            for y in range(self.size):
                valid = self.isValidMove(t, color, x, y)
                if valid:
                    return True
        return False

    def updateBoard(self, t, tile, row, col):
        """
        @param string t
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
        board = self.board if t == 'live' else self.virtualBoard
        result = self.isValidMove(board, tile, row, col)
        if result != False:
            if t == 'live' :
                self.nextTurn = self.BLACK if self.nextTurn != self.BLACK else self.WHITE
            else:
                self.virtualNextTurn = self.BLACK if self.virtualNextTurn != self.BLACK else self.WHITE

            board[row][col] = tile
            for row in result:
                board[ row[0] ][ row[1] ] = tile
            if ( t == 'live'):
                self.syncVirtualBoard()

            return True
        else:
            return False

    def getOwnership(self, tile):
        flatBoard = self.board.flatten()
        owned = 0
        total = 0
        for t in flatBoard:
            if t != 0:
                total += 1
            if t == tile:
                owned += 1
        return owned/total

    def printBoard(self, t='live'):
        """
        Print board to terminal for debugging
        @param string type 'virtual' or 'live'
        """
        board = self.board if t == 'live' else self.virtualBoard

        print(Back.GREEN +              "\t      BOARD      ")

        # Print column titles
        head = Back.GREEN + Fore.WHITE + "\t "
        for i in range(self.board.shape[0]):
            head += '|' + str(i)
        print(head)

        # Print rows
        for i in range(self.board.shape[0]):
            print(Back.GREEN + Fore.WHITE + "\t" + str(i) + getRow(board[i]))
        print(Style.RESET_ALL)

        return

    def isOnBoard(self, x, y):
        """
        Returns True if the coordinates are located on the board.
        """
        return x >= 0 and x < self.board.shape[0] and y >= 0 and y < self.board.shape[0]

    def isValidMove(self, t, tile, xstart, ystart):
        """
        From https://inventwithpython.com/reversi.py
        @param String t 'live' or 'virtual'
        @param int tile
            self.BLACK or self.WHITE
        @param int xstart
        @param int ystart
        Returns False if the player's move on space xstart, ystart is invalid.
        If it is a valid move, returns a list of spaces that would become the player's if they made a move here.
        """
        board = self.board if str(t) == 'live' else self.virtualBoard
        if not self.isOnBoard(xstart, ystart) or board[xstart][ystart] != 0:
            return False

        # temporarily set the tile on the board.
        board[xstart][ystart] = tile

        otherTile = tile * -1

        tilesToFlip = []
        # loop through all directions around flipped tile
        for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x, y = xstart, ystart
            x += xdirection  # first step in the direction
            y += ydirection  # first step in the direction
            if self.isOnBoard(x, y) and board[x][y] == otherTile:
                # There is a piece belonging to the other player next to our piece.
                x += xdirection
                y += ydirection
                if not self.isOnBoard(x, y):
                    continue
                while board[x][y] == otherTile:
                    x += xdirection
                    y += ydirection
                    if not self.isOnBoard(x, y):  # break out of while loop, then continue in for loop
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

        board[xstart][ystart] = 0  # restore the empty space
        if len(tilesToFlip) == 0:  # If no tiles were flipped, this is not a valid move.
            return False
        else:
            return tilesToFlip


def processUserTurn(color):
    success = False
    try:
        while not success:
            move = input('Move coords (q to quit): ')
            if 'q' in move:
                quit()
            elif ',' in move:
                int(move.split(',')[0])
                int(move.split(',')[1])

            if board.updateBoard('live',  color, int(move.split(',')[0]), int(move.split(',')[1])):
                success = True
            else:
                print('Invalid move')
    except ValueError:
        print("Invalid input")


if __name__ == "__main__":
    board = Board(10)
    board.printBoard()

    whiteWins = 0
    blackWins = 0
    game = 0

    # Init AI player
    player_A = Player(board, board.WHITE)
    player_B = Player(board, board.BLACK)

    iterations = 1000
    # Training - no board print
    for i in range(iterations):
        if board.nextTurn == board.BLACK:
            player_B.takeTurn()
        else:
            player_A.takeTurn()

        v = board.validateBoard()

        while not bool(v):
            turn = board.nextTurn
            if turn == board.BLACK:
                player_B.takeTurn()
            else:
                player_A.takeTurn()
            v = board.validateBoard()
        if v == board.BLACK:
            blackWins += 1
        else:
            whiteWins += 1
        game += 1

        # Adjust exploration - reduces random choices as game number
        # approaches iterations
        player_A.explore = 1 # - game/iterations
        player_B.explore = 1 - game/iterations
        board.newGame()
    print("White won", whiteWins, "games.")
    print("Black won", blackWins, "games.")


    player_B.saveWeights("weights")
    quit()

    if board.nextTurn == board.BLACK:
        print("Black's turn")
#        processUserTurn(board.BLACK)
        player_B.takeTurn()
    else:
        print("White's turn")
        player_A.takeTurn()

    # Show play
    board.printBoard()

    while board.validateBoard():
        turn = board.nextTurn
        if turn == board.BLACK:
            print("Black's turn")
#            processUserTurn(board.BLACK)
            player_B.takeTurn()
        else:
            print("White's turn")
            player_A.takeTurn()
        board.printBoard()
