#!/usr/bin/python

import sys
import json

brackets = ['[', ']', '(', ')', '{', '}']
operators = ['+', '-', '*', '/']
assignments = ['=', '<', '>']
others = [';', '#', '.']

spaces = [' ', '\t']
linebreak = ['\n']

lowercase = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', \
'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

uppercase = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', \
'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

underscore = ['_']
letters = lowercase + uppercase
digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
names = lowercase + uppercase + digits + underscore	

def main():
	if len(sys.argv) != 2:
		print("Argument missing.")
		sys.exit(1)

	filename = sys.argv[1]
	with open(filename, 'r') as file:
		code = file.read()

	pos = 0

	tokens = []

	while(True):
		if pos == len(code):
			break

		char = code[pos]
		if char in names:
			pos = read_name(tokens, code, pos)
		elif char in digits:
			pos = read_number(tokens, code, pos)
		elif char in brackets or char in operators or char in assignments \
		or char in linebreak or char in others:
			tokens.append(char)
			pos += 1
		elif char in spaces:
			pos += 1


	print(tokens)
	with open('json_' + filename, 'w') as file:
		json.dump(tokens, file, indent = 2)



def read_name(tokens, code, pos):
	name = code[pos]
	while(True):
		pos += 1
		if pos >= len(code) or (not (code[pos] in names)):
			tokens.append(name)
			break;
		else:
			name += code[pos]
	return pos

def read_number(tokens, code, pos):
	name = code[pos]
	while(True):
		pos += 1
		if pos >= len(code) or code[pos] not in digits + ['.']: # add suport for constants (Long, float, etc.)
			tokens.append(name)
			break;
		else:
			name += code[pos]
	return pos


if __name__ == "__main__":
	main()