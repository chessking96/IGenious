#!/usr/bin/python

from lark import Lark, logger, Transformer, Visitor, Tree, Token
import sys
import json
import os, re

from helper import getEnvVar

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
		res = ''
		for i in range(len(s)):
			res += s[i]
		return res


	def typespointer(self, s):
		return s[0] + "*"

	def typeswithoutpointer(self, s):
		return s[0]

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

	def char(self, s):
		return "char"

	def signedchar(self, s):
		return "signed char"

	def unsignedchar(self, s):
		return "unsigned char"

	def short(self, s):
		return "short"

	def shortint(self, s):
		return "short int"

	def signedshort(self, s):
		return "signed short"

	def signedshortint(self, s):
		return "signed short int"

	def unsignedshort(self, s):
		return "unsigned short"

	def unsignedshortint(self, s):
		return "unsigned short int"

	def int(self, s):
		return "int"

	def signed(self, s):
		return "signed"

	def signedint(self, s):
		return "signed int"

	def unsigned(self, s):
		return "unsigned"

	def unsignedint(self, s):
		return "unsigned int"

	def long(self, s):
		return "long"

	def longint(self, s):
		return "long int"

	def signedlong(self, s):
		return "signed long"

	def signedlongint(self, s):
		return "signed long int"

	def unsignedlong(self, s):
		return "unsigned long"

	def unsignedlongint(self, s):
		return "unsigned long int"

	def longlong(self, s):
		return "long long"

	def longlongint(self, s):
		return "long long int"

	def signedlonglong(self, s):
		return "signed long long"

	def signedlonglongint(self, s):
		return "signed long long int"

	def unsignedlonglong(self, s):
		return "unsigned long long"

	def unsignedlonglongint(self, s):
		return "unsigned long long int"

	def float(self, s):
		return "float"

	def double(self, s):
		return "double"

	def longdouble(self, s):
		return "long double"

	def multivardecl(self, s):
		res = s[0] + ' ' + s[1]
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
		for i in range(len(s) - 1):
			res += s[i] + ' '
		res += s[len(s) - 1]
		return res

	def arguments(self, s):
		res = ''
		if len(s) >= 1:
			res += s[0]
		for i in range(1, len(s)):
			res += ', ' + s[i]
		return res

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
		res = ''
		for i in range(len(s)):
			res += s[i]
		return res

	def WORD(self, s):
		return s.value

	def CNAME(self, s):
		return s.value

	def NUMBER(self, s):
		return s.value

	def op(self, s):
		return s[0]

	def lbrace(self, s):
		return "("

	def rbrace(self, s):
		return ")"

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

	def minus(self, s):
		return '-'

	def plus(self, s):
		return '+'

class RemoveMultiDec(Visitor):
	def some():
		return

	def stmts(self, t):

		s = t.children
		for i in range(len(s)): # all statments
			if s[i].children[0].data == 'multivardecl': # if statement is multivardecl
				mvd = s[i].children[0]
				type = mvd.children[0]
				vars = mvd.children
				newstmts = []
				for j in range(1, len(vars)):
					newstmts += [Tree('stmt', [Tree('vardeclwithout', [type] + [Token('CNAME', vars[j])])])]

				del(t.children[i])
				for j in range(len(newstmts)):
					t.children.insert(i + j, newstmts[j])

class ChangeTypes(Visitor):


	def func(self, s):
		fun_name = s.children[1]
		# arguments: s.children[2]
		body = s.children[3]
		stmts = body.children
		for i in range(len(stmts)):
			stmt = stmts[i]
			if (stmt.children[0].data == 'vardeclwithout' or stmt.children[0].data == 'vardeclwith')\
			and stmt.children[0].children[0].data == 'dtype':
				name = stmt.children[0].children[1]
				newtype = str(reps_dict.get((fun_name, name)))
				s.children[3].children[i].children[0].children[0] = Tree((newtype), [])

# self made json load, as standard json load doesn't work for this file
def load_json(string):
    return re.findall("localVar\": {\n\t\t\"function\": \"(.+(?=\"))\",\n\t\t\"type\": \"(.+(?=\"))\",\n\t\t\"name\": \"(.+(?=\"))", string, re.MULTILINE)

# create tree from file.c
def createTree(filename):
	with open(filename, 'r') as file:
		code = file.read()

	path = getEnvVar('SOURCE_PATH')
	grammar_file = path + '/src/rules.lark'
	p = Lark.open(grammar_file, rel_to =__file__, parser = 'lalr')
	tree = p.parse(code)
	return tree

# exchange, according to replacements
def change(tree, path_config):
	with open(path_config, "r") as myfile:
		reps = load_json(myfile.read())

	global reps_dict
	reps_dict = {}

	for rep in reps:
		reps_dict[(rep[0], rep[2])] = rep[1]

	ChangeTypes().visit(tree)

	return tree

# remove multi declaration
def removeMultiDecl(tree):
	return RemoveMultiDec().visit(tree)

# print tree to code
def printCode(tree):
	return Printer().transform(tree)


def main():
	if len(sys.argv) != 2:
		print("Argument missing.")
		sys.exit(1)

	tree = createTree(sys.argv[1])

	code_orig = Printer().transform(tree)

	afterrm = RemoveMultiDec().visit(tree)

	code_after_remove = Printer().transform(afterrm)


	afterrep = change(tree, "config_temp.json")

	code_after_rep = Printer().transform(afterrep)

	#print(afterrep)
	#print(code_after_rep)

if __name__ == "__main__":
	main()
