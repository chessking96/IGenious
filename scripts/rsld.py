#!/usr/bin/python
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from helper import call, getEnvVar, call_background

# This function replaces the same-line declarations of a C-file with single line declarations
def run(file_path, file_name):

    # Make sure, that AST visitor is compiled
    scripts_path = getEnvVar('SOURCE_PATH') + '/scripts'
    call_background('cd ' + scripts_path + '/removeSameLineDecl && cmake . && make')

    # Call AST visitor
    call(scripts_path + '/removeSameLineDecl/clang_ast_visitor ' + os.path.join(file_path, file_name) + ' -- ' + file_path + '/ ' + file_name)

    # Read produced code from AST and create dictionary
    with open(file_path + '/vars.txt', 'r') as myfile:
        data = myfile.read()

    lines = data.split('\n')

    if (len(lines) - 1) % 7 != 0:
        print("Error: vars.txt corrupted.")
        sys.exit(-1)

    vars = {}


    with open(os.path.join(file_path, file_name), 'r') as myfile:
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


    # Build new code blocks
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

        blocks[minLine] = (block, minLine, maxLine)


    for minLine in sorted(blocks.keys(), reverse = True):
        (block, minLine, maxLine) = blocks.get(minLine)
        del(code[minLine-1:maxLine])
        code.insert(minLine-1, block)

    # Build code blocks together
    replaced_code = ''
    for line in code:
        replaced_code += line + '\n'

    # Save new code
    with open(file_path + '/rmd_' + file_name, 'w') as myfile:
        myfile.write(replaced_code)
