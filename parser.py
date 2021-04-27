#!/usr/bin/python

from lark import Lark, logger, Transformer
import sys
import json
import os

class MyTransformer(Transformer):
	def preprocstmt(self, s):
		return

	def decl(self, s):
		if s == [None]:
			return
		return s



def main():
	if len(sys.argv) != 2:
		print("Argument missing.")
		sys.exit(1)

	filename = sys.argv[1]
	with open(filename, 'r') as file:
		#tokens = json.load(file)
		code = file.read()

	#code = 'a'
	path = os.path.dirname(os.path.realpath(__file__))
	grammar_file = path + '/rules.lark'

	p = Lark.open(grammar_file, rel_to =__file__, parser = 'lalr')

	
	tree = p.parse(code)
	#print(tree)
	result = MyTransformer().transform(tree)
	print(result)
	

if __name__ == "__main__":
	main()