class Coordination:
  def __init__(self, x, y):
    self.x = x
    self.y = y
  def __eq__(self, other):
    return self.x == other.x and self.y == other.y
  def __str__(self):
    return "{} {}".format(self.x, self.y)