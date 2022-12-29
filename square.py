class Square:
        def __init__(self,row,col, piece = None):
                self.row = row
                self.col = col
                self.piece = None

        def has_piece(self):
                return self.piece != None
        
        def __eq__(self, other):
                return self.row == other.row and self.col == other.col

        def has_piece(self):
                if self.piece.name != "Normal":
                        return True
                else:
                        return False

        def isempty(self):
                return not self.has_piece()

        def has_team_piece(self,name):
                return self.has_piece() and self.piece.name == name

        def has_enemy_piece(self, name):
                return self.has_piece() and self.piece.name != name

        def isempty_or_enemy(self, name):
                return self.isempty() or self.has_enemy_piece(name)