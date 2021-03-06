#!/usr/bin/python

# This file removes the same line declarations

import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from helper import call, getEnvVar, call_background

# This function replaces the same-line declarations of a C-file with single line declarations
def run(file_path, file_name):

    # Make sure, that AST visitor is compiled
    scripts_path = getEnvVar('SOURCE_PATH') + '/scripts'
    call_background('cd ' + scripts_path + '/removeSameLineDecl/build && cmake .. && make')

    # Call AST visitor
    call(scripts_path + '/removeSameLineDecl/build/clang_ast_visitor ' + os.path.join(file_path, file_name) + ' -- ' + file_path + '/ ' + file_name)

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

    # Extract important information (positions in the code)
    for i in range(0, len(lines) - 1, 7):
        typeBeg = lines[i + 0]
        typeEnd = lines[i + 1]
        varName = lines[i + 2]
        initBeg = lines[i + 3]
        initEnd = lines[i + 4]
        begin = lines[i + 5]
        end = lines[i + 6]

        # Get type info from string
        typeBegLine = int(typeBeg.split(':')[-2])
        typeBegCol = int(typeBeg.split(':')[-1])
        typeEndLine = int(typeEnd.split(':')[-2])
        typeEndCol = int(typeEnd.split(':')[-1])
        beginLine = int(begin.split(':')[-2])
        beginCol =  int(begin.split(':')[-1])
        endLine = int(end.split(':')[-2])
        endCol =  int(end.split(':')[-1])

        # Get positions of initialization
        try:
            initbeginLine = int(initBeg.split(':')[-2])
            initbeginCol =  int(initBeg.split(':')[-1])
            initendLine = int(initEnd.split(':')[-2])
            initendCol =  int(initEnd.split(':')[-1])
        except:
            initbeginLine = -1
            initbeginCol = -1
            initendLine = -1
            initendCol = -1

        # Insert into dict
        currentVal = vars.get((typeBegLine, typeBegCol, typeEndLine, typeEndCol))
        if currentVal == None:
            currentVal = []
        vars[(typeBegLine, typeBegCol, typeEndLine, typeEndCol)] = currentVal + [(varName, beginLine, beginCol, endLine, endCol, initbeginLine, initbeginCol, initendLine, initendCol)]

    # Build new code blocks
    blocks = {}
    for var in vars:
        block = ''
        (tbl, tbc, tel, tec) = var
        varNames = vars[var]

        # Do nothing, if it is not a same line declaration
        if len(vars[var]) == 1:
            continue

        # Same line declaration
        minLine = 1000000 # some large integer
        maxLine = -1
        for (name, beginLine, beginCol, endLine, endCol, initBeginLine, initBeginCol, initEndLine, initEndCol) in varNames:

            # Get varname and type and exact positions
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
            decl = type + name

            # Get initialization value (if exist)
            if initBeginLine != -1:
                init = ''
                i = initBeginCol - 1
                while True:
                    letter = code[initBeginLine-1][i]
                    if (i >= initEndCol) and (letter.isspace() or (letter == ',') or (letter == ';')):
                        break
                    init += code[initBeginLine-1][i]
                    i += 1
                decl += ' = ' + init

            decl += ";"
            block += decl + '\n';

        # build new code blocks
        blocks[minLine] = (block, minLine, maxLine)


    for minLine in sorted(blocks.keys(), reverse = True):
        (block, minLine, maxLine) = blocks.get(minLine)
        del(code[minLine-1:maxLine]) # Delete old declaration
        code.insert(minLine-1, block) # Insert new declaration

    # Build code blocks together
    replaced_code = ''
    for line in code:
        replaced_code += line + '\n'

    # Save new code
    with open(file_path + '/rmd_' + file_name, 'w') as myfile:
        myfile.write(replaced_code)
