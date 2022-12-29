import os
class Piece:

    def __init__(self, name, value,visited = False, texture = None):
        self.visited = visited
        self.value = value
        if (value == 0):
            self.color = (230,230,250)
        elif (value == 1):
            self.color = (0,0,255)
        elif (value == 2):
            self.color = (0,0,205)
        elif (value == 3):
            self.color = (0,0,155)
        elif (value == 4):
            self.color = (0,0,105)
        elif (value == 5):
            self.color = (0,0,55)
        else :
           self.color = (0,0,0)
        self.name = name
        self.move = []
        self.moved = False 
        self.texture = texture
        
    def add_move(self, move): 
        self.move.append(move) 

class Mountain(Piece):
    def __init__(self):
        Piece.__init__(self, "Mountain", -1)

class Treasure(Piece):
    def __init__(self):
        Piece.__init__(self, "Treasure",-1)

class Monster(Piece):
    def __init__(self,color):
        Piece.__init__(self, "Monster", 1)

class Water(Piece):
    def __init__(self):
        Piece.__init__(self, "Water", -1)

class Prison(Piece):
    def __init__(self,color):
        Piece.__init__(self, "Prison",1)
    
class Player(Piece):
    def __init__(self,color):
        Piece.__init__(self, "Player", 0)

