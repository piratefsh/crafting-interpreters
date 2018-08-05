from Scanner import Scanner
from TokenTypes import TokenTypes
from Token import Token

def scan(src):
    s = Scanner(src)
    s.scan()
    return s

def run():

    assert(scan('()').tokens == [Token(type=TokenTypes.LEFT_PAREN, lexeme='(', literal=None, line_number=0),
                        Token(type=TokenTypes.RIGHT_PAREN, lexeme=')', literal=None, line_number=0)])

    assert(scan('( )').tokens == [Token(type=TokenTypes.LEFT_PAREN, lexeme='(', literal=None, line_number=0),
                        Token(type=TokenTypes.RIGHT_PAREN, lexeme=')', literal=None, line_number=0)])

    assert(scan('  ( )  ').tokens == [Token(type=TokenTypes.LEFT_PAREN, lexeme='(', literal=None, line_number=0),
                        Token(type=TokenTypes.RIGHT_PAREN, lexeme=')', literal=None, line_number=0)])

    assert(scan("{}").tokens == [Token(type=TokenTypes.LEFT_BRACE, lexeme='{', literal=None, line_number=0),
                        Token(type=TokenTypes.RIGHT_BRACE, lexeme='}', literal=None, line_number=0)])

    assert(scan(", . : - + / *").tokens == [
      Token(type=TokenTypes.COMMA, lexeme=',', literal=None, line_number=0),
      Token(type=TokenTypes.DOT, lexeme='.', literal=None, line_number=0),
      Token(type=TokenTypes.SEMICOLON, lexeme=':', literal=None, line_number=0),
      Token(type=TokenTypes.MINUS, lexeme='-', literal=None, line_number=0),
      Token(type=TokenTypes.PLUS, lexeme='+', literal=None, line_number=0),
      Token(type=TokenTypes.SLASH, lexeme='/', literal=None, line_number=0),
      Token(type=TokenTypes.STAR, lexeme='*', literal=None, line_number=0)])


    print('tests pass')


def assert_obj_equal(obj1, obj2):
    assert(obj1.__dict__ == obj2.__dict__)
