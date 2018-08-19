# Recursive descent parser
from TokenTypes import TokenTypes
import ast.Expr as Expr


class Parser():
    def __init__(self, tokens, lox_instance):
        self.tokens = tokens
        self.curr_idx = 0
        self.lox = lox_instance

    def parse(self):
        return self.expression()

    def expression(self):
        return self.equality()

    def equality(self):
        expr = self.comparison()

        while(self.match(TokenTypes.BANG_EQUAL, TokenTypes.EQUAL_EQUAL)):
            operator = self.previous()
            right = self.comparison()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def comparison(self):
        expr = self.addition()

        while(self.match(TokenTypes.GREATER,
                         TokenTypes.GREATER_EQUAL,
                         TokenTypes.LESS,
                         TokenTypes.LESS_EQUAL,
                         TokenTypes.GREATER,
                         TokenTypes.GREATER_EQUAL)):
            operator = self.previous()
            right = self.addition()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def addition(self):
        expr = self.multiplication()

        while(self.match(TokenTypes.MINUS,
                         TokenTypes.PLUS)):
            operator = self.previous()
            right = self.multiplication()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def multiplication(self):
        expr = self.unary()

        while(self.match(TokenTypes.SLASH,
                         TokenTypes.STAR)):
            operator = self.previous()
            right = self.unary()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def unary(self):
        expr = self.primary()

        while(self.match(TokenTypes.BANG, TokenTypes.MINUS)):
            operator = self.previous()
            expr = Expr.Unary(operator, self.unary())

        return expr

    def primary(self):
        breakpoint()
        if(self.match(TokenTypes.FALSE,
                      TokenTypes.TRUE,
                      TokenTypes.NIL,
                      TokenTypes.STRING,
                      TokenTypes.NUMBER)):
            return Expr.Literal(self.previous().literal)

        if (self.match(TokenTypes.LEFT_PAREN)):
            expr = self.expression()
            self.consume(TokenTypes.RIGHT_PAREN)
            return Expr.Grouping(expr)

        token = self.previous()
        self.lox.error(token.line_number, 'Unexpected token {}: `{}`'.format(token.type, token.lexeme))

    #  return true and advance if next token is one of types
    def match(self, *types):
        for t in types:
            if self.check(t):
                self.advance()
                return True

        return False

    def check(self, ttype):
        if self.is_at_end():
            return False
        return self.tokens[self.curr_idx].type == ttype

    def advance(self):
        self.curr_idx = self.curr_idx + 1
        return self.previous()

    def previous(self):
        return self.tokens[self.curr_idx - 1]

    def is_at_end(self):
        return self.curr_idx >= len(self.tokens)

    def peek(self):
        return self.tokens[self.curr_idx]

    def consume(self, ttype):
        if self.check(ttype):
            self.match(ttype)
        else:
            self.lox.error(self.previous().line_number,
                      'Expected `%s` token' % ttype.value)

    # discard tokens until start of a new statement
    def synchronize(self):
      advance()

      while(not self.is_at_end()):
        # if just ended a statement
        if self.previous().type == TokenTypes.SEMICOLON:
          return

        # if starting a new statement
        ttype = self.peek().type
        if ttype == TokenTypes.CLASS or \
          ttype == TokenTypes.FUN or \
          ttype == TokenTypes.VAR or \
          ttype == TokenTypes.FOR or \
          ttype == TokenTypes.IF or \
          ttype == TokenTypes.WHILE or \
          ttype == TokenTypes.PRINT or \
          ttype == TokenTypes.RETURN:
          return

        self.advance()