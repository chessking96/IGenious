#!/usr/bin/python

from lark import Lark, logger, Transformer, Visitor
import sys
import json
import os, re

class Printer(Transformer):
	def preprocstmt(self, s):
		return (s[0])

	def start(self, s):
		return s[0]

	def program(self, s):
		res = ''
		for decl in s:
			res += str(decl) +'\n'
		return res

	def decl(self, s):
		return s[0]

	def vardeclwith(self, s):
		res = ''
		for i in range(len(s) - 1):
			res += s[i] + ' '
		res += '=' + s[-1] + ' '
		return res

	def vardeclwithout(self, s):
		res = ''
		for i in range(len(s)):
			res += s[i] + ' '
		return res

	def funcdecl(self, s):
		return s[0] + ' ' + s[1] + '(' + str(s[2]) + ');\n'

	def types(self, s):
		return s[0]

	def shortint(self, s):
		return "short int"

	def longdouble(self, s):
		return "long double"

	def double(self, s):
		return "double"

	def dtype(self, s):
		return s[0]

	def type(self, s):
		return s[0]

	def type1(self, s):
		return s[0]

	def type2(self, s):
		return s
	def type3(self, s):
		return s
	def type4(self, s):
		return s
	def type5(self, s):
		return s
	def type6(self, s):
		return s
	def type7(self, s):
		return s
	def type8(self, s):
		return s


	def multivardecl(self, s):
		res = s[0] + s[1]
		for i in range(2, len(s)):
			res += ', ' + s[i]
		return res

	def comment(self, s):
		return s[0]

	def longcomment(self, s):
		return s[0]


	def ccomment(self, s):
		return str(s[0])


	def func(self, s):
		return s[0] + ' ' + s[1] + '(' + str(s[2]) + '){\n' + str(s[3]) + '\n}\n'

	def argument(self, s):
		res = ''
		for decl in s:
			res += str(decl) + ' '
		return res

	def arguments(self, s):
		return s[0]

	def stmts(self, s):
		res = ''
		for decl in s:
			res += str(decl) + '\n'
		return res

	def stmt(self, s):
		return str(s[0]) + ';'

	def assignment(self, s):
		return s[0] + " = " + s[1]

	def expr(self, s):
		return s[0]

	def minus(self, s):
		return '-'

	def plus(self, s):
		return '+'

	def WORD(self, s):
		return s.value

	def CNAME(self, s):
		return s.value

	def NUMBER(self, s):
		return s.value

	def op(self, s):
		return s[0]

	def exprop(self, s):
		return str(s[0]) + "(" + str(s[1]) + ")"

	def expropexpr(self, s):
		return "(" + s[0] + s[1] + s[2] + ")"

	def exprbraces(self, s):
		return "(" + str(s[0]) + ")"

	def exprcname(self, s):
		return s[0]

	def exprnumber(self, s):
		return s[0]

	def star(self, s):
		return '*'

class RemoveMultiDec(Visitor):
	def program(self, s):

		return

	def multivardecl(self, s):
		return

#Get function name, variable name and type out of json file
def load_json(string):
    return re.findall("localVar\": {\n\t\t\"function\": \"(.+(?=\"))\",\n\t\t\"type\": \"(.+(?=\"))\",\n\t\t\"name\": \"(.+(?=\"))", string, re.MULTILINE)


def printFile(tree):
	print('')
	#print(tree)
	res = Printer().transform(tree)
	print(res)

def swapCode(tree):
	with open("config_temp.json", "r") as myfile:
		replacements = load_json(myfile.read())

	print("hi")

	tree = RemoveMultiDec().visit(tree)
	#print(tree)

	print("Bye")
	return


def main():
	if len(sys.argv) != 2:
		print("Argument missing.")
		sys.exit(1)

	filename = sys.argv[1]
	with open(filename, 'r') as file:
		#tokens = json.load(file)
		code = file.read()

	path = os.path.dirname(os.path.realpath(__file__))
	grammar_file = path + '/rules.lark'

	p = Lark.open(grammar_file, rel_to =__file__, parser = 'lalr')


	tree = p.parse(code)
	printFile(tree)
	swapCode(tree)

if __name__ == "__main__":
	main()
