from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from GobangLogicnew import Board
import numpy as np


class GobangGame(Game):
    def __init__(self, n=11):
        self.n = n

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.n)
        return np.array(b.pieces)

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self):
        # return number of actions
        #return self.n + (self.n + self.n//2)/2 * 10
        return self.n * self.n

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        if action == self.n * self.n:
            return (board, -player)
        b = Board(self.n)
        b.pieces = np.copy(board)
        move = (int(action / self.n), action % self.n)
        b.execute_move(move, player)
        return (b.pieces, -player)

    # modified
    def getValidMoves(self, board):
        # return a fixed size binary vector
        # if valid[n * x + y]=1, walk can in x,y position
        valids = [0] * self.getActionSize()
        b = Board(self.n)
        b.pieces = np.copy(board)
        legalMoves = b.get_legal_moves()
        if len(legalMoves) == 0:
            valids[-1] = 1
            return np.array(valids)
        for x, y in legalMoves:
            valids[self.n * x + y] = 1
        return np.array(valids)

    def check_single(self, line, player):
        L = len(line)
        opponent = player * (-1)
        for i in range(L-4):
            if player == line[i+1] == line[i+2] == line[i+3] == line[i+4]:
                if (i == 0 or line[i-1] != player) and (i == L-5 or line[i+5] != player):
                    return player
            if opponent == line[i+1] == line[i+2] == line[i+3] == line[i+4]:
                if (i == 0 or line[i-1] != opponent) and (i == L-5 or line[i+5] != opponent):
                    return opponent
        return 0

    # modified
    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        b = Board(self.n)
        b.pieces = np.copy(board)
        # check if anybody win
        for i in range(6):
            winner = self.check_single(board[i, :i+6], player)
            if winner != 0:
                return winner
            winner = self.check_single(board[:i+6, i], player)
            if winner != 0:
                return winner
        for i in range(6, 11):
            winner = self.check_single(board[i, i-5:], player)
            if winner != 0:
                return winner
            winner = self.check_single(board[i-5:, i], player)
            if winner != 0:
                return winner
        for k in range(-5, 6):
            print(np.diag(board, k))
            winner = self.check_single(np.diag(board, k), player)
            if winner != 0:
                return winner
        #check if there is still legal moves
        if b.has_legal_moves():
            return 0
        # check if terminated when nobody win
        if not 0 in board:
            return 0
        return 0

    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        new_board=player * board
        for i in range(self.n // 2):
            new_board[i][11 - (5 - i):] = 10
            new_board[10 - i][:5 - i] = 10
        return new_board

    # modified
    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert(len(pi) == self.n**2 + 1)  # 1 for pass
        pi_board = np.reshape(pi[:-1], (self.n, self.n))
        l = []
        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(board, i)
                newPi = np.rot90(pi_board, i)
                if j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)
                l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        return l

    def stringRepresentation(self, board):
        return board.tostring()

    def display(self, board):
        n = board.shape[0]

        for y in range(n):
            print(y, "|", end="")
        print("")
        print(" -----------------------")
        for y in range(n):
            print(y, "|", end="")    # print the row #
            for x in range(n):
                piece = board[y][x]    # get the piece to print
                if piece == -1:
                    print("b ", end="")
                elif piece == 1:
                    print("W ", end="")
                else:
                    if x == n:
                        print("-", end="")
                    else:
                        print("- ", end="")
            print("|")
        print("   -----------------------")