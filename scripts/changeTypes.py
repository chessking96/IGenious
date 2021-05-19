#!/usr/bin/python
import sys, os, json
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from helper import call, getEnvVar, call_background, load_json

if __name__ == "__main__":
    # arguments: path, filename without extension
    if len(sys.argv) != 3:
        print("Incorrect number of arguments: " + str(len(sys.argv)))
        sys.exit(-1)

    file_path = sys.argv[1]
    file_name = sys.argv[2] # without extension

    scripts_path = getEnvVar('SOURCE_PATH') + '/scripts'

    # for now, to make sure, that c++ is compiled and run
    call('cd ' + scripts_path + '/changeTypes && cmake . && make')
    call(scripts_path + '/changeTypes/clang_ast_visitor IGen/rmd_' + file_name + ' -- ' + file_path + ' ' + file_name)

    # read code
    with open('IGen/rmd_' + file_name, 'r') as myfile:
        code = myfile.read().split('\n')

    # read vars from clang
    with open('IGen/vars2.txt', 'r') as myfile:
        lines = myfile.read().split('\n')

    if (len(lines) - 1) % 8 != 0:
        print("Error: vars.txt corrupted.")
        sys.exit(-1)

    # read precimonious config
    with open("config_temp.json", "r") as myfile:
        reps = load_json(myfile.read())

    reps_dict = {}

    for rep in reps:
        reps_dict[(rep[0], rep[2])] = rep[1]

    for i in range(len(lines) - 9, 0, -8):
        typeBeg = lines[i + 0]
        typeEnd = lines[i + 1]
        varName = lines[i + 2]
        funName = lines[i + 3]
        initBeg = lines[i + 4]
        initEnd = lines[i + 5]
        begin = lines[i + 6]
        end = lines[i + 7]

        # get type info from string
        typeBegLine = int(typeBeg.split(':')[-2])
        typeBegCol = int(typeBeg.split(':')[-1])
        typeEndLine = int(typeEnd.split(':')[-2])
        typeEndCol = int(typeEnd.split(':')[-1])
        beginLine = int(begin.split(':')[-2])
        beginCol =  int(begin.split(':')[-1])
        endLine = int(end.split(':')[-2])
        endCol =  int(end.split(':')[-1])

        type = reps_dict.get((funName, varName))
        if type == 'longdouble':
            type = 'long double'
        if type == 'longdouble*':
            type = 'long double *'
        if type == None:
            continue



        line = typeBegLine - 1
        i = typeBegCol - 1
        while(True):
            if i >= len(code[line]):
                break
            if i >= typeEndCol - 1 and (code[line][i].isspace() or code[line][i-1] == '*'):
                break
            i += 1

        start = typeBegCol - 1
        end = i

        if type != None and type != 'long double *' and type != 'double*' and type != 'float*':
            code[line] = code[line][0:start] + type + code[line][end:len(code[line])]


    # save replaced code
    replaced_code = ''
    for line in code:
        replaced_code += line + '\n'
    with open('IGen/chg_rmd_' + file_name, 'w') as myfile:
        myfile.write(replaced_code)

    #print(replaced_code)
    # print('f:', count_float, 'd:', count_double, 'dd:', count_longdouble)
