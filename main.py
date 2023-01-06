import sys
import os
import random
from coord import *
import const
from visualization import *

NORTH = Coordination(-1, 0)
SOUTH = Coordination(1, 0)
WEST = Coordination(0, -1)
EAST = Coordination(0, 1)

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
    
    def tilesWithoutTreasure(self):
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
            log += "{} ".format(regions[-1])
        for row in range(self.H):
            for col in range(self.W):
                if (self.gameMap[row][col] in regions):
                    bitmap[row][col] = 0
        return {
            "bitmap": bitmap,
            "log": log
        }

    def bigRecWithTreasure(self):
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

    def smallRecWithoutTreasure(self):
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
        if (rand > 75):
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
            return self.bigRecWithTreasure()
        if (type == 6):
            return self.smallRecWithoutTreasure()
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
            self.obstacle = [[False]*self.W for _ in range(self.H)]
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
                            self.obstacle[row][col] = True
                            self.mountainCoords.append(Coordination(row, col))
                        elif (rawRow[col][-1] == 'P'):
                            self.prisonCoords.append(Coordination(row, col))
                    else:
                        self.gameMap[-1].append(int(rawRow[col]))
                        if (int(rawRow[col]) != 0):
                            possiblePlayerSpawnCoords.append(Coordination(row, col))
                        else:
                            self.obstacle[row][col] = True
            for row in range(self.H):
                for col in range(self.W):
                    if (self.gameMap[row][col] == 0):
                        self.bitMap[row][col] = 0
            self.playerCoord = possiblePlayerSpawnCoords[random.randint(0, len(possiblePlayerSpawnCoords) - 1)]
            self.pirateCoord = self.prisonCoords[random.randint(0, len(self.prisonCoords) - 1)]
            self.hintFactory = HintFactory(self.W, self.H, self.R, self.gameMap)
            self.calculatePiratePath()
    
    def output(self, output_path): 
        with open(output_path, "w") as file:
            print(len(self.log), file=file)
            print(self.log[-1].split(" ")[-1], file=file)
            for log in self.log:
                print(log, file=file) 

    def calculatePiratePath(self):
        deltaX = [0, 0, 1, -1, 0, 0, 2, -2]
        deltaY = [1, -1, 0, 0, 2, -2, 0, 0]
        self.piratePath = []
        queue = []
        visited = [[None]*self.W for _ in range(self.H)]
        visited[self.pirateCoord.x][self.pirateCoord.y] = None
        queue.append(Coordination(self.pirateCoord. x, self.pirateCoord.y))
        while (len(queue)):
            at = queue.pop(0)
            for index in range(len(deltaX)):
                to = Coordination(at.x + deltaX[index], at.y + deltaY[index])
                if (to.x < 0 or to.x >= self.H or to.y < 0  or to.y >= self.W):
                    continue
                if (self.obstacle[to.x][to.y] == True):
                    continue
                if (not visited[to.x][to.y] is None):
                    continue
                queue.append(to)
                visited[to.x][to.y] = Coordination(at.x, at.y)

        if (visited[self.T.x][self.T.y] is None):
            return

        self.piratePath.append(self.T)
        cur = self.T
        while (not (visited[cur.x][cur.y] is None)) and (not (visited[cur.x][cur.y] == self.pirateCoord)):
            self.piratePath.append(visited[cur.x][cur.y])
            cur = visited[cur.x][cur.y]

    def endCondition(self):
        if (len(self.log) and self.log[-1].split(" ")[0] == "ENDG"):
            return True
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

    def directionsDescSortedByPotential(self):
        total = [(0, SOUTH), (0, NORTH), (0, EAST), (0, WEST)]
        #Bottom top right left
        playerPrimaryDiagonal =  self.playerCoord.y - self.playerCoord.x
        playerSecondaryDiagonal = self.playerCoord.x + self.playerCoord.y
        for row in range(0, self.H):
            for col in range(0, self.W):
                if (self.bitMap[row][col]):
                    primaryDiagonal = col - row
                    secondaryDiagonal = row + col
                    isNorth = row <= self.playerCoord.x and primaryDiagonal >= playerPrimaryDiagonal and secondaryDiagonal <= playerSecondaryDiagonal
                    isSouth = row >= self.playerCoord.x and primaryDiagonal <= playerPrimaryDiagonal and secondaryDiagonal >= playerSecondaryDiagonal
                    isEast = col >= self.playerCoord.y and primaryDiagonal >= playerPrimaryDiagonal and secondaryDiagonal >= playerSecondaryDiagonal
                    isWest = col <= self.playerCoord.y and primaryDiagonal <= playerPrimaryDiagonal and secondaryDiagonal <= playerSecondaryDiagonal
                    total[0] = (total[0][0] + int(isSouth), total[0][1])
                    total[1] = (total[1][0] + int(isNorth), total[1][1])
                    total[2] = (total[2][0] + int(isEast), total[2][1])
                    total[3] = (total[3][0] + int(isWest), total[3][1])
        total = sorted(total, key=lambda x:x[0])
        total.reverse()
        return [total[0][1], total[1][1], total[2][1], total[3][1]]

    def stepAndSmallScan(self, step, direction):
        self.log.append("ASSN {} {}".format(step, direction))

        self.playerCoord.x += step * direction.x
        self.playerCoord.y += step * direction.y

        deltaX = [0, 0, 0, 1, -1, 1, -1, 1, -1]
        deltaY = [0, 1, -1, 0, 0, 1, -1, -1, 1]
        for index in range(len(deltaX)):
            x = self.boundX(self.playerCoord.x + deltaX[index])
            y = self.boundX(self.playerCoord.y + deltaY[index])
            if (Coordination(x, y) == self.T):
                self.log.append("ENDG WIN")
                return
            else:
                self.bitMap[x][y] = 0
    
    def stepAndNoScan(self, step, direction):
        self.log.append("ANSN {} {}".format(step, direction))
        for _ in range(step):
            self.playerCoord.x += direction.x
            self.playerCoord.y += direction.y
            if (self.playerCoord == self.T):
                self.log.append("ENDG WIN")
                return 
            else:
                self.bitMap[self.playerCoord.x][self.playerCoord.y] = 0
    

    def pirateNextMove(self):
        savedPirateCoord = Coordination(self.pirateCoord.x, self.pirateCoord.y)
        if (len(self.piratePath)):
            self.pirateCoord = self.piratePath.pop()
        self.log.append("PMOV {}".format(self.pirateCoord))
        self.bitMap[self.pirateCoord.x][self.pirateCoord.y] = 0
        if (abs(self.pirateCoord.x - savedPirateCoord.x) + abs(self.pirateCoord.y - savedPirateCoord.y)) == 2:
            self.bitMap[(self.pirateCoord.x + savedPirateCoord.x) //2][(self.pirateCoord.y + savedPirateCoord.y) // 2] = 0
        if (self.pirateCoord == self.T):
            self.log.append("ENDG LOSE")
            return True
        return False
    
    def processAgentNextMove(self): 
        optimalDirection = self.directionsDescSortedByPotential()
        nextDirection = Coordination(0, 0)
        for direction in optimalDirection:
            candidatePlayerCoord = Coordination(self.playerCoord.x + direction.x, self.playerCoord.y + direction.y)
            if (candidatePlayerCoord.x < 0 or candidatePlayerCoord.x >= self.H or candidatePlayerCoord.y < 0 or candidatePlayerCoord.y >= self.W):
                continue
            if (self.obstacle[candidatePlayerCoord.x][candidatePlayerCoord.y] == False):
                nextDirection = direction
                break

        if (nextDirection == Coordination(0, 0)):
            return self.largeScan()
        
        greatestStepPossible = 1
        for index in range(2, 5):
            test_coord = Coordination(self.playerCoord.x + nextDirection.x * index, self.playerCoord.y + nextDirection.y * index)
            if (test_coord.x < 0 or test_coord.x >= self.H or test_coord.y < 0 or test_coord.y >= self.W):
                break
            if (self.obstacle[test_coord.x][test_coord.y]):
                break
            greatestStepPossible = index
        
        if (greatestStepPossible <= 2):
            return self.stepAndSmallScan(greatestStepPossible, nextDirection)
        
        deltaX = [0, 0, 0, 1, -1, 1, -1, 1, -1]
        deltaY = [0, 1, -1, 0, 0, 1, -1, -1, 1]
        for index in range(len(deltaX)):
            x = self.boundX(self.playerCoord.x + deltaX[index])
            y = self.boundX(self.playerCoord.y + deltaY[index])
            if (self.bitMap[x][y] == 1):
                return self.stepAndSmallScan(2, nextDirection)
        return self.stepAndNoScan(greatestStepPossible, nextDirection)

    def agentNextMove(self):
        if (self.turn == 0):
            self.hints.append(self.hintFactory.firstHint())
            self.log.append(self.hints[-1]["log"]) # HINT
            self.largeScan()
            if (self.endCondition()):
                return True
            self.processAgentNextMove()
        else:
            self.hints.append(self.hintFactory.createRandomHint())
            self.log.append(self.hints[-1]["log"])
            self.log.append("VRFY {}".format(len(self.hints)))
            self.verifyBitmap(self.hints[-1]["bitmap"])
            self.processAgentNextMove()
        return self.endCondition()

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
            for row in range(self.H):
                for col in range(self.W):
                    if (hintBitmap[row][col] == 1):
                        self.bitMap[row][col] = 0
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
                self.bitMap[self.pirateCoord.x][self.pirateCoord.y] = 0
            if (self.turn == self.R):
                self.log.append("FREE") # PIRATE IS FREE
            if (self.turn >= self.R):
                if (self.pirateNextMove()):
                    break
            if (self.agentNextMove()):
                break
            self.turn += 1
                    

def main(input_path, output_path):
    game = Game()
    game.initialize(input_path)
    game.simulate()
    game.output(output_path)
    visualizer = Visualizer()
    visualizer.initialize(input_path)
    visualizer.simulate(output_path)

if __name__ == '__main__':
    if (len(sys.argv) < 3):
        print('usage:\tmain.py <input_file> <log_file> <block_size>')
        sys.exit(0)
        if (len(sys.argv) > 3):
            const.SIZE = sys.argv[3] 
    main(sys.argv[1],sys.argv[2])