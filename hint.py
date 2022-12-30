import pygame
from const import *

class Hint:
    def __init__(self, screen):
        self.screen = screen
        self.text = ""
        self.font = pygame.font.SysFont("Times New Roman", 20, True, False)

    def get_hint(self, index):
        if index == 1:
            self.text = "A list of random tiles that doesn't contain the treasure (1 to 12)"
        elif index == 2:
            self.text = "2-5 regions that 1 of them has the treasure."
        elif index == 3:
            self.text = "1-3 regions that do not contain the treasure."    
        elif index == 4:
            self.text = "A large rectangle area that has the treasure."
        elif index == 5:
            self.text = "A small rectangle area that doesn't has the treasure."
        elif index == 6:
            self.text = "He tells you that you are the nearest person to the treasure (between you and the prison he is staying)."
        elif index == 7:
            self.text = "column and/or a row that contain the treasure (rare)."
        elif index == 8:
            self.text = "A column and/or a row that do not contain the treasure."
        elif index == 9:
            self.text = "2 regions that the treasure is somewhere in their boundary."
        elif index == 10:
            self.text = "The treasure is somewhere in a boundary of 2 regions."
        elif index == 11:
            self.text = "The treasure is somewhere in an area bounded by 2-3 tiles from sea."
        elif index == 12:
            self.text = "A half of the map without treasure (rare)."
        elif index == 13:
            self.text = "From the center of the map/from the prison that he's staying, he tells you a direction that has the treasure."
        elif index == 14:
            self.text = "2 squares that are different in size, the small one is placed inside the bigger one, the treasure is somewhere inside the gap between 2 squares."
        elif index == 15:
            self.text = "The treasure is in a region that has mountain."

    def print_hint(self):
        surface = self.font.render(self.text, True, (255, 0, 0))
        self.screen.blit(surface, (0, 0))     