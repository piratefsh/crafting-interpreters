from .Expr import Expr

class Binary(Expr):
    def __init__(self, left, operator, right):
      self.left = left
      self.operator = operator
      self.right = right
