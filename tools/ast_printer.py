from ast.Expr import Visitor, Expr


class Printer(Visitor):
    def __init__(self):
        pass

    def print(self, expr):
        return expr.accept(self)

    def paren(self, *expressions):
        breakpoint()
        tokens = " ".join([self.print(expr) if isinstance(expr, Expr) else str(expr) for expr in expressions])
        return "({})".format(tokens)

    def visitBinaryExpr(self, expr):
        return self.paren(expr.operator.lexeme, expr.left, expr.right)

    def visitGroupingExpr(self, expr):
        return self.paren("group", expr.expression)

    def visitLiteralExpr(self, expr):
        return "{}".format(expr.value)

    def visitUnaryExpr(self, expr):
        return self.paren(expr.operator.lexeme, expr.right)
