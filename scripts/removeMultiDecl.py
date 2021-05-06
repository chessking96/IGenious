#!/usr/bin/python

import sys
from parser import createTree, removeMultiDecl, printCode

def main():
    if len(sys.argv) != 3:
        print("Incorrect number of arguments: " + str(len(sys.argv)))
        exit()

	# get filename
    filename = sys.argv[2]
    path = sys.argv[1]

    # read original code
    with open(path + filename, "r") as myfile:
        c = myfile.read()

    tree = createTree(path + filename)
    multidecl_removed = removeMultiDecl(tree)
    c_new = printCode(multidecl_removed)

    with open(path + 'rmd_' + filename, 'w') as myfile:
        myfile.write(c_new)


if __name__ == "__main__":
    main()
