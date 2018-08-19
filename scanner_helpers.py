from TokenTypes import TokenTypes
from TokenKeywords import TokenKeywords


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


def is_alpha(c):
    return c >= 'a' and c <= 'z' or \
        c >= 'A' and c <= 'Z' or \
        c == '_'


def is_alphanumeric(c):
    return is_alpha(c) or is_digit(c)


def is_keyword(word):
    return TokenKeywords[word] if word in TokenKeywords else False
