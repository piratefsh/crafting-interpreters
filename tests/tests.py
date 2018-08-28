#!/usr/local/bin/python3

import sys
sys.path.append('.')

from os import environ
from src.Scanner import Scanner
from src.TokenTypes import TokenTypes
from src.Token import Token
from src.Lox import Lox
from src.Parser import Parser

from src.tools.ast_printer import Printer
import src.ast.Expr as Expr

def scan(src):
    l = Lox()
    s = Scanner(src, l)
    s.scan()
    return s


def assert_exception(call, expected_message):
    try:
        call()
    except Exception as e:
        assert(str(e) == expected_message)


def test_parser():
    l = Lox()
    printer = Printer()
    parserE = Parser([
        Token(type=TokenTypes.BANG_EQUAL, lexeme='!=',
              literal=None, line_number=0)
    ], l)

    assert(parserE.check(TokenTypes.BANG_EQUAL) == True)
    assert(parserE.match(TokenTypes.BANG_EQUAL) == True)

    parser = Parser([
        Token(type=TokenTypes.TRUE, lexeme='true',
              literal=True, line_number=0),
        Token(type=TokenTypes.BANG_EQUAL, lexeme='!=',
              literal=None, line_number=0),
        Token(type=TokenTypes.FALSE, lexeme='false',
              literal=False, line_number=0)
    ], l)
    assert(printer.print(parser.parse()) == '(!= True False)')

    parser = Parser([
        Token(type=TokenTypes.NUMBER, lexeme='2', literal=2, line_number=0),
        Token(type=TokenTypes.STAR, lexeme='*', literal=None, line_number=0),
        Token(type=TokenTypes.NUMBER, lexeme='3', literal=3, line_number=0),
        Token(type=TokenTypes.PLUS, lexeme='+', literal=None, line_number=0),
        Token(type=TokenTypes.NUMBER, lexeme='5', literal=5, line_number=0),
    ], l)

    parser = Parser([
        Token(type=TokenTypes.LEFT_PAREN,
              lexeme='(', literal=None, line_number=0),
        Token(type=TokenTypes.NUMBER, lexeme='5', literal=5, line_number=0),
        Token(type=TokenTypes.RIGHT_PAREN, lexeme=')',
              literal=None, line_number=0),
    ], l)
    # 2 * (3 + 5)
    assert(printer.print(parser.parse()) == '(group 5)')

    parser = Parser([
        Token(type=TokenTypes.NUMBER, lexeme='2', literal=2, line_number=0),
        Token(type=TokenTypes.STAR, lexeme='*', literal=None, line_number=0),
        Token(type=TokenTypes.LEFT_PAREN,
              lexeme='(', literal=None, line_number=0),
        Token(type=TokenTypes.NUMBER, lexeme='3', literal=3, line_number=0),
        Token(type=TokenTypes.PLUS, lexeme='+', literal=None, line_number=0),
        Token(type=TokenTypes.NUMBER, lexeme='5', literal=5, line_number=0),
        Token(type=TokenTypes.RIGHT_PAREN, lexeme=')',
              literal=None, line_number=0),
    ], l)
    # 2 * (3 + 5)

    assert(printer.print(parser.parse()) == '(* 2 (group (+ 3 5)))')

    parser = Parser([
        Token(type=TokenTypes.TRUE, lexeme='true',
              literal=True, line_number=0),
        Token(type=TokenTypes.EQUAL_EQUAL, lexeme='==',
              literal=None, line_number=0),
        Token(type=TokenTypes.LEFT_PAREN,
              lexeme='(', literal=None, line_number=0),
        Token(type=TokenTypes.NUMBER, lexeme='3', literal=3, line_number=0),
        Token(type=TokenTypes.PLUS, lexeme='+', literal=None, line_number=0),
        Token(type=TokenTypes.NUMBER, lexeme='5', literal=5, line_number=0),
        Token(type=TokenTypes.RIGHT_PAREN, lexeme=')',
              literal=None, line_number=0),
        Token(type=TokenTypes.GREATER_EQUAL,
              lexeme='>=', literal=None, line_number=0),
        Token(type=TokenTypes.NUMBER, lexeme='8', literal=8, line_number=0),
    ], l)
    # True == (3 + 5) >= 8
    assert(printer.print(parser.parse()) ==
           '(== True (>= (group (+ 3 5)) 8))')

    parser = Parser([
        Token(type=TokenTypes.LEFT_PAREN,
              lexeme='(', literal=None, line_number=0),
        Token(type=TokenTypes.NUMBER, lexeme='5', literal=5, line_number=0),
    ], l)

    # (5 unbalanced paren
    assert_exception(lambda: printer.print(parser.parse()),
                     '[LOX ERROR] line 0: Expected `)` token')

    # ** Unexpected token
    assert_exception(lambda: printer.print(Parser([
        Token(type=TokenTypes.STAR, lexeme="*", literal=None, line_number=99),
    ], l).expression()),
        '[LOX ERROR] line 99: Unexpected token TokenTypes.STAR: `*`')

    assert_exception(lambda: printer.print(Parser([
        Token(type=TokenTypes.NUMBER, lexeme='3', literal=3, line_number=0),
        Token(type=TokenTypes.PLUS, lexeme='+', literal=None, line_number=0),
        Token(type=TokenTypes.NUMBER, lexeme='2', literal=2, line_number=0),
        Token(type=TokenTypes.STAR, lexeme="*", literal=None, line_number=99),
    ], l).expression()),
        '[LOX ERROR] line 99: Unexpected token TokenTypes.STAR: `*`')

    # comma operator
    parser = Parser([
        Token(type=TokenTypes.NUMBER, lexeme='12', literal=12, line_number=0),
        Token(type=TokenTypes.SLASH, lexeme='/', literal=None, line_number=0),
        Token(type=TokenTypes.NUMBER, lexeme='9', literal=9, line_number=0),
        Token(type=TokenTypes.COMMA, lexeme=',', literal=None, line_number=0),
        Token(type=TokenTypes.NUMBER, lexeme='3', literal=3, line_number=0),
        Token(type=TokenTypes.PLUS, lexeme='+', literal=None, line_number=0),
        Token(type=TokenTypes.NUMBER, lexeme='2', literal=2, line_number=0),
    ], l)
    # 12/9, 3+5
    assert(printer.print(parser.parse()) ==
           '(, (/ 12 9) (+ 3 2))')

    # TODO:comma operator wth function
    # parser = Parser([
    #     Token(type=TokenTypes.IDENTIFIER, lexeme='foo', literal=None, line_number=0),
    #     Token(type=TokenTypes.LEFT_PAREN, lexeme='(', literal=None, line_number=0),
    #     Token(type=TokenTypes.NUMBER, lexeme='9', literal=9, line_number=0),
    #     Token(type=TokenTypes.COMMA, lexeme=',', literal=None, line_number=0),
    #     Token(type=TokenTypes.NUMBER, lexeme='3', literal=3, line_number=0),
    #     Token(type=TokenTypes.RIGHT_PAREN, lexeme=')', literal=None, line_number=0),
    # ], l)
    # assert(printer.print(parser.parse()) ==
    #        '(foo 9 3)')

    # ternary operator
    # a == b ? 0 : 1
    parser = Parser([
        Token(type=TokenTypes.NUMBER, lexeme='9', literal=9, line_number=0),
        Token(type=TokenTypes.EQUAL_EQUAL, lexeme='==', literal=None, line_number=0),
        Token(type=TokenTypes.NUMBER, lexeme='3', literal=3, line_number=0),
        Token(type=TokenTypes.QUESTION_MARK, lexeme='?', literal=None, line_number=0),
        Token(type=TokenTypes.NUMBER, lexeme='0', literal=0, line_number=0),
        Token(type=TokenTypes.COLON, lexeme=':', literal=None, line_number=0),
        Token(type=TokenTypes.NUMBER, lexeme='1', literal=1, line_number=0),
    ], l)
    # 12/9, 3+5
    assert(printer.print(parser.parse()) ==
           '(?: (== 9 3) 0 1)')

    parser = Parser([
        Token(type=TokenTypes.NUMBER, lexeme='9', literal=9, line_number=0),
        Token(type=TokenTypes.MINUS, lexeme='-', literal=None, line_number=0),
        Token(type=TokenTypes.NUMBER, lexeme='3', literal=3, line_number=0),
    ], l)
    assert(printer.print(parser.parse()) ==
           '(- 9 3)')

    # !0
    parser = Parser([
        Token(type=TokenTypes.BANG, lexeme='!', literal=None, line_number=0),
        Token(type=TokenTypes.NUMBER, lexeme='0', literal=0, line_number=0),
    ], l)
    assert(printer.print(parser.parse()) ==
           '(! 0)')
     # -4
    parser = Parser([
        Token(type=TokenTypes.MINUS, lexeme='-', literal=None, line_number=0),
        Token(type=TokenTypes.NUMBER, lexeme='4', literal=4, line_number=0),
    ], l)
    assert(printer.print(parser.parse()) ==
           '(- 4)')

   # -4 * 3
    parser = Parser([
        Token(type=TokenTypes.MINUS, lexeme='-', literal=None, line_number=0),
        Token(type=TokenTypes.NUMBER, lexeme='4', literal=4, line_number=0),
        Token(type=TokenTypes.STAR, lexeme='*', literal=None, line_number=0),
        Token(type=TokenTypes.NUMBER, lexeme='3', literal=3, line_number=0),
    ], l)
    # assert(printer.print(parser.parse()) ==
           # '(* (- 4) 3)')


def test_ast():
    expression = Expr.Binary(
        Expr.Unary(
            Token(type=TokenTypes.MINUS, lexeme="-",
                  literal=None, line_number=1),
            Expr.Literal(123)),
        Token(type=TokenTypes.STAR, lexeme="*", literal=None, line_number=1),
        Expr.Grouping(
            Expr.Literal(45.67)))

    p = Printer()
    assert(p.print(Expr.Literal(45.67)) == '45.67')
    assert(p.print(Expr.Unary(
        Token(type=TokenTypes.MINUS, lexeme="-", literal=None, line_number=1),
        Expr.Literal(123))) == '(- 123)')
    assert(p.print(Expr.Binary(
        Expr.Literal('1'),
        Token(type=TokenTypes.STAR, lexeme="*", literal=None, line_number=1),
        Expr.Grouping(Expr.Literal('2')))) == "(* 1 (group 2))")

    assert(p.print(Expr.Binary(
        Expr.Literal(True),
        Token(type=TokenTypes.EQUAL_EQUAL, lexeme="==",
              literal=None, line_number=1),
        Expr.Literal(False))) == '(== True False)')

    assert(p.print(expression) == "(* (- 123) (group 45.67))")


def test_token():
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

    assert(scan(", . ; - + / * ").tokens == [
        Token(type=TokenTypes.COMMA, lexeme=',', literal=None, line_number=0),
        Token(type=TokenTypes.DOT, lexeme='.', literal=None, line_number=0),
        Token(type=TokenTypes.SEMICOLON, lexeme=';',
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

    assert(scan('fun x(a){return a;}').tokens == [
        Token(type=TokenTypes.FUN, lexeme='fun', literal=None, line_number=0),
        Token(type=TokenTypes.IDENTIFIER, lexeme='x',
              literal=None, line_number=0),
        Token(type=TokenTypes.LEFT_PAREN,
              lexeme='(', literal=None, line_number=0),
        Token(type=TokenTypes.IDENTIFIER, lexeme='a',
              literal=None, line_number=0),
        Token(type=TokenTypes.RIGHT_PAREN, lexeme=')',
              literal=None, line_number=0),
        Token(type=TokenTypes.LEFT_BRACE,
              lexeme='{', literal=None, line_number=0),
        Token(type=TokenTypes.RETURN, lexeme='return',
              literal=None, line_number=0),
        Token(type=TokenTypes.IDENTIFIER, lexeme='a',
              literal=None, line_number=0),
        Token(type=TokenTypes.SEMICOLON, lexeme=';',
              literal=None, line_number=0),
        Token(type=TokenTypes.RIGHT_BRACE,
              lexeme='}', literal=None, line_number=0)
    ])


def run():
    test_token()
    test_ast()
    test_parser()
    print('tests pass')


if __name__ == '__main__':
    run()
