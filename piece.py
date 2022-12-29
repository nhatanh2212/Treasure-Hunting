import os
class Piece:

    def __init__(self, name, value,visited = False, texture = None, texture_rect=None):
        self.name = name
        self.visited = visited
        self.value = value
        self.move = []
        self.moved = False 
        self.texture = texture
        if(name != "Normal" and name != "Water"):
            self.set_texture()
        self.texture_rect = texture_rect
        
    def set_texture(self):
        self.texture = os.path.join(
            f'images/{self.name}.png')  

    def add_move(self, move): 
        self.move.append(move) 


class Monster(Piece):
    def __init__(self):
        Piece.__init__(self, 'Monster', 1)

    
   
    
class Player(Piece):
    def __init__(self):
        Piece.__init__(self, 'Player', 0)
    


