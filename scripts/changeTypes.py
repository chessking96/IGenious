#!/usr/bin/python

import sys, json

from parser import createTree, change, printCode

def main():
    if len(sys.argv) != 3:
        print("Incorrect number of arguments: " + str(len(sys.argv)))
        exit()



    file_path = sys.argv[1]
    file_name = sys.argv[2]


    #read original code
    with open ('IGen/rmd_' + file_name + '.c', 'r') as myfile:
        c = myfile.read()

    tree = createTree('IGen/rmd_' + file_name + '.c')

    tree_changed = change(tree, "config_temp.json")

    code_new = printCode(tree_changed)

    with open('IGen/chg_rmd_' + file_name + '.c', 'w') as f:
        f.write(code_new)


    return


if __name__ == "__main__":
    main()
