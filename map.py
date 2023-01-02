import const
from board import Board
import os

class Map:
    def show_map(self, screen, gameMap):
        for row in range(len(gameMap)):
            for col in range(len(gameMap).size):
                if gameMap[row][col] == 0:
                    color = const.BLUE
                elif gameMap[row][col] == 1:
                    color = const.GREEN
                elif gameMap[row][col] == 2:
                    color = const.YELLOW
                elif gameMap[row][col] == 3:
                    color = const.ORANGE
                elif gameMap[row][col] == 4:
                    color = const.PURPLE
                elif gameMap[row][col] == 5:
                    color = const.ORANGE
                elif gameMap[row][col] == 6:
                    color = const.PINK
                else:
                    color = const.TUR
                screen.draw.rect(gameMap, color, (col * const.SIZE, row * const.SIZE, const.SIZE, const.SIZE), 0, 1)

    def show_piece(self, screen, filename, coord):
        img = pygame.image.load(os.path.join(f'images/{filename}'))
        screen.blit(img, (coord.x, coord.y))

        