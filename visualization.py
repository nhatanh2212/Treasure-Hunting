import pygame
import sys
import os
import random
from coord import *
import const

class Hint:
    pass

class Game:
    def __init__(self):
        pygame.init()
        self.log = []
        self.turn = 0
        self.hints = []

    def initialize(self, input_path):
        with open(input_path) as file:
            dimensions = list(map(int, file.readline().strip().split(" ")))
            self.W = dimensions[0]
            self.H = dimensions[1]
            self.screen = pygame.display.set_mode((const.SIZE*self.W, const.SIZE*self.H))
            self.r = int(file.readline().strip())
            self.f = int(file.readline().strip())
            self.R = int(file.readline().strip())
            treasureCoord = list(map(int, file.readline().strip().split(" ")))
            self.T = Coordination(treasureCoord[0], treasureCoord[1])
            self.gameMap = []
            self.mountainCoords = []
            self.prisonCoords = []
            possiblePlayerSpawnCoords = []
            for row in range(self.H):
                rawRow = file.readline().replace(" ", "").split(";")
                self.gameMap.append([])
                for col in range(self.W):
                    if rawRow[col][-1].isalpha():
                        self.gameMap[-1].append(int(rawRow[col][:-1]))
                        if (rawRow[col][-1] == 'M'):
                            self.mountainCoords.append(Coordination(row, col))
                        elif (rawRow[col][-1] == 'P'):
                            self.prisonCoords.append(Coordination(row, col))
                    else:
                        self.gameMap[-1].append(int(rawRow[col]))
                        if (int(rawRow[col]) != 0):
                            possiblePlayerSpawnCoords.append(Coordination(row, col))
            self.playerCoord = possiblePlayerSpawnCoords[random.randint(0, len(possiblePlayerSpawnCoords) - 1)]
            self.pirateCoord = self.prisonCoords[random.randint(0, len(self.prisonCoords) - 1)]
    
    def endCondition(self):
        if (self.pirateCoord == self.T):
            self.log.append("Pirate wins")
            self.log.append("End game")
            return True
        if (self.playerCoord == self.T):
            self.log.append("Agent wins")
            self.log.append("End game")
            return True
        return False

    def show_map(self):
        gameMap = self.gameMap
        for row in range(len(gameMap)):
            for col in range(len(gameMap[0])):
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
                pygame.draw.rect(self.screen, color, (col * const.SIZE, row * const.SIZE, const.SIZE, const.SIZE), 0, 1)

    def show_piece(self, filename, coord):
        img = pygame.image.load(os.path.join(f'images/{filename}'))
        self.screen.blit(img, (coord.y*const.SIZE, coord.x*const.SIZE))

    def generate_hint(self):
        pass

    def simulate(self):
        while True:
            self.show_map()
            self.show_piece("player.png", self.playerCoord)
            for prisonCoord in self.prisonCoords:
                self.show_piece("prison.png", prisonCoord)
            if (self.turn > self.r):
                self.show_piece("pirate.png", self.pirateCoord)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            if (self.endCondition()):
                # END GAME LÀM CÁI GÌ ĐÓ NHƯ HIỆN KQ
                break
            self.hints.append(Hint())
            if (self.turn == self.r):
                self.log.append("Pirate reveals his position at {}".format(self.pirateCoord))
            if (self.turn > self.f):
              pass
                # PIRATE MOVES
            #AGENTS MOVE
            


def main(input_path, output_path):
    game = Game()
    game.initialize(input_path)
    game.simulate()

if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print('usage:\tmain.py <input_file> <output_file>')
        sys.exit(0)
    main(sys.argv[1],sys.argv[2])