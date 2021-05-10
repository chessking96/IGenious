#!/usr/bin/python

import sys, json

from parser import createTree, change, printCode

from helper import load_json

def main():
    if len(sys.argv) != 3:
        print("Incorrect number of arguments: " + str(len(sys.argv)))
        sys.exit(-1)

    file_path = sys.argv[1]
    file_name = sys.argv[2]

    #read original code
    with open ('IGen/rmd_' + file_name + '.c', 'r') as myfile:
        c = myfile.read()

    tree = createTree('IGen/rmd_' + file_name + '.c')

    tree_changed = change(tree, "config_temp.json")

    code_new = printCode(tree_changed)

    # print config summary (debug)
    with open("config_temp.json", "r") as myfile:
        reps = load_json(myfile.read())

    count_float = 0
    count_double = 0
    count_longdouble = 0

    for rep in reps:
        if rep[1] == 'float':
            count_float += 1
        elif rep[1] == 'double':
            count_double += 1
        elif rep[1] == 'longdouble':
            count_longdouble += 1


    print('f:', count_float, 'd:', count_double, 'dd:', count_longdouble)


    with open('IGen/chg_rmd_' + file_name + '.c', 'w') as f:
        f.write(code_new)

if __name__ == "__main__":
    main()
