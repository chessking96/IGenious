#!/usr/bin/env python

import sys
import re

def main():

	
	# break, if number of arguments is incorrect
	if len(sys.argv) != 2:
	  	print("Incorrect number of arguments: " + str(len(sys.argv)))
	  	exit()
	  
	# get filename
	filename = sys.argv[1]
	
	# read original code
	with open("code_temp.c", "r") as myfile:
		c = myfile.read()
	#print(c)

	tokens = re.split('(\W)', c)

	some_symbols = ["", "=", "+", "*", "-", "\n", " ", "{", "}"]
	types =  ['double', 'float', 'long double']

	stat = 0
	pos = 0
	curr_type = ''
	names = []
	start = -1
	end = -1
	twice = False

	while True:
		if pos >= len(tokens):
			break
		#if pos >= 150:
		#	break
		token = tokens[pos]
		if token not in some_symbols:
			#print(token, stat)
			if token in types:
				#print("1: " + token)
				stat = 1
				start = pos
				curr_type = token
				twice = False
				if token == 'double' and tokens[pos - 2] == 'long':
					twice = True
					curr_type = 'long double'
			if stat == 1:
				if token in types:
					stat = 1
					start = pos
					curr_type = token
					twice = False
					if token == 'double' and tokens[pos - 2] == 'long':
						twice = True
						curr_type = 'long double'
					names.clear()
					#print("1.1: " + token)
				else:
					stat = 2
					names.append(token)
					#print("2.1: " + token)
				
			elif stat == 2:
				#print("hi")
	
				if token in types:
					stat = 1
					start = pos
					curr_type = token
					twice = False

					if token == 'double' and tokens[pos - 1] == 'long':
						twice = True
						curr_type = 'long double'
					names.clear()
					#print("3.1: " + token)
				elif token == ",":
					stat = 1
					#print("3.2: " + token)
				elif token == ";":
					print("type: " + curr_type)
					end = pos
					for i in range(len(names)):
						#print(i - start, names[i - start], curr_type)
						tokens[start + 2 * i] = "\t" + curr_type + " "
						tokens[start + 2 * i + 1] = names[i] + ";\n"

					del tokens[start + 2 * len(names):end + 3]
					if twice:
						del tokens[start - 2:start]
					names.clear()
					#print("hi", token)
					stat = 0
				else:
					stat = 0
					names.clear()
					#print("not good:" + token)
		

		pos += 1

	c_new = ""
	for token in tokens:
		c_new += token

	f = open("code_temp.c", "w+")
	f.write(c_new)
	f.close()
	# print(c_new)
	
	#input("...");



if __name__ == "__main__":
  	main()
