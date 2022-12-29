from const import *
from square import Square
from piece import *

class Board:

    def __init__(self, size):
        self._size = size
        self._square = []
        self._create_board(size)
        self._add_pieces()

        
    def _create_board(self, size):
        for row in range(size):
            self._square.append([])
            for col in range(size):
                self._square[row].append(Square(row, col))

    def _add_pieces(self):
        PIECES = VALUES16
        for row in range(self._size):
            for col in range(self._size):
                if PIECES[row][col] == 'M': 
                    self._square[row][col].piece = Piece('mountain',PIECES[row][col])
                elif PIECES[row][col] == 'T':
                    self._square[row][col].piece = Piece('Treasure',PIECES[row][col])
                elif PIECES[row][col] == 'P':
                    self._square[row][col].piece = Piece('Prison',PIECES[row][col])
                elif PIECES[row][col] == '0':
                    self._square[row][col].piece = Piece('Water',PIECES[row][col])
                elif PIECES[row][col] == 'I':
                    self._square[row][col].piece = Player()
                else:
                    self._square[row][col].piece = Piece('Normal',PIECES[row][col])