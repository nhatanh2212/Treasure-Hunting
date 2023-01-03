import sys
import os
import random
from coord import *
import const

class HintFactory:
    def __init__(self, W, H, R, gameMap):
        self.W = W
        self.H = H
        self.R = R
        self.gameMap = gameMap

    def firstHint(self):
        num = random.randint(1, min(12, self.H*self.W - 1))
        bitmap = [[1]*self.W for _ in range(self.H)]
        log = "HINT 1 {} ".format(num)
        uniqueNode = set()
        while len(uniqueNode) < num:
            x = random.randint(0, self.W-1)
            y = random.randint(0, self.H-1)
            if (x, y) in uniqueNode:
                continue
            bitmap[x][y] = 0
            uniqueNode.add((x, y))
            log += "{} {} ".format(x, y)
        return {
            "bitmap": bitmap,
            "log": log
        }
    
    def tilesWithoutTreasure(self, firstHint):
        num = random.randint(1, 12)
        bitmap = [[1]*self.W for _ in range(self.H)]
        log = "HINT 1 {} ".format(num)     
        for _ in range(num):
            x = random.randint(0, self.W-1)
            y = random.randint(0, self.H-1)
            bitmap[x][y] = 0
            log += "{} {} ".format(x, y)
        return {
            "bitmap": bitmap,
            "log": log
        }
    
    def tilesWithTreasure(self):
        num = random.randint(5, 20)
        bitmap = [[0]*self.W for _ in range(self.H)]
        log = "HINT 2 {} ".format(num)
        for _ in range(num):
            x = random.randint(0, self.W-1)
            y = random.randint(0, self.H-1)
            bitmap[x][y] = 1
            log += "{} {} ".format(x, y)
        return {
            "bitmap": bitmap,
            "log": log
        }

    def regionsWithTreasure(self):
        num = random.randint(2, 5)
        bitmap = [[0]*self.W for _ in range(self.H)]
        log = "HINT 3 {} ".format(num)
        regions = []
        for _ in range(num):
            regions.append(random.randint(0, self.R))
            log += "{} ".format(regions[-1])
        for row in range(self.H):
            for col in range(self.W):
                if (self.gameMap[row][col] in regions):
                    bitmap[row][col] = 1
        return {
            "bitmap": bitmap,
            "log": log
        }

    def regionsWithoutTreasure(self):
        num = random.randint(1, 3)
        bitmap = [[1]*self.W for _ in range(self.H)]
        log = "HINT 4 {} ".format(num)
        regions = []
        for _ in range(num):
            regions.append(random.randint(0, self.R-1))
        for row in range(self.H):
            for col in range(self.W):
                if (self.gameMap[row][col] in regions):
                    bitmap[row][col] = 0
        return {
            "bitmap": bitmap,
            "log": log
        }

    def bigRecWithoutTreasure(self):
        bitmap = [[0]*self.W for _ in range(self.H)]
        x1, y1 = random.randint(0, self.W // 2), random.randint(0, self.H // 2)
        minSize = max(self.W, self.H) // 2
        x2, y2 = min(self.W - 1, x1 + random.randint(minSize, 2*minSize)), min(self.H - 1, y1 + random.randint(minSize, 2*minSize))
        log = "HINT 5 {} {} {} {}".format(x1, y1, x2, y2)
        for x in range(x1, x2):
            for y in range(y1, y2):
                bitmap[x][y] = 1
        return {
            "bitmap": bitmap,
            "log": log
        }

    def smallRecWithTreasure(self):
        bitmap = [[1]*self.W for _ in range(self.H)]
        x1, y1 = random.randint(0, self.W-1), random.randint(0, self.H-1)
        maxSize = max(self.W, self.H) // 3
        x2, y2 = min(self.W - 1, x1 + random.randint(0, maxSize)), min(self.H - 1, y1 + random.randint(0, maxSize))
        log = "HINT 6 {} {} {} {}".format(x1, y1, x2, y2)
        for x in range(x1, x2):
            for y in range(y1, y2):
                bitmap[x][y] = 1
        return {
            "bitmap": bitmap,
            "log": log
        }

    def agentIsNearestToTreasure(self):
        log = "HINT 7"
        return {
            "log": log
        }
    
    def rowOrColumnWithTreasure(self):
        bitmap = [[0]*self.W for _ in range(self.H)]
        isRow = random.randint(0, 1)
        log = "HINT 8 "
        if isRow:
            row = random.randint(0, self.H-1)
            for col in range(self.W):
                bitmap[row][col] = 1
            log += "{} {}".format(isRow, row)
        else:
            col = random.randint(0, self.W-1)
            for row in range(self.H):
                bitmap[row][col] = 1   
            log += "{} {}".format(isRow, col)  
        return {
            "bitmap": bitmap,
            "log": log
        }
    
    def rowOrColumnWithoutTreasure(self):
        bitmap = [[1]*self.W for _ in range(self.H)]
        isRow = random.randint(0, 1)
        log = "HINT 9 "
        if isRow:
            row = random.randint(0, self.H-1)
            for col in range(self.W):
                bitmap[row][col] = 0
            log += "{} {}".format(isRow, row)
        else:
            col = random.randint(0, self.W-1)
            for row in range(self.H):
                bitmap[row][col] = 1   
            log += "{} {}".format(isRow, col)  
        return {
            "bitmap": bitmap,
            "log": log
        }
    
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

    def twoRegionBoundaryWithTreasure(self):
        bitmap = [[0]*self.W for _ in range(self.H)]
        regA = random.randint(1, self.R)
        regB = random.randint(1, self.R)
        log = "HINT 10 {} {}".format(regA, regB)
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
        return {
            "bitmap": bitmap,
            "log": log
        }
    
    def anyRegionBoundaryWithTreasure(self):
        bitmap = [[0]*self.W for _ in range(self.H)]
        log = "HINT 11"
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
        return {
            "bitmap": bitmap,
            "log": log
        }
    
    def seaBoundaryWithTreasure(self):
        bitmap = [[0]*self.W for _ in range(self.H)]
        thickness = random.randint(1, 3)
        log = "HINT 12 {}".format(thickness)
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
        return {
            "bitmap": bitmap,
            "log": log
        }

    def createRandomHint(self):
        rand = random.randint(0, 100)
        normalIndex = [1, 3, 4, 5, 6, 9, 10, 11, 12]
        rareIndex = [2, 8]        
        if (rand > 85):
            type = rareIndex[random.randint(0, len(rareIndex)-1)]
        else:
            type = normalIndex[random.randint(0, len(normalIndex)-1)]

        if (type == 1):
            return self.tilesWithoutTreasure()
        if (type == 2):
            return self.tilesWithTreasure()
        if (type == 3):
            return self.regionsWithTreasure()
        if (type == 4):
            return self.regionsWithoutTreasure()
        if (type == 5):
            return self.bigRecWithoutTreasure()
        if (type == 6):
            return self.smallRecWithTreasure()
        if (type == 7):
            return self.agentIsNearestToTreasure()
        if (type == 8):
            return self.rowOrColumnWithTreasure()
        if (type == 9):
            return self.rowOrColumnWithoutTreasure()
        if (type == 10):
            return self.twoRegionBoundaryWithTreasure()
        if (type == 11):
            return self.anyRegionBoundaryWithTreasure()
        if (type == 12):
            return self.seaBoundaryWithTreasure()


class Game:
    def __init__(self):
        self.log = []
        self.turn = 0
        self.hints = []

    def initialize(self, input_path):
        with open(input_path) as file:
            dimensions = list(map(int, file.readline().strip().split(" ")))
            self.W = dimensions[0]
            self.H = dimensions[1]
            self.r = int(file.readline().strip())
            self.f = int(file.readline().strip())
            self.R = int(file.readline().strip())
            treasureCoord = list(map(int, file.readline().strip().split(" ")))
            self.T = Coordination(treasureCoord[0], treasureCoord[1])
            self.gameMap = []
            self.mountainCoords = []
            self.prisonCoords = []
            possiblePlayerSpawnCoords = []
            self.bitMap = [[1]*self.W for _ in range(self.H)]
            for row in range(self.H):
                rawRow = file.readline().replace(" ", "").split(";")
                self.gameMap.append([])
                self.bitMap.append([])
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
            for row in range(self.H):
                for col in range(self.W):
                    if (self.gameMap[row][col] == 0):
                        self.bitMap[row][col] = 0
            self.playerCoord = possiblePlayerSpawnCoords[random.randint(0, len(possiblePlayerSpawnCoords) - 1)]
            self.pirateCoord = self.prisonCoords[random.randint(0, len(self.prisonCoords) - 1)]
            self.hintFactory = HintFactory(self.W, self.H, self.R, self.gameMap)
    
    def output(self, output_path): 
        with open(output_path, "w") as file:
            print(len(self.log), file=file)
            print(self.log[-1].split(" ")[-1], file=file)
            for log in self.log:
                print(log, file=file) 
    
    def endCondition(self):

        if (self.pirateCoord == self.T):
            self.log.append("ENDG LOSE")
            return True
        if (self.playerCoord == self.T):
            self.log.append("ENDG WIN")
            return True
        return False
    
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

    def directionToGo(self):
        total = [0, 0, 0, 0] #Bottom top right left
        direction = [Coordination(1, 0), Coordination(-1, 0), Coordination(0, 1), Coordination(0, -1)]
        for row in range(0, self.H):
            for col in range(0, self.W):
                if (self.bitMap[row][col]):
                    total[0] += int(row > self.playerCoord.x)
                    total[1] += int(row < self.pirateCoord.x)
                    total[2] += int(col > self.playerCoord.y)
                    total[3] += int(col < self.playerCoord.y)
        maxx = max(total[0], total[1], total[2], total[3])
        for index in range(4):
            if (maxx == total[index]):
                return direction[index]

    def smallScan(self):
        optimalDirection = self.directionToGo()
        self.playerCoord.x = self.boundX(self.playerCoord.x + optimalDirection.x * 2)
        self.playerCoord.y = self.boundY(self.playerCoord.y + optimalDirection.y * 2)
        self.log.append("ASSN {}".format(self.pirateCoord))
        deltaX = [0, 0, 0, 1, -1, 1, -1, 1, -1]
        deltaY = [0, 1, -1, 0, 0, 1, -1, -1, 1]
        for index in range(len(deltaX)):
            x = self.boundX(self.playerCoord.x + deltaX[index])
            y = self.boundX(self.playerCoord.y + deltaY[index])
            if (Coordination(x, y) == self.T):
                self.log.append("ENDG WIN")
                return True
            else:
                self.bitMap[x][y] = 0
        return False
    
    def noScan(self):
        optimalDirection = self.directionToGo()
        savedPlayerCoord = Coordination(self.playerCoord.x, self.playerCoord.y)
        self.playerCoord.x = self.boundX(self.playerCoord.x + optimalDirection.x * 4)
        self.playerCoord.y = self.boundY(self.playerCoord.y + optimalDirection.y * 4)
        self.log.append("ANSN {}".format(self.playerCoord))
        for index in range(1, 5):
            newCoord = Coordination(self.boundX(savedPlayerCoord.x +  optimalDirection.x * index), self.boundY(savedPlayerCoord.y + optimalDirection.y * index))
            if (newCoord == self.T):
                self.log.append("ENDG WIN")
                return True
            else:
                self.bitMap[newCoord.x][newCoord.y] = 0
        return False

    
    def agentNextMove(self): 
        optimalDirection = self.directionToGo()
        candidatePlayerCoord = Coordination(self.playerCoord.x, self.playerCoord.y)
        candidatePlayerCoord.x = self.boundX(candidatePlayerCoord.x + optimalDirection.x * 2)
        candidatePlayerCoord.y = self.boundY(candidatePlayerCoord.y + optimalDirection.y * 2)
        deltaX = [0, 0, 0, 1, -1, 1, -1, 1, -1]
        deltaY = [0, 1, -1, 0, 0, 1, -1, -1, 1]
        for index in range(len(deltaX)):
            x = self.boundX(self.playerCoord.x + deltaX[index])
            y = self.boundX(self.playerCoord.y + deltaY[index])
            if (self.bitMap[x][y] == 1):
                return self.smallScan()
        return self.noScan()

    def largeScan(self):
        self.log.append("ALSN") 
        deltaX = [0, 0, 0, 1, -1, 1, -1, 1, -1, 0, 0, 2, -2, 1, 1, -1, -1, 2, 2, -2, -2, 2, 2, -2, -2]
        deltaY = [0, 1, -1, 0, 0, 1, -1, -1, 1, 2, -2, 0, 0, 2, -2, 2, -2, 1, -1, 1, -1, 2, -2, 2, -2]
        for index in range(len(deltaX)):
            x = self.boundX(self.playerCoord.x + deltaX[index])
            y = self.boundX(self.playerCoord.y + deltaY[index])
            if (Coordination(x, y) == self.T):
                self.log.append("ENDG WIN")
                return True
            else:
                self.bitMap[x][y] = 0
        return False

    def verifyBitmap(self, hintBitmap):
        if hintBitmap[self.T.x][self.T.y] == 0:
            self.log.append("SYST 0")
            return False
        for row in range(self.H):
            for col in range(self.W):
                if (hintBitmap[row][col] == 0):
                    self.bitMap[row][col] = 0
        self.log.append("SYST 1")
        return True

    def boundMove(self, rawStep, step):
        if (rawStep > step):
            return step
        if (rawStep < -step):
            return -step
        return rawStep

    def simulate(self):
        self.log.append("ASPW {}".format(self.playerCoord))
        while (not self.endCondition()):
            self.log.append("TURN {}".format(self.turn + 1)) # TURN SEQUENCE NUMBER
            if (self.turn == self.r):
                self.log.append("RVEL {}".format(self.pirateCoord)) # PIRATE REVEALS COORD
            if (self.turn == self.R):
                self.log.append("FREE") # PIRATE IS FREE
            if (self.turn >= self.R):
                if (self.pirateCoord.x != self.T.x):
                    self.pirateCoord.x += self.boundMove(self.T.x - self.pirateCoord.x, 2)
                elif (self.pirateCoord.y != self.T.y):
                    self.pirateCoord.x += self.boundMove(self.T.y - self.pirateCoord.y, 2)
                self.log.append("PMOV {}".format(self.pirateCoord))
            if (self.turn == 0):
                self.hints.append(self.hintFactory.firstHint())
                self.log.append(self.hints[-1]["log"]) # HINT
                if (self.largeScan()):
                    break
            else:
                self.hints.append(self.hintFactory.createRandomHint())
                self.log.append(self.hints[-1]["log"])
                self.log.append("VRFY {}".format(len(self.hints)))
                self.verifyBitmap(self.hints[-1]["bitmap"])
                if (self.agentNextMove()):
                    break
            self.turn += 1
                    

def main(input_path, output_path):
    game = Game()
    game.initialize(input_path)
    game.simulate()
    game.output(output_path)

if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print('usage:\tmain.py <input_file> <output_file>')
        sys.exit(0)
    main(sys.argv[1],sys.argv[2])