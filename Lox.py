import sys
from os import path
from Scanner import Scanner

class Lox():
    def __init__(self):
        self.had_error = False

    def run(self, src):
        print("echo %s" % src)
        sc = Scanner(src, self)
        sc.scan()
        print("parsed %s" % sc.tokens)
        if self.had_error:
            exit(1)

    def run_file(self, filename):
        print("running %s" % filename)
        if not path.exists(filename):
            Lox.error(message="File does not exist: %s" % filename)
        with open(filename, "r") as f:
            src = f.read()
        self.run(src)

    def run_repl(self):
        while True:
            line = input('> ')
            self.run(line)
            self.had_error = False
        pass

    @staticmethod
    def error(line_num="-", message=""):
        Lox.report(line_num, message)
        exit(1)

    @staticmethod
    def report(line_num, message):
        raise Exception('[LOX ERROR] line %s: %s' %
                         (str(line_num), str(message)))
