#!/usr/local/bin/python3

import os
from grammar import Grammar
import shutil

PARENT_CLASS_TEMPLATE = '''class %s():
    def accept(visitor):
        return
'''

INHERITED_CLASS_TEMPLATE = '''

class %s(%s):
    def __init__(self, %s):
%s
    def accept(visitor):
        visitor.visit%s()
'''

VISITOR_TEMPLATE='''
class Visitor():
    def __init__(self):
        pass

    %s
'''

ROOT_DIR = "./ast"


def clean():
    if os.path.exists(ROOT_DIR):
        shutil.rmtree(ROOT_DIR)

def gen_visitor_superclass(rules, parent_type):
    visit_types = [ \
        'def visit%s%s():\n        return' % (name, parent_type) \
        for name, _ in rules.items()]

    return VISITOR_TEMPLATE % "\n\n    ".join(visit_types)


def gen_grammar(grammar):
    # make directory for ruleset
    if not os.path.exists(ROOT_DIR):
        os.mkdir(ROOT_DIR)
    # add __init__.py to ROOT_DIR
    with open(os.path.join(ROOT_DIR, '__init__.py'), 'w') as f:
        f.write('#make module')

    for ruleset in grammar:
        print(ruleset['name'])
        # make parent class
        parent_class = ruleset['name']
        filename = "%s.py" % parent_class
        ruleset_dirname = "%s" % parent_class
        ruleset_path = ROOT_DIR
        parent_filepath = os.path.join(ruleset_path, filename)
        visitor_filepath = os.path.join(ruleset_path, "Visitor.py")


        if not os.path.exists(ruleset_path):
            os.mkdir(ruleset_path)

        with open(parent_filepath, 'w') as f:
            # make parent class file
            f.write(PARENT_CLASS_TEMPLATE % parent_class)

            # make visitor class file
            f.write(gen_visitor_superclass(ruleset['rules'], parent_class))


            # make rules
            for rule_name, rule_params in ruleset['rules'].items():
                print(" %s" % rule_name)
                # filename = "%s.py" % rule_name
                params = [p.split()[1] for p in rule_params]
                params_init = ["        self.%s = %s" % (p, p) for p in params]
                classname = rule_name + parent_class
                data = (classname, parent_class, ', '.join(params),
                    '\n'.join(params_init), rule_name + parent_class)

                filepath = os.path.join(ruleset_path, filename)
                f.write(INHERITED_CLASS_TEMPLATE % data)



def main():
    clean()
    gen_grammar(Grammar)


if __name__ == '__main__':
    main()
