from TokenTypes import TokenTypes
from Token import Token
from Lox import Lox
import pdb


def is_digit(c):
    return c >= '0' and c <= '9'


def is_dot(c):
    return c == TokenTypes.DOT.value


def is_nextline(c):
    return c == '\n'


def is_whitespace(c):
    return c == '\t' or c == ' ' or c == '\r'


def is_quotemark(c):
    return c == '"'


class Scanner:
    def __init__(self, src):
        self.src = src
        self.tokens = []
        self.curr_idx = -1
        self.line = 0

    def scan_token(self):
        char = self.consume()
        # pdb.set_trace()
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

        elif char == TokenTypes.BANG.value:
            self.add_token(TokenTypes.BANG_EQUAL if self.match(
                TokenTypes.EQUAL.value) else TokenTypes.BANG)

        elif char == TokenTypes.LESS.value:
            self.add_token(TokenTypes.LESS_EQUAL if self.match(
                TokenTypes.EQUAL.value) else TokenTypes.LESS)

        elif char == TokenTypes.GREATER.value:
            self.add_token(TokenTypes.GREATER_EQUAL if self.match(
                TokenTypes.EQUAL.value) else TokenTypes.GREATER)

        elif char == TokenTypes.EQUAL.value:
            self.add_token(TokenTypes.EQUAL_EQUAL if self.match(
                TokenTypes.EQUAL.value) else TokenTypes.EQUAL)

        elif char == TokenTypes.SLASH.value:
            # if is comment
            if self.peek() == TokenTypes.SLASH.value:
                # consume comment
                line = self.consume_line()
            else:
                self.add_token(TokenTypes.SLASH)

        elif is_digit(char):
            text, literal = self.number()
            self.add_token(TokenTypes.NUMBER, text, literal)

        elif is_quotemark(char):
            text, literal, start_line = self.string()
            self.add_token(TokenTypes.STRING, text, literal, start_line)

        elif is_nextline(char):
            self.line = self.line + 1

        elif is_whitespace(char):
            pass
        else:
            Lox.error(self.line, "Unknown token %s" % char)

    """ Consumes a series of digits
        e.g 2345b => consumes 2345
        e.g 123.4 => consumes 123
    """

    def consume_number(self):
        while self.has_GREATER():
            # if is number, eat it
            if is_digit(self.peek()):
                self.consume()
            # otherwise, consider end of number
            else:
                break

    def string(self):
        start = self.curr_idx
        start_line = self.line
        while self.has_GREATER() and not is_quotemark(self.peek()):
            char = self.consume()
            if is_nextline(char):
                self.next_line()

        # did not find end of string
        if not self.has_GREATER():
            Lox.error(self.line, "Unterminated string")

        # consume closing quote
        self.consume()

        end = self.curr_idx
        substr = self.src[start + 1:end]
        return substr, substr, start_line

    """ Consumes and returns a number
        can be int or float
        e.g. 123, 1.11
    """

    def number(self):
        start = self.curr_idx

        # consume number chunk
        self.consume_number()

        # if is dot and has number after it
        if is_dot(self.peek()) and is_digit(self.peek(2)):
            self.consume()
            self.consume_number()

        end = self.curr_idx
        substr = self.src[start:end + 1]
        return substr, float(substr)

    def add_token(self, ttype, tvalue=None, literal=None, line=None):
        value = tvalue if tvalue is not None else ttype.value

        line = self.line if line is None else line
        self.tokens.append(Token(ttype, value, literal, line))

    def consume(self):
        if not self.has_GREATER():
            return '\0'
        self.curr_idx = self.curr_idx + 1
        return self.src[self.curr_idx]

    def peek(self, ahead=1):
        if self.curr_idx + ahead > len(self.src) - 1:
            return '\0'
        return self.src[self.curr_idx + ahead]

    """Only consume if matches c
    """

    def match(self, c):
        if c == self.peek():
            return self.consume()
        return False

    def consume_line(self):
        line = ''
        while(self.has_GREATER()):
            char = self.consume()
            line = line + char
            if is_nextline(char):
                return line

        return line

    def next_line(self):
        self.line = self.line + 1

    def has_GREATER(self):
        return self.curr_idx < len(self.src) - 1

    def scan(self):
        while(self.has_GREATER()):
            self.scan_token()
