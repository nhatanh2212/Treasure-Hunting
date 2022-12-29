from const import *
from square import Square
from piece import *

class Board:

    def __init__(self, size):
        self._size = size
        self._square = []
        self._create_board(size)
        self._add_pieces(0, 0)

        
    def _create_board(self, size):
        for row in range(size):
            self._square.append([])
            for col in range(size):
                self._square[row].append(Square(row, col))

    def _add_pieces(self, row, col):
        for row in range(self._size):
            for col in range(self._size):
                    self._square[row][col].piece = Mountain()