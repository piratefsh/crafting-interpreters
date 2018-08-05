from TokenTypes import TokenTypes
from Token import Token
from Lox import Lox
import pdb


class Scanner:
    def __init__(self, src):
        self.src = src
        self.tokens = []
        self.curr_idx = -1
        self.line = 0

    def scan_token(self):
        char = self.consume()
        if char == TokenTypes.LEFT_PAREN.value:
            self.add_token(TokenTypes.LEFT_PAREN)
        elif char == TokenTypes.RIGHT_PAREN.value:
            self.add_token(TokenTypes.RIGHT_PAREN)
        elif char == TokenTypes.LEFT_BRACE.value:
            self.add_token(TokenTypes.LEFT_BRACE)
        elif char == TokenTypes.RIGHT_BRACE.value:
            self.add_token(TokenTypes.RIGHT_BRACE)
        elif char == TokenTypes.COMMA.value:
            self.add_token(TokenTypes.COMMA)
        elif char == TokenTypes.DOT.value:
            self.add_token(TokenTypes.DOT)
        elif char == TokenTypes.MINUS.value:
            self.add_token(TokenTypes.MINUS)
        elif char == TokenTypes.PLUS.value:
            self.add_token(TokenTypes.PLUS)
        elif char == TokenTypes.SEMICOLON.value:
            self.add_token(TokenTypes.SEMICOLON)
        elif char == TokenTypes.STAR.value:
            self.add_token(TokenTypes.STAR)
        elif char == TokenTypes.SLASH.value:
            self.add_token(TokenTypes.SLASH)
        elif self.is_nextline(char):
            self.line = self.line + 1
        elif self.is_whitespace(char):
            pass
        else:
            Lox.error(self.line, "Unknown token %s" % char)

    def add_token(self, ttype, tvalue=None):
        # TODO: literal
        literal = None

        value = tvalue if tvalue is not None else ttype.value

        self.tokens.append(Token(ttype, value, literal, self.line))

    def consume(self):
        self.curr_idx = self.curr_idx + 1
        return self.src[self.curr_idx]

    def is_nextline(self, c):
        return c == '\n'

    def is_whitespace(self, c):
        return c == '\t' or c == ' ' or c == '\r'

    def scan(self):
        while(self.curr_idx < len(self.src) - 1):
            self.scan_token()
