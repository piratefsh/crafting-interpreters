from ast.Expr import Visitor
from .TokenTypes import TokenTypes

class Interpreter(Visitor):
    def __init__(self):
        pass

    def evaluate(self, expr):
        reurn expr.accept(this)

    def visitTernaryExpr(self, expr):
        pass
    def visitBinaryExpr(self, expr):
        pass
    def visitGroupingExpr(self, expr):
        return self.evaluate(expr);

    def visitLiteralExpr(self, expr):
        return expr.value

    def visitUnaryExpr(self, expr):
        operator = expr.operator
        if operator.type ==  TokenTypes.MINUS:
            return -expr.value

        return None