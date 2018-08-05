#!/usr/local/bin/python3
import sys
from Lox import Lox

def main():
    args = sys.argv[1:]
    if len(args) > 1:
        print("Usage: ./plox.py <file path>")
        exit(1)
    elif len(args) == 1:
        lox = Lox()
        lox.run_file(args[0])
    else:
        lox = Lox()
        lox.run_repl()


if __name__ == '__main__':
    main()
