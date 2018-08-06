import os
from grammar import Grammar
import shutil

PARENT_CLASS_TEMPLATE = '''
class %s():
    pass
'''

INHERITED_CLASS_TEMPLATE = '''
from %s import %s
class %s(%s):
    def __init__(%s):
%s
'''

ROOT_DIR = "./ast"


def clean():
    if os.path.exists(ROOT_DIR):
        shutil.rmtree(ROOT_DIR)


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
        ruleset_path = os.path.join(ROOT_DIR, ruleset_dirname)
        filepath = os.path.join(ruleset_path, filename)


        if not os.path.exists(ruleset_path):
            os.mkdir(ruleset_path)

        # make parent class file
        with open(filepath, 'w') as f:
            f.write(PARENT_CLASS_TEMPLATE % parent_class)

        # make parent dir a module
        with open(os.path.join(ruleset_path, '__init__.py'), 'w') as f:
            f.write('#make module') 

        # make rules
        for rule_name, rule_params in ruleset['rules'].items():
            print(" %s" % rule_name)
            filename = "%s.py" % rule_name
            params = [p.split()[1] for p in rule_params]
            params_init = ["\t\t\tself.%s = %s" % (p, p) for p in params]
            data = (parent_class, parent_class, rule_name, parent_class,
                    ', '.join(params), '\n'.join(params_init))

            filepath = os.path.join(ruleset_path, filename)
            with open(filepath, 'w') as f:
                f.write(INHERITED_CLASS_TEMPLATE % data)


def main():
    clean()
    gen_grammar(Grammar)


if __name__ == '__main__':
    main()
