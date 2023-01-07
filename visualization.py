import pygame
import sys
import os
import random
from coord import *
import const

class HintLogDecoder:
    def __init__(self, W, H, gameMap):
        self.W = W
        self.H = H
        self.gameMap = gameMap
    
    def tilesWithoutTreasure(self, args):
        bitmap = [[1]*self.W for _ in range(self.H)]
        for i in range(2, len(args), 2):
            bitmap[int(args[i])][int(args[i+1])] = 0
        return bitmap
    
    def tilesWithTreasure(self, args):
        bitmap = [[0]*self.W for _ in range(self.H)]
        for i in range(2, len(args), 2):
            bitmap[int(args[i])][int(args[i+1])] = 1
        return bitmap

    def regionsWithTreasure(self, args):
        bitmap = [[0]*self.W for _ in range(self.H)]
        regions = list(map(int, args[2:]))
        for row in range(self.H):
            for col in range(self.W):
                if (self.gameMap[row][col] in regions):
                    bitmap[row][col] = 1
        return bitmap

    def regionsWithoutTreasure(self, args):
        bitmap = [[1]*self.W for _ in range(self.H)]
        regions = list(map(int, args[2:]))
        for row in range(self.H):
            for col in range(self.W):
                if (self.gameMap[row][col] in regions):
                    bitmap[row][col] = 0
        return bitmap

    def bigRecWithTreasure(self, args):
        bitmap = [[0]*self.W for _ in range(self.H)]
        x1, y1, x2, y2 = int(args[1]), int(args[2]), int(args[3]), int(args[4])
        for x in range(x1, x2):
            for y in range(y1, y2):
                bitmap[x][y] = 1
        return bitmap

    def smallRecWithoutTreasure(self, args):
        bitmap = [[1]*self.W for _ in range(self.H)]
        x1, y1, x2, y2 = int(args[1]), int(args[2]), int(args[3]), int(args[4])
        for x in range(x1, x2):
            for y in range(y1, y2):
                bitmap[x][y] = 0
        return bitmap

    def agentIsNearestToTreasure(self):
        log = "HINT 7"
        return {
            "log": log
        }
    
    def rowOrColumnWithTreasure(self, args):
        bitmap = [[0]*self.W for _ in range(self.H)]
        isRow = int(args[1])
        if isRow:
            row = int(args[2])
            for col in range(self.W):
                bitmap[row][col] = 1
        else:
            col = int(args[2])
            for row in range(self.H):
                bitmap[row][col] = 1   
        return bitmap
    
    def rowOrColumnWithoutTreasure(self, args):
        bitmap = [[1]*self.W for _ in range(self.H)]
        isRow = int(args[1])
        if isRow:
            row = int(args[2])
            for col in range(self.W):
                bitmap[row][col] = 0
        else:
            col = int(args[2])
            for row in range(self.H):
                bitmap[row][col] = 1   
        return bitmap
    
    def boundX(self, x):
        if (x < 0):
            return 0
        if (x > self.W - 1):
            return self.W - 1
        return x

    def boundY(self, y):
        if (y < 0):
            return 0
        if (y > self.H - 1):
            return self.H - 1
        return y

    def twoRegionBoundaryWithTreasure(self, args):
        bitmap = [[0]*self.W for _ in range(self.H)]
        regA = int(args[1])
        regB = int(args[2])
        deltaX = [1, -1, 0, 0]
        deltaY = [0, 0, 1, -1]
        for row in range(self.H):
            for col in range(self.W):
                at = self.gameMap[row][col]
                if (at == regA or at == regB):
                    for i in range(len(deltaX)):
                        to = self.gameMap[self.boundX(row + deltaX[i])][self.boundY(col + deltaY[i])]
                        if (to != at and (to == regA or to == regB)):
                            bitmap[row][col] = 1
                            bitmap[self.boundX(row + deltaX[i])][self.boundY(col + deltaY[i])]
        return bitmap
    
    def anyRegionBoundaryWithTreasure(self):
        bitmap = [[0]*self.W for _ in range(self.H)]
        deltaX = [1, -1, 0, 0]
        deltaY = [0, 0, 1, -1]
        for row in range(self.H):
            for col in range(self.W):
                if (self.gameMap[row][col] == 0):
                    continue
                at = self.gameMap[row][col]
                for i in range(len(deltaX)):
                    to = self.gameMap[self.boundX(row + deltaX[i])][self.boundY(col + deltaY[i])]
                    if (to != at):
                        bitmap[row][col] = 1
                        bitmap[self.boundX(row + deltaX[i])][self.boundY(col + deltaY[i])]
        return bitmap
    
    def seaBoundaryWithTreasure(self, args):
        bitmap = [[0]*self.W for _ in range(self.H)]
        thickness = args[1]
        deltaX = [0, 0, 1, -1, 0, 0, 2, -2, 0, 0, 3, -3]
        deltaY = [1, -1, 0, 0, 2, -2, 0, 0, 3, -3, 0, 0]
        for row in range(self.H):
            for col in range(self.W):
                if (self.gameMap[row][col] == 0):
                    at = self.gameMap[row][col]
                    for i in range(4*thickness):
                        to = self.gameMap[self.boundX(row + deltaX[i])][self.boundY(col + deltaY[i])]
                        if (to != at):
                            bitmap[row][col] = 1
                            bitmap[self.boundX(row + deltaX[i])][self.boundY(col + deltaY[i])]
        return bitmap



class Visualizer:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont("Times New Roman", 20, True, False)
        self.log = []
        self.turn = 0
        self.isPirateRevealed = False
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
            self.bitMap = [[1]*self.W for _ in range(self.H)]
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
            self.hintLogDecoder = HintLogDecoder(self.W, self.H, self.gameMap)

    
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
                elif gameMap[row][col] == 7:
                    color = const.DARK_GREEN
                elif gameMap[row][col] == 8:
                    color = const.MARGENTA
                elif gameMap[row][col] == 9:
                    color = const.LIGHT_RED
                else:
                    color = const.TUR
                pygame.draw.rect(self.screen, color, (col * const.SIZE, row * const.SIZE, const.SIZE, const.SIZE), 0, 1)
        
    def show_bitmap(self):
        bitMap = self.bitMap
        for row in range(len(bitMap)):
            for col in range(len(bitMap[0])):
                if (bitMap[row][col] == 0):
                    pygame.draw.rect(self.screen, (80, 80, 80), (col * const.SIZE, row * const.SIZE, const.SIZE, const.SIZE), 0, 1)

    def show_piece(self, filename, coord):
        img = pygame.transform.scale(pygame.image.load(os.path.join(f'images/{filename}')), (const.SIZE, const.SIZE))
        self.screen.blit(img, (coord.y*const.SIZE, coord.x*const.SIZE))

    def show_text(self, text):
        _text = self.font.render(text, True, (255, 0, 0))
        self.screen.blit(_text, (0, 0))

    def boundX(self, x):
        if (x < 0):
            return 0
        if (x > self.W - 1):
            return self.W - 1
        return x

    def boundY(self, y):
        if (y < 0):
            return 0
        if (y > self.H - 1):
            return self.H - 1
        return y
    
    def largeScan(self):
        deltaX = [0, 0, 0, 1, -1, 1, -1, 1, -1, 0, 0, 2, -2, 1, 1, -1, -1, 2, 2, -2, -2, 2, 2, -2, -2]
        deltaY = [0, 1, -1, 0, 0, 1, -1, -1, 1, 2, -2, 0, 0, 2, -2, 2, -2, 1, -1, 1, -1, 2, -2, 2, -2]
        for index in range(len(deltaX)):
            x = self.boundX(self.playerCoord.x + deltaX[index])
            y = self.boundX(self.playerCoord.y + deltaY[index])
            self.bitMap[x][y] = 0
    
    def smallScan(self):
        deltaX = [0, 0, 0, 1, -1, 1, -1, 1, -1]
        deltaY = [0, 1, -1, 0, 0, 1, -1, -1, 1]
        for index in range(len(deltaX)):
            x = self.boundX(self.playerCoord.x + deltaX[index])
            y = self.boundX(self.playerCoord.y + deltaY[index])
            self.bitMap[x][y] = 0

    def mergeBitmap(self, hintBitmap, isHintTrue):
        if not isHintTrue:
            for row in range(self.H):
                for col in range(self.W):
                    if (hintBitmap[row][col] == 1):
                        self.bitMap[row][col] = 0
        else:
            for row in range(self.H):
                for col in range(self.W):
                    if (hintBitmap[row][col] == 0):
                        self.bitMap[row][col] = 0
    

    def getHintBitmap(self, args):
        if (int(args[0]) == 1):
            return self.hintLogDecoder.tilesWithoutTreasure(args)
        if (int(args[0]) == 2):
            return self.hintLogDecoder.tilesWithTreasure(args)
        if (int(args[0]) == 3):
            return self.hintLogDecoder.regionsWithTreasure(args)
        if (int(args[0]) == 4):
            return self.hintLogDecoder.regionsWithoutTreasure(args)
        if (int(args[0]) == 5):
            return self.hintLogDecoder.bigRecWithTreasure(args)
        if (int(args[0]) == 6):
            return self.hintLogDecoder.smallRecWithoutTreasure(args)
        if (int(args[0]) == 7):
            return self.hintLogDecoder.agentIsNearestToTreasure()
        if (int(args[0]) == 8):
            return self.hintLogDecoder.rowOrColumnWithTreasure(args)
        if (int(args[0]) == 9):
            return self.hintLogDecoder.rowOrColumnWithoutTreasure(args)
        if (int(args[0]) == 10):
            return self.hintLogDecoder.twoRegionBoundaryWithTreasure(args)
        if (int(args[0]) == 11):
            return self.hintLogDecoder.anyRegionBoundaryWithTreasure()
        if (int(args[0]) == 12):
            return self.hintLogDecoder.seaBoundaryWithTreasure(args)


    def simulate(self, log_path):
        with open(log_path) as file:
            self.turn = 0
            self.numlog = int(file.readline().strip())
            self.isWin = file.readline().strip() == "WIN"
            rawAgentCoord = list(map(int, file.readline().strip().split(" ")[1:]))
            self.playerCoord = Coordination(rawAgentCoord[0], rawAgentCoord[1])
            file.readline() #READ INITIAL DUMMY TURN COMMAND

            line = file.readline().strip().split(" ")
            command = line[0]
            if (command == "ENDG"):
                args = ["WIN"]
            else:
                args = list(map(int, line[1:]))

            while True:
                self.show_map()
                self.show_bitmap()
                self.show_piece("treasure.png", self.T)
                self.show_piece("player.png", self.playerCoord)
                for prisonCoord in self.prisonCoords:
                    self.show_piece("prison.png", prisonCoord)
                if (self.isPirateRevealed):
                    self.show_piece("pirate.png", self.pirateCoord)
                for mountainCoord in self.mountainCoords:
                    self.show_piece("mountain.png", mountainCoord)
                self.show_text("TURN {}".format(self.turn))
                pygame.display.update()
                
                isNewturn = False

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if (command == "ENDG"):
                                continue
                            self.turn += 1
                            isNewturn = True

                if (not isNewturn):
                    continue

                if (command == "ENDG"):
                    self.turn = args[0]
                    continue

                while (command != "TURN"):
                    if (command == "RVEL"):
                        self.isPirateRevealed = True
                        self.pirateCoord = Coordination(args[0], args[1])
                    elif (command == "PMOV"):
                        self.pirateCoord = Coordination(args[0], args[1])
                    elif (command == "ALSN"):
                        self.largeScan()
                    elif (command == "ASSN"):
                        self.playerCoord.x += args[0] * args[1]
                        self.playerCoord.y += args[0] * args[2]
                        self.smallScan()
                    elif (command == "ANSN"):
                        self.playerCoord.x += args[0] * args[1]
                        self.playerCoord.y += args[0] * args[2]
                    elif (command == "HINT"):
                        self.hints.append(self.getHintBitmap(args))
                    elif (command == "VRFY"):
                        bitmap = self.hints[args[0]-1]
                        line = file.readline().strip().split(" ")
                        command = line[0]
                        args = list(map(int, line[1:]))
                        assert(command == "SYST")
                        self.mergeBitmap(bitmap, bool(int(args[0])))
                    elif (command == "ENDG"):
                        self.turn = args[0]
                        break

                    line = file.readline().strip().split(" ")
                    command = line[0]
                    if (command == "ENDG"):
                        args = line[1:]
                    else:
                        args = list(map(int, line[1:]))

                if (command == "ENDG"):
                    continue
                line = file.readline().strip().split(" ")
                command = line[0]
                if (command == "ENDG"):
                    args = ["WIN"]
                else:
                    args = list(map(int, line[1:]))
            


def main(input_path, log_path):
    game = Visualizer()
    game.initialize(input_path)
    game.simulate(log_path)


if __name__ == '__main__':
    if (len(sys.argv) < 3):
        print('usage:\tvisualization.py <input_file> <log_file> <block_size>')
        sys.exit(0)
    if (len(sys.argv) > 3):
        const.SIZE = int(sys.argv[3]) 
    main(sys.argv[1],sys.argv[2])