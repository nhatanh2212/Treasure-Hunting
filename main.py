import pygame
import sys
from map import Map
from const import *

class Main:
    def __init__(self):
        pygame.init()
        # print('Enter the map size(16, 32,64: ')
        # x = input()
        self._map = Map(16)
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT))
        pygame.display.set_caption('Treasure Island')
 
    def main_loop(self):
        screen = self.screen
        map = self._map

        while True:
            map.show_map(screen)
            map.show_piece(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
            pygame.display.update()

main = Main()
main.main_loop()