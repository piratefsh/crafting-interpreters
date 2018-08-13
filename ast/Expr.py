class Expr():
    def accept(visitor):
        return

class Visitor():
    def __init__(self):
        pass

    def visitBinaryExpr(expr):
        return

    def visitGroupingExpr(expr):
        return

    def visitLiteralExpr(expr):
        return

    def visitUnaryExpr(expr):
        return


class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    def accept(self, visitor):
        return visitor.visitBinaryExpr(self)


class Grouping(Expr):
    def __init__(self, expression):
        self.expression = expression
    def accept(self, visitor):
        return visitor.visitGroupingExpr(self)


class Literal(Expr):
    def __init__(self, value):
        self.value = value
    def accept(self, visitor):
        return visitor.visitLiteralExpr(self)


class Unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right
    def accept(self, visitor):
        return visitor.visitUnaryExpr(self)
