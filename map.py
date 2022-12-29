import pygame
from const import *
from board import Board
from dragger import Dragger
import os

class Map:
    def __init__(self , size):
        self.size = size
        self.board = Board(size)
        self.dragger = Dragger()

    def show_map(self, surface):
        LIST = REGION16 
        PSIZE = WIDTH / self.size
        for row in range(self.size):
            for col in range(self.size):
                if LIST[row][col] == 0:
                    color = BLUE
                elif LIST[row][col] == 1:
                    color = GREEN
                elif LIST[row][col] == 2:
                    color = YELLOW
                elif LIST[row][col] == 3:
                    color = ORANGE
                elif LIST[row][col] == 4:
                    color = PURPLE
                elif LIST[row][col] == 5:
                    color = ORANGE
                elif LIST[row][col] == 6:
                    color = PINK
                else:
                    color = TUR
                pygame.draw.rect(surface, color, (row * PSIZE, col * PSIZE, PSIZE, PSIZE),0,1)

    def show_piece(self, surface):
        PSIZE = WIDTH / self.size
        for row in range(self.size):
            for col in range(self.size):
                if self.board._square[row][col].has_piece():
                   piece = self.board._square[row][col].piece
                if piece is not self.dragger.piece:
                    piece.set_texture()
                    img = pygame.image.load(piece.texture)
                    img_center = col * PSIZE + PSIZE // 2, row * PSIZE + PSIZE // 2
                    piece.texture_rect = img.get_rect(center=img_center)
                    surface.blit(img, piece.texture_rect)


        