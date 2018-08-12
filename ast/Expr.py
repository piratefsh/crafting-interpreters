class Expr():
    def accept(visitor):
        return

class Visitor():
    def __init__(self):
        pass

    def visitBinaryExpr():
        return

    def visitGroupingExpr():
        return

    def visitLiteralExpr():
        return

    def visitUnaryExpr():
        return


class BinaryExpr(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    def accept(visitor):
        visitor.visitBinaryExpr()


class GroupingExpr(Expr):
    def __init__(self, expression):
        self.expression = expression
    def accept(visitor):
        visitor.visitGroupingExpr()


class LiteralExpr(Expr):
    def __init__(self, value):
        self.value = value
    def accept(visitor):
        visitor.visitLiteralExpr()


class UnaryExpr(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right
    def accept(visitor):
        visitor.visitUnaryExpr()
