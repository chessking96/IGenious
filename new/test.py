#!/usr/bin/python

from lark import *

class Printer(Transformer):
    def start(self, s):
        return s[0]

    def program(self, s):
        res = ""
        for stmt in s:
            res += str(stmt)
        return res

    def args(self, s):
        #
        return s[0]

    def arg(self, s):
        return s[0] + ' ' + s[1]

    def type(self, s):
        return s

    def ftype(self, s):
        return s[0]

    def decl(self, s):
        return s[0] + '\n'

    def comment(self, s):
        return s[0]

    def C_COMMENT(self, s):
        return s.value

    def funcdecl(self, s):
        return s[0] + ' ' + s[1] + '(' + s[2] + ')' + ';'

    def func(self, s):
        return " "

    def CNAME(self, s):
        return s.value

    def float(self, s):
        return "float"

    def double(self, s):
        return "double"

    def longdouble(self, s):
        return "long double"

    def leftover(self, s):
        return ""

def main():

    with open('example.c', 'r') as file:
        code = file.read()

    grammar_file = 'rules.lark'

    p = Lark.open(grammar_file, rel_to =__file__, parser = 'earley')

    tree = p.parse(code)

    #print(tree)

    code_orig = Printer().transform(tree)
    print(code_orig)

if __name__ == "__main__":
    main()
