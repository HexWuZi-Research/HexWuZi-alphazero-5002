'''
Board class.
Board data:
  1=white, -1=black, 0=empty,10=edge
  first dim is column , 2nd is row:
     pieces[1][7] is the square in column 2,
     at the opposite end of the board in row 8.
Squares are stored and manipulated as (x,y) tuples.
x is the column, y is the row.
'''
import numpy as np
class Board():
    def __init__(self, n=11):
        "Set up initial board configuration."
        self.n = n
        # Create the empty board array.
        self.pieces = np.zeros([self.n, self.n])
        for i in range(self.n // 2):
            self.pieces[i][11 - (5 - i):] = 10
            self.pieces[10 - i][:5 - i] = 10


    # add [][] indexer syntax to the Board
    def __getitem__(self, index):
        return self.pieces[index]

    def get_legal_moves(self):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black
        """
        moves = set()  # stores the legal moves.
        # Get all empty locations.
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y] == 0:
                    moves.add((x, y))
        return list(moves)

    def has_legal_moves(self):
        """Returns True if has legal move else False
        """
        # Get all empty locations.
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y] == 0:
                    return True
        return False

    def execute_move(self, move, color):
        """Perform the given move on the board; flips pieces as necessary.
        color gives the color pf the piece to play (1=white,-1=black)
        """
        (x,y) = move
        assert self[x][y] == 0
        self[x][y] = color
