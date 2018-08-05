from os import path
import sys


class Lox():
    def __init__(self):
        self.had_error = False

    def run(self, src):
        print("echo %s" % src)
        if self.had_error:
            exit(1)

    def run_file(self, filename):
        print("running %s" % filename)
        if not path.exists(filename):
            Lox.error(message="File does not exist: %s" % filename)
        with open(filename, "r") as f:
            src = f.read()
        run(src)

    def run_repl(self):
        while True:
            line = input('> ')
            run(line)
            self.had_error = False
        pass

    @staticmethod
    def error(line_num="-", message=""):
        Lox.report(line_num, message)
        exit(1)

    @staticmethod
    def report(line_num, message):
        sys.stderr.write('[LOX ERROR] line %s: %s' %
                         (str(line_num), str(message)))
