#!/usr/bin/python

from helper import call, call_background, getEnvVar, nameWithoutExtension, readConfig
import sys, re, json

def createMain(file_name, function_name, args, ret, rep):

    # includes
    inc1 = '#include "random_range_igen.c"\n'
    inc2 = '#include "' + file_name + '"\n'
    inc3 = '#include <time.h>\n'
    inc4 = '#include <stdio.h>\n'
    inc5 = '#include <fenv.h>\n'
    inc6 = '#include <math.h>\n'
    includes = inc1 + inc2 + inc3 + inc4 + inc5 + inc6

    # main
    init1 = 'int main(){\n'
    init2 = '\tfesetround(FE_UPWARD);\n'
    init3 = '\tinitRandomSeed();\n'
    init = init1 + init2 + init3

    # read in types
    types = []
    with open('funargs.txt', 'r') as myfile:
        funargs = myfile.read().split('\n')

    for i in range(len(funargs) - 1):
        line = funargs[i]
        fun_name = line.split(',')[0]
        var_type = line.split(',')[2]
        if function_name == fun_name:
            if var_type[0] == ' ': # The split from above sometimes contains an uneccessary blank space
                var_type = var_type[1:]
            if var_type[-1] == '*':
                var_type = var_type[0:-1]
            if var_type[-1] == ' ':
                var_type = var_type[0:-1]
            types.append(var_type)
    input = ''
    for i in range(len(args)):
        arg = args[i]

        #type = arg[0]
        type_2 = types[i]

        length = arg[1]
        pointer = arg[2]
        inputORoutput = arg[3]

        if pointer == 'pointer':
            input1 = '\t' + type_2 + '* x_' + str(i) + ' = malloc(' + str(length) + ' * sizeof(' + type_2 + '));\n' # sizeof(long double) potentially to big
            input2 = '\tfor(int i = 0; i < ' + str(length) + '; i++){\n'
            if inputORoutput == 'input':
                if type_2 == "long double":
                    input3 = '\t\t' + type_2 + ' h = getRandomDoubleDoubleInterval();\n'
                elif type_2 == "double":
                    input3 = '\t\t' + type_2 + ' h = getRandomDoubleInterval();\n'
                elif type_2 == "float":
                    input3 = '\t\t' + type_2 + ' h = getRandomFloatInterval();\n'
            elif inputORoutput == 'output':
                input3 = '\t\t' + type_2 + ' h = 0;\n'
            else:
                print("Error in config file.")
                sys.exit(-1)
            input4 = '\t\tx_' + str(i) + '[i] = h;\n'
            input5 = '\t}\n'
            input_part = input1 + input2 + input3 + input4 + input5
        else:
            print("No pointer type not implemented yet")

        input += input_part

    if ret[0] == "True":
        return1 = '\t' + ret[1] + ' return_value = 0;\n'
    else:
        return1 = ''
    timeS1 = '\tclock_t start = clock();\n'
    timeS2 = '\tfor(long i = 0; i < ' + str(rep) + '; i++){\n'
    timeS = timeS1 + timeS2

    arguments = ''

    if len(args) >= 1:
        arguments += 'x_0'
    for i in range(1, len(args)):
        arguments += ', x_' + str(i)


    if ret[0] == "True":
        call_function = '\t\treturn_value = ' + function_name + '(' + arguments + ');\n'
    else:
        call_function = '\t\t' + function_name + '(' + arguments + ');\n'


    timeE1 = '\t}\n'
    timeE2 = '\tclock_t end = clock();\n'
    timeE3 = '\tlong diff_time = (long)(end - start);\n'
    timeE4 = '\tFILE* file = fopen("score.cov", "w");\n'
    timeE5 = '\tfprintf(file, "%ld\\n", diff_time);\n'
    timeE6 = '\tfclose(file);\n'
    timeE = timeE1 + timeE2 + timeE3 + timeE4 + timeE5 + timeE6

    rep = '\tprintf("BeforeIGenReplacement\\n");\n'

    main_end = '}\n'

    main = init + input + return1 + timeS + call_function + timeE + rep + main_end
    code = includes + main


    with open ('chg_main.c', 'w') as myfile:
        myfile.write(code)


def cleanUp(file_name, function_name, err_type, args, ret, precision):

    with open('igen_chg_main.c', 'r') as myfile:
        c_old = myfile.read()

    substitute = '  printf\("BeforeIGenReplacement' + r'\\' + 'n"\);'

    # read in types
    types = []
    with open('funargs.txt', 'r') as myfile:
        funargs = myfile.read().split('\n')

    for i in range(len(funargs) - 1):
        line = funargs[i]
        fun_name = line.split(',')[0]
        var_type = line.split(',')[2]
        if function_name == fun_name:
            if var_type[0] == ' ': # The split from above sometimes contains an uneccessary blank space
                var_type = var_type[1:]
            if var_type[-1] == '*':
                var_type = var_type[0:-2]
            types.append(var_type)

    if err_type == 'highestAbsolute':

        pre_err1 = '\tint max = 0;\n'
        pre_err2 = '\tint imax = 0;\n'
        pre_err3 = '\tdd_I diff_max = _ia_zero_dd();\n'
        err = pre_err1 + pre_err2 + pre_err3


        for i in range(len(args)):
            arg = args[i]
            length = arg[1]
            pointer = arg[2]
            inputORoutput = arg[3]

            if inputORoutput == 'output':
                if types[i] == "long double":
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

        if ret[0] == "True":
            ret1 = '\tdd_I lower_bound = _ia_set_dd(' + 'return_value' + '.lh, ' + 'return_value' + '.ll, -' + 'return_value' + '.lh, -' + 'return_value' + '.ll);\n'
            ret2 = '\tdd_I upper_bound = _ia_set_dd(-' + 'return_value' + '.uh, -' + 'return_value' + '.ul, ' + 'return_value' + '.uh, ' + 'return_value' + '.ul);\n'
            ret3 = '\tdd_I diff = _ia_sub_dd(upper_bound, lower_bound);\n'
            ret4 = '\tif(_ia_cmpgt_dd(diff, diff_max)){\n'
            ret5 = '\t\tdiff_max = diff;\n'
            ret6 = '\t\tmax = -1;\n'
            ret7 = '\t}\n'
            err += ret1 + ret2 + ret3 + ret4 + ret5 + ret6 + ret7
    else:
        print("This error type is not supported:", err_type)
        sys.exit(-1)

    ans1 = '\tchar* answer = "false";\n'
    ans2 = '\tdouble th = ' + str(10**(-precision)) + ';\n'
    ans3 = '\tif((int)_ia_cmpgt_dd(_ia_set_dd(-th, 0, th, 0), diff_max) == 1){\n'
    ans4 = '\t\tanswer = "true";\n'
    ans5 = '\t}\n'
    ans6 = '\tfile = fopen("sat.cov", "w");\n'
    ans7 = '\tfprintf(file, "%s' + r"\\n" + '", answer);\n'
    ans8 = '\tfclose(file);\n'
    ans9 = '\tfile = fopen("precision.cov", "w");\n'
    ans10 = '\tdouble prec = _ia_cast_dd_to_f64(diff_max).up;\n'
    ans11 = '\tfprintf(file, "%.17g' + r"\\n" + '", prec);\n'
    ans12 = '\tprintf("Precision constraint: %s' + r"\\n" + '", answer);\n'
    ans = ans1 + ans2 + ans3 + ans4 + ans5 + ans6 + ans7 + ans8 + ans9 + ans10 + ans11 + ans12

    p1 = '\tprintf("Diff lower bound: %.17g %.17g' + r"\\n" + '", diff_max.lh, diff_max.ll);\n'
    p2 = '\tprintf("Diff upper bound: %.17g %.17g' + r"\\n" + '", diff_max.uh, diff_max.ul);\n'
    p =  p1 + p2

    code = err + ans + p

    c_new = re.sub(substitute, code, c_old)

    substitute = '#include "random_range.c"'
    code = '#include "cleaned_igen_random_range.c"'
    c_new = re.sub(substitute, code, c_new)

    substitute = '#include "' + file_name + '"'
    code = '#include "igen_chg_rmd_' + file_name + '"'
    c_new = re.sub(substitute, code, c_new)


    with open('cleaned_igen_chg_main.c', 'w') as myfile:
        myfile.write(c_new)

def run(main_path, file_name, function_name, args, ret, rep, prec, err_type, search_counter):
    createMain(file_name, function_name, args, ret, rep)
    igen_src = getEnvVar('IGEN_PATH')
    call_background('python3 ' + igen_src + '/bin/igen.py chg_main.c')
    cleanUp(file_name, function_name, err_type, args, ret, prec)
