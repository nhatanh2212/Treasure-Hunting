from const import *
from square import Square
from piece import Piece, Mountain, Treasure, Prison, Player

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
                    self._square[row][col].piece = Mountain()
                elif PIECES[row][col] == 'T':
                    self._square[row][col].piece = Treasure()
                elif PIECES[row][col] == 'P':
                    self._square[row][col].piece = Prison()
                elif PIECES[row][col] == 'I':
                    self._square[row][col].piece = Player()
                else:
                    self._square[row][col].piece = Piece('Normal',PIECES[row][col])