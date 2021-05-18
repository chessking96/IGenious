#!/usr/bin/python
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from helper import call, getEnvVar, call_background

if __name__ == "__main__":
    # arguments: filename (with absolute path)
    if len(sys.argv) != 3:
        print("Wrong number of arguments.")
        sys.exit(-1)

    scripts_path = getEnvVar('SOURCE_PATH') + '/scripts'

    file_path = sys.argv[1]
    file_name = sys.argv[2]

    # for now, to make sure, that c++ is compiled
    call_background('cd ' + scripts_path + '/removeSameLineDecl && cmake . && make')

    call(scripts_path + '/removeSameLineDecl/clang_ast_visitor ' + file_path + file_name + ' -- ' + file_path + ' ' + file_name)

    with open(file_path + 'vars.txt', 'r') as myfile:
        data = myfile.read()

    lines = data.split('\n')

    if (len(lines) - 1) % 7 != 0:
        print("Error: vars.txt corrupted.")
        sys.exit(-1)

    vars = {}

    # read code
    with open(file_path + file_name, 'r') as myfile:
        code = myfile.read().split('\n')

    for i in range(0, len(lines) - 1, 7):
        typeBeg = lines[i + 0]
        typeEnd = lines[i + 1]
        varName = lines[i + 2]
        initBeg = lines[i + 3]
        initEnd = lines[i + 4]
        begin = lines[i + 5]
        end = lines[i + 6]

        # get type info from string
        typeBegLine = int(typeBeg.split(':')[-2])
        typeBegCol = int(typeBeg.split(':')[-1])
        typeEndLine = int(typeEnd.split(':')[-2])
        typeEndCol = int(typeEnd.split(':')[-1])
        beginLine = int(begin.split(':')[-2])
        beginCol =  int(begin.split(':')[-1])
        endLine = int(end.split(':')[-2])
        endCol =  int(end.split(':')[-1])

        # todo: get info from initBeg and initEnd

        # insert into dict
        currentVal = vars.get((typeBegLine, typeBegCol, typeEndLine, typeEndCol))
        if currentVal == None:
            currentVal = []
        vars[(typeBegLine, typeBegCol, typeEndLine, typeEndCol)] = currentVal + [(varName, beginLine, beginCol, endLine, endCol)]


    # build new code blocks
    blocks = {}
    for var in vars:
        block = ''
        (tbl, tbc, tel, tec) = var
        varNames = vars[var]


        # do nothing, if it is not a same line decl
        if len(vars[var]) == 1:
            continue

        # same line decl
        minLine = 1000000 # some large integer
        maxLine = -1
        for (name, beginLine, beginCol, endLine, endCol) in varNames:
            # get type
            start = tbc
            end  = tec
            type = ''
            begin_line = tbl - 1
            end_line = tel
            if beginLine < minLine:
                minLine = beginLine
            if endLine > maxLine:
                maxLine = endLine

            i = start - 1
            while True:
                type += code[begin_line][i]
                if i > end and code[begin_line][i].isspace():
                    break
                i += 1

            decl = type + name + ";"
            block += decl + '\n';

        blocks[(typeBegLine, typeBegCol)] = (block, minLine, maxLine)



    for (line, col) in sorted(blocks.keys(), reverse = True):
        (block, minLine, maxLine) = blocks.get((line, col))
        del(code[minLine:maxLine])
        code[line - 1] = block

    # save replaced code
    replaced_code = ''
    for line in code:
        replaced_code += line + '\n'
    with open(file_path + 'rmd_' + file_name, 'w') as myfile:
        myfile.write(replaced_code)
