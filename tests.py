#!/usr/local/bin/python3

from Scanner import Scanner
from TokenTypes import TokenTypes
from Token import Token
from os import environ


def scan(src):
    s = Scanner(src)
    s.scan()
    return s


def b():
    breakpoint()


def run():
    assert(scan('()').tokens == [Token(type=TokenTypes.LEFT_PAREN, lexeme='(', literal=None, line_number=0),
                                 Token(type=TokenTypes.RIGHT_PAREN, lexeme=')', literal=None, line_number=0)])

    assert(scan('( )').tokens == [Token(type=TokenTypes.LEFT_PAREN, lexeme='(', literal=None, line_number=0),
                                  Token(type=TokenTypes.RIGHT_PAREN, lexeme=')', literal=None, line_number=0)])

    assert(scan('  ( )  ').tokens == [Token(type=TokenTypes.LEFT_PAREN, lexeme='(', literal=None, line_number=0),
                                      Token(type=TokenTypes.RIGHT_PAREN, lexeme=')', literal=None, line_number=0)])

    assert(scan("{}").tokens == [Token(type=TokenTypes.LEFT_BRACE, lexeme='{', literal=None, line_number=0),
                                 Token(type=TokenTypes.RIGHT_BRACE, lexeme='}', literal=None, line_number=0)])
    assert(scan("""
      // hi i am comment
      ()
      """).tokens == [Token(type=TokenTypes.LEFT_PAREN, lexeme='(', literal=None, line_number=1),
                      Token(type=TokenTypes.RIGHT_PAREN, lexeme=')', literal=None, line_number=1)])
    assert(scan(" * ").tokens == [
        Token(type=TokenTypes.STAR, lexeme='*', literal=None, line_number=0)])

    assert(scan("/ * ").tokens == [
        Token(type=TokenTypes.SLASH, lexeme='/', literal=None, line_number=0),
        Token(type=TokenTypes.STAR, lexeme='*', literal=None, line_number=0)])

    assert(scan(", . : - + / * ").tokens == [
        Token(type=TokenTypes.COMMA, lexeme=',', literal=None, line_number=0),
        Token(type=TokenTypes.DOT, lexeme='.', literal=None, line_number=0),
        Token(type=TokenTypes.SEMICOLON, lexeme=':',
              literal=None, line_number=0),
        Token(type=TokenTypes.MINUS, lexeme='-', literal=None, line_number=0),
        Token(type=TokenTypes.PLUS, lexeme='+', literal=None, line_number=0),
        Token(type=TokenTypes.SLASH, lexeme='/', literal=None, line_number=0),
        Token(type=TokenTypes.STAR, lexeme='*', literal=None, line_number=0)])

    assert(scan("9").tokens == [
        Token(type=TokenTypes.NUMBER, lexeme='9', literal=9, line_number=0)])

    assert(scan("96").tokens == [
        Token(type=TokenTypes.NUMBER, lexeme='96', literal=96, line_number=0)])

    assert(scan('(9)').tokens == [
        Token(type=TokenTypes.LEFT_PAREN,
              lexeme='(', literal=None, line_number=0),
        Token(type=TokenTypes.NUMBER, lexeme='9', literal=9, line_number=0),
        Token(type=TokenTypes.RIGHT_PAREN, lexeme=')', literal=None, line_number=0)])

    assert(scan("96.7").tokens == [
        Token(type=TokenTypes.NUMBER, lexeme='96.7', literal=96.7, line_number=0)])

    assert(scan("1.111").tokens == [
        Token(type=TokenTypes.NUMBER, lexeme='1.111', literal=1.111, line_number=0)])

    assert(scan("1.2.3").tokens == [
        Token(type=TokenTypes.NUMBER, lexeme='1.2', literal=1.2, line_number=0),
        Token(type=TokenTypes.DOT, lexeme='.', literal=None, line_number=0),
        Token(type=TokenTypes.NUMBER, lexeme='3', literal=3, line_number=0),
    ])

    assert(scan("1.").tokens == [
        Token(type=TokenTypes.NUMBER, lexeme='1', literal=1, line_number=0),
        Token(type=TokenTypes.DOT, lexeme='.', literal=None, line_number=0),
    ])

    assert(scan('"a"').tokens == [
        Token(type=TokenTypes.STRING, lexeme='a', literal='a', line_number=0)])

    assert(scan('"abc"').tokens == [
        Token(type=TokenTypes.STRING, lexeme='abc', literal='abc', line_number=0)])

    assert(scan('''"abc
def"''').tokens == [
        Token(type=TokenTypes.STRING, lexeme='abc\ndef',
              literal='abc\ndef', line_number=0),
    ])

    assert(scan('!').tokens == [
        Token(type=TokenTypes.BANG, lexeme='!', literal=None, line_number=0)])
    assert(scan('!=').tokens == [
        Token(type=TokenTypes.BANG_EQUAL, lexeme='!=', literal=None, line_number=0)])

    assert(scan('<').tokens == [
        Token(type=TokenTypes.LESS, lexeme='<', literal=None, line_number=0)])
    assert(scan('<=').tokens == [
        Token(type=TokenTypes.LESS_EQUAL, lexeme='<=', literal=None, line_number=0)])

    assert(scan('>').tokens == [
        Token(type=TokenTypes.GREATER, lexeme='>', literal=None, line_number=0)])
    assert(scan('>=').tokens == [
        Token(type=TokenTypes.GREATER_EQUAL, lexeme='>=', literal=None, line_number=0)])

    assert(scan('=').tokens == [
        Token(type=TokenTypes.EQUAL, lexeme='=', literal=None, line_number=0)])
    assert(scan('==').tokens == [
        Token(type=TokenTypes.EQUAL_EQUAL, lexeme='==', literal=None, line_number=0)])

    b()
    assert(scan('varietal').tokens == [
        Token(type=TokenTypes.IDENTIFIER, lexeme='varietal', literal=None, line_number=0)])
    assert(scan('var').tokens == [
        Token(type=TokenTypes.VAR, lexeme='var', literal=None, line_number=0)])
    assert(scan('print').tokens == [
        Token(type=TokenTypes.PRINT, lexeme='print', literal=None, line_number=0)])
    assert(scan('true').tokens == [
        Token(type=TokenTypes.TRUE, lexeme='true', literal=True, line_number=0)])
    assert(scan('false').tokens == [
        Token(type=TokenTypes.FALSE, lexeme='false', literal=False, line_number=0)])

    print('tests pass')

    # scan("""

    #   ~
    # """)


if __name__ == '__main__':
    run()
