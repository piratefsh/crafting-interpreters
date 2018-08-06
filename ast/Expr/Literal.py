from .Expr import Expr

class Literal(Expr):
    def __init__(self, value):
      self.value = value
