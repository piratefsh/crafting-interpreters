from .Expr import Expr

class Unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right
    def accept(visitor):
        visitor.visitUnaryExpr()
