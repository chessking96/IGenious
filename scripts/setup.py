#!/usr/bin/python

from helper import call, call_background, getEnvVar, nameWithoutExtension
import sys, re, json

def createMain(func_name):
    # includes
    inc1 = '#include "random_range.c"\n'
    inc2 = '#include "' + file_name + '"\n'
    inc3 = '#include <time.h>\n'
    inc4 = '#include <stdio.h>\n'
    inc5 = '#include <fenv.h>\n'
    inc6 = '#include <math.h>\n'
    include = inc1 + inc2 + inc3 + inc4 + inc5 + inc6

    # main
    main_start = 'int main(){\n'

    init1 = '\tfesetround(FE_UPWARD);\n'
    init2 = '\tinitRandomSeed();\n'
    init = init1 + init2


    # read in types

    if cast:
        with open('IGen/funargs.txt', 'r') as myfile:
            funargs = myfile.read().split('\n')


        for i in range(len(funargs) - 1):
            line = funargs[i]
            fun_name = line.split(',')[0]
            var_type = line.split(',')[2]
            if function_name == fun_name:
                types.append(var_type)

    input = ''
    for i in range(int(len(inputs) / 4)):
        type = inputs[i * 4]
        if cast:
            type_2 = types[i]
        else:
            type_2 = type

        if type_2 == " long double *":
            type_2 = "long double"
        if type_2 == " double*":
            type_2 = "double"
        if type_2 == " float*":
            type_2 = "float"

        if cast:
            types[i] = type_2
        length = inputs[i * 4 + 1]
        pointer = inputs[i * 4 + 2]
        inputORoutput = inputs[i * 4 + 3]
        if pointer == 'pointer':
            input1 = '\t' + type_2 + '* x_' + str(i) + ' = malloc(' + str(length) + ' * sizeof(long double));\n' # sizeof(long double) potentially to big
            input2 = '\tfor(int i = 0; i < ' + str(length) + '; i++){\n'
            if inputORoutput == 'input':
                if type_2 == "long double":
                    input3 = '\t\t' + type_2 + ' h = getRandomDoubleDouble();\n'
                elif type_2 == "double":
                    input3 = '\t\t' + type_2 + ' h = getRandomDouble();\n'
                elif type_2 == "float":
                    input3 = '\t\t' + type_2 + ' h = getRandomFloat();\n'
            elif inputORoutput == 'output':
                input3 = '\t\t' + type_2 + ' h = 0;\n'
            else:
                print("Error in config file.")
                sys.exit(-1)
            input4 = '\t\tx_' + str(i) + '[i] = h;\n'
            input5 = '\t}\n'
            input_part = input1 + input2 + input3 + input4 + input5
        else:
            print("Not implemented yet")


        input += input_part

    if returnInfo[0] == "True":
        return1 = '\t' + returnInfo[1] + ' return_value = 0;\n'
    else:
        return1 = ''
    timeS1 = '\tclock_t start = clock();\n'
    timeS2 = '\tfor(int i = 0; i < ' + str(repetitions) + '; i++){\n'
    timeS = timeS1 + timeS2

    arguments = ''



    if int(len(inputs) / 4) >= 1:
        arguments += 'x_0'
    for i in range(1, int(len(inputs) / 4)):

        arguments += ', x_' + str(i)


    if returnInfo[0] == "True":
        call = '\t\treturn_value = ' + function_name + '(' + arguments + ');\n'
    else:
        call = '\t\t' + function_name + '(' + arguments + ');\n'


    timeE1 = '\t}\n'
    timeE2 = '\tclock_t end = clock();\n'
    timeE3 = '\tlong diff_time = (long)(end-start);\n'
    timeE4 = '\tFILE* file = fopen("score.cov", "w");\n'
    timeE5 = '\tfprintf(file, "%ld\\n", diff_time);\n'
    timeE6 = '\tfclose(file);\n'
    timeE = timeE1 + timeE2 + timeE3 + timeE4 + timeE5 + timeE6

    rep = '\tprintf("BeforeIGenReplacement\\n");\n'

    main_end = '}\n'

    main = main_start + init + input + return1 + timeS + call + timeE + rep + main_end
    code = include + main

    if cast:
        with open ('IGen/' + func_name, 'w') as myfile:
            myfile.write(code)
    else:
        with open (file_path + func_name, 'w') as myfile:
            myfile.write(code)

def precimoniousSetup():
    call('cp ' + src_path + '/random_range.c ' + file_path)

    call('cd ' + file_path + ' && clang -emit-llvm -c ' + 'main.c' + ' -o '
    + nameWOExt + '.bc')

    call('cd ' + file_path + ' && opt -load ' + shared_lib + ' -create-call-dependency '
    + nameWOExt + '.bc --call-main ' + function_name + ' > '
    + nameWOExt +  '.tmp')
    call('rm ' + file_path + nameWOExt +  '.tmp')

    call('touch ' + file_path + 'exclude.txt') # would allow to exclude variables from analysis

    call('cd ' + file_path + ' && opt -load ' + shared_lib + ' -config-file --only-arrays --only-scalars --funs --pformat '
    + nameWOExt + '.bc --filename config_' + nameWOExt + '.json > '
    + nameWOExt +  '.tmp')
    call('rm ' + file_path + nameWOExt +  '.tmp')

    call('cd ' + file_path + ' && opt -load ' + shared_lib + ' -search-file --original-type --only-arrays --only-scalars --funs '
    + nameWOExt + '.bc --filename search_' + nameWOExt + '.json > '
    + nameWOExt +  '.tmp')
    call('rm ' + file_path + nameWOExt +  '.tmp')

    call('cp ' + src_path + '/normal_CMakeLists.txt ' + file_path + 'CMakeLists.txt')

def igenSetup():
    call('cd ' + file_path + ' && mkdir IGen && cp ' + file_name + ' IGen/')
    call('cd ' + file_path + ' && cp ' + 'random_range.c' + ' IGen/')
    call('cd ' + file_path + ' && cp ' + 'main.c' + ' IGen/')
    print("setup", file_path, file_name)

    # remove same line declarations
    call('python3 ' + scripts_path + '/rsld.py ' + file_path + 'IGen/ ' + file_name)
    call_background('cd ' + file_path + 'IGen && python3 ' + igen_path + '/bin/igen.py main.c')
    # call_background('cd ' + file_path + 'IGen && python3 ' + igen_path + '/bin/igen.py random_range.c')
    call_background('cd ' + file_path + 'IGen && python3 ' + igen_path + '/bin/igen.py rmd_' + file_name)

    call('cp ' + src_path + '/igen_CMakeLists.txt ' + file_path + 'IGen/CMakeLists.txt')

def cleanUp():
    # main
    if cast:
        with open('IGen/igen_casts_main.c', 'r') as myfile:
            c_old = myfile.read()
    else:
        with open(file_path + 'IGen/igen_main.c', 'r') as myfile:
            c_old = myfile.read()

    substitute = 'printf\("BeforeIGenReplacement' + r'\\' + 'n"\);'

    if errorType == 'highestAbsolute':

        pre_err1 = '\tint max = 0;\n'
        pre_err2 = '\tint imax = 0;\n'
        pre_err3 = '\tdd_I diff_max = _ia_zero_dd();\n'
        err = pre_err1 + pre_err2 + pre_err3


        for i in range(int(len(inputs) / 4)):
            type = inputs[i * 4]
            length = inputs[i * 4 + 1]
            pointer = inputs[i * 4 + 2]
            inputORoutput = inputs[i * 4 + 3]

            if inputORoutput == 'output':
                if cast and types[i] == "long double":
                    varName = 'x_' + str(i)
                    err1 = '\tfor(int i = 0; i < ' + str(length) + '; i++){\n'
                    err2 = '\t\tdd_I lower_bound = _ia_set_dd(' + varName + '[i].lh, ' + varName + '[i].ll, -' + varName + '[i].lh, -' + varName + '[i].ll);\n'
                    err3 = '\t\tdd_I upper_bound = _ia_set_dd(-' + varName + '[i].uh, -' + varName + '[i].ul, ' + varName + '[i].uh, ' + varName + '[i].ul);\n'
                    err4 = '\t\tdd_I diff = _ia_sub_dd(upper_bound, lower_bound);\n'
                    err5 = '\t\tif(_ia_cmpgt_dd(diff, diff_max)){\n'
                    err6 = '\t\t\tdiff_max = diff;\n'
                    err7 = '\t\t\tmax = i;\n'
                    err8 = '\t\t}\n'
                    err9 = '\t}\n'
                    err += err1 + err2 + err3 + err4 + err5 + err6 + err7 + err8 + err9
                else:
                    varName = 'x_' + str(i)
                    err1 = '\tfor(int i = 0; i < ' + str(length) + '; i++){\n'
                    err2 = '\t\tdd_I lower_bound = _ia_set_dd(' + varName + '[i].lo, ' + str(0) + ', -' + varName + '[i].lo, -' + str(0) + ');\n'
                    err3 = '\t\tdd_I upper_bound = _ia_set_dd(-' + varName + '[i].up, -' + str(0) + ', ' + varName + '[i].up, ' + str(0) + ');\n'
                    err4 = '\t\tdd_I diff = _ia_sub_dd(upper_bound, lower_bound);\n'
                    err5 = '\t\tif(_ia_cmpgt_dd(diff, diff_max)){\n'
                    err6 = '\t\t\tdiff_max = diff;\n'
                    err7 = '\t\t\tmax = i;\n'
                    err8 = '\t\t}\n'
                    err9 = '\t}\n'
                    err += err1 + err2 + err3 + err4 + err5 + err6 + err7 + err8 + err9

        if returnInfo[0] == "True":
            ret1 = '\tdd_I lower_bound = _ia_set_dd(' + 'return_value' + '.lh, ' + 'return_value' + '.ll, -' + 'return_value' + '.lh, -' + 'return_value' + '.ll);\n'
            ret2 = '\tdd_I upper_bound = _ia_set_dd(-' + 'return_value' + '.uh, -' + 'return_value' + '.ul, ' + 'return_value' + '.uh, ' + 'return_value' + '.ul);\n'
            ret3 = '\tdd_I diff = _ia_sub_dd(upper_bound, lower_bound);\n'
            ret4 = '\tif(_ia_cmpgt_dd(diff, diff_max)){\n'
            ret5 = '\t\tdiff_max = diff;\n'
            ret6 = '\t\tmax = -1;\n'
            ret7 = '\t}\n'
            err += ret1 + ret2 + ret3 + ret4 + ret5 + ret6 + ret7

    ans1 = '\tchar* answer = "false";\n'
    ans2 = '\tdouble th = ' + str(precision) + ';\n'
    ans3 = '\tif((int)_ia_cmpgt_dd(_ia_set_dd(-th, 0, th, 0), diff_max) == 1){\n'
    ans4 = '\t\tanswer = "true";\n'
    ans5 = '\t}\n'
    ans6 = '\tfile = fopen("sat.cov", "w");\n'
    ans7 = '\tfprintf(file, "%s' + r"\\n" + '", answer);\n'
    ans8 = '\tfclose(file);\n'
    ans9 = '\tprintf("%s' + r"\\n" + '", answer);\n'
    ans = ans1 + ans2 + ans3 + ans4 + ans5 + ans6 + ans7 + ans8 + ans9

    dr = 'x_0'

    #p1 = '\tprintf("Debug: %.20g %.20g' + r"\\n" + '", ' + dr + '[0].lh, ' + dr + '[0].ll);\n'
    #p2 = '\tprintf("Debug: %.20g %.20g' + r"\\n" + '", ' + dr + '[0].uh, ' + dr + '[0].ul);\n'
    p1 = ''
    p2 = ''
    p3 = '\tprintf("Diff lower bound: %.17g %.17g' + r"\\n" + '", diff_max.lh, diff_max.ll);\n'
    p4 = '\tprintf("Diff upper bound: %.17g %.17g' + r"\\n" + '", diff_max.uh, diff_max.ul);\n'
    p =  p1 + p2 + p3 + p4

    code = err + ans + p

    c_new = re.sub(substitute, code, c_old)

    substitute = '#include "random_range.c"'
    code = '#include "cleaned_igen_random_range.c"'
    c_new = re.sub(substitute, code, c_new)

    substitute = '#include "' + file_name + '"'
    code = '#include "igen_chg_rmd_' + file_name + '"'
    c_new = re.sub(substitute, code, c_new)

    if cast:
        with open('IGen/cleaned_igen_casts_main.c', 'w') as myfile:
            myfile.write(c_new)
    else:
        with open(file_path + 'IGen/cleaned_igen_casts_main.c', 'w') as myfile:
            myfile.write(c_new)

    if not cast:
        # random_range
        init1 = '#include <stdlib.h>\n'
        init2 = 'void initRandomSeed(){\n'
        init3 = '\tsrand(42);\n'
        init4 = '}\n'
        init = init1 + init2 + init3 + init4

        dd1 = 'dd_I getRandomDoubleDouble() {\n'
        dd2 = '\tdouble r1 = ((double)rand())/(RAND_MAX);\n'
        dd3 = '\tdd_I a = _ia_set_dd(-r1, 0, r1, 0);\n'
        dd4 = '\treturn a;\n'
        dd5 = '}\n'
        dd = dd1 + dd2 + dd3 + dd4 + dd5

        d1 = 'f64_I getRandomDouble() {\n'
        d2 = '\tdouble r = ((double)rand())/(RAND_MAX);\n'
        d3 = '\tf64_I a = _ia_set_f64(-r, r);\n'
        d4 = '\treturn a;\n'
        d5 = '}\n'
        d = d1 + d2 + d3 + d4 + d5

        f1 = 'f32_I getRandomFloat() {\n'
        f2 = '\tfloat r = ((float)rand())/(RAND_MAX);\n'
        f3 = '\tf32_I a = _ia_set_f32(-r, r);\n'
        f4 = '\treturn a;\n'
        f5 = '}\n'
        f = f1  + f2 + f3 + f4 + f5

        c = init + dd + d + f

        with open(file_path + 'IGen/cleaned_igen_random_range.c', 'w') as myfile:
                myfile.write(c)

if __name__ == "__main__":
    # arguments: filepath filename, functionname, cast
    if len(sys.argv) != 5:
        print("Wrong number of arguments.")
        sys.exit(-1)

    file_path = sys.argv[1] + 'analysis/'
    file_name = sys.argv[2]
    function_name = sys.argv[3]

    types = []

    # use same file for run (just for now)
    if sys.argv[4] == "yes":
        cast = True
    else:
        cast = False

    if cast:
        with open('../config.json', 'r') as myfile:
            data = json.load(myfile)
            inputs = data['args']
        if len(inputs) % 4 != 0:
            printf("Config file is not valid.")
            sys.exit(-1)

        repetitions = data['repetitions']
        precision = data['precision']
        errorType = data['errortype']
        returnInfo = data['return']

        nameWOExt = nameWithoutExtension(file_name)
        prec_path = getEnvVar('CORVETTE_PATH') # path to precimonious
        scripts_path = getEnvVar('SOURCE_PATH') + '/scripts' # path to scripts
        src_path = getEnvVar('SOURCE_PATH') + '/src'
        igen_path = getEnvVar('IGEN_PATH')
        shared_lib = prec_path + '/src/Passes.so'

        createMain('casts_main.c')
        call_background('cd ' + 'IGen && python3 ' + igen_path + '/bin/igen.py casts_main.c')
        cleanUp()


    else:

        with open(file_path + '../config.json', 'r') as myfile:
            data = json.load(myfile)
            inputs = data['args']

        if len(inputs) % 4 != 0:
            printf("Config file is not valid.")
            sys.exit(-1)

        repetitions = data['repetitions']
        precision = data['precision']
        errorType = data['errortype']
        returnInfo = data['return']

        nameWOExt = nameWithoutExtension(file_name)
        prec_path = getEnvVar('CORVETTE_PATH') # path to precimonious
        scripts_path = getEnvVar('SOURCE_PATH') + '/scripts' # path to scripts
        src_path = getEnvVar('SOURCE_PATH') + '/src'
        igen_path = getEnvVar('IGEN_PATH')
        shared_lib = prec_path + '/src/Passes.so'
        createMain('main.c')
        precimoniousSetup()
        print("Precimonious setup finished.")
        igenSetup()
        cleanUp()
        print("IGen setup finished.")
