#!/usr/bin/python

# This code creates a suitable main file for a given configuration

from helper import call, call_background, getEnvVar, nameWithoutExtension, Config
import sys, re, json

# If the program produces the same result, independent of the input,
# the accuracy measurment is done only once
input_dependent = False

# Builds a suitable main function for the program
def createMain(path, config):
    global input_dependent
    input_dependent = False

    # includes
    inc = ''
    inc += '#include "random_range_igen.c"\n'
    inc += '#include "' + config.file_name + '"\n'
    inc += '#include <time.h>\n'
    inc += '#include <stdio.h>\n'
    inc += '#include <fenv.h>\n'
    inc += '#include <math.h>\n'
    includes = inc

    # main
    init = ''
    init += 'int main(){\n'
    init += '\tfesetround(FE_UPWARD);\n'
    init += '\tinitRandomSeed();\n'

    # read in types
    types = []
    try:
        with open('funargs.txt', 'r') as myfile:
            funargs = myfile.read().split('\n')

        for i in range(len(funargs) - 1):
            line = funargs[i]
            fun_name = line.split(',')[0]
            var_type = line.split(',')[2]
            if config.function_name == fun_name:
                if var_type[0] == ' ': # The split from above sometimes contains an uneccessary blank space
                    var_type = var_type[1:]
                if var_type[-1] == '*':
                    var_type = var_type[:-1]
                if var_type[-1] == ' ':
                    var_type = var_type[:-1]
                types.append(var_type)
    except: # During initialization, no funargs.txt exists, just use long double
        for arg in config.function_args:
            types.append('long double')

    # Get function signature
    if config.return_info[0] == "True":
        typedef_text = '\ttypedef dd_I (*FunctionType)('
    elif config.return_info[0] == "False":
        typedef_text = '\ttypedef void (*FunctionType)('
    else:
        print('error in config file, return_info')
    if len(types) >= 1:
        if types[0] == 'long double':
            typedef_text += 'dd_I*'
        elif types[0] == 'double':
            typedef_text += 'f64_I*'
        elif types[0] == 'float':
            typedef_text += 'f32_I*'
    for i in range(1, len(types)):
        if types[i] == 'long double':
            typedef_text += ', dd_I*'
        elif types[i] == 'double':
            typedef_text += ', f64_I*'
        elif types[i] == 'float':
            typedef_text += ', f32_I*'
    typedef_text += ');\n'

    # This is to confuse GCC, that repetitions don't get optimized away
    typedef_text += '\tFunctionType * addresses = aligned_alloc(32, ' + str(config.repetitions) + ' * sizeof(FunctionType));\n'
    typedef_text += '\tfor(int i = 0;i < ' + str(config.repetitions) + '; i++){\n'
    typedef_text += '\taddresses[i] = (FunctionType)' + config.function_name + ';\n'
    typedef_text += '\t}\n'

    # Code for time and accuracy measurement
    diff_max_decl = '\tdd_I diff_max = _ia_zero_dd();\n'
    temp_decl = '\tu_ddi temp;\n'
    time_decl = '\tclock_t start;\n'
    time_decl += '\tclock_t end;\n'
    time_decl += '\tlong diff_time = 0;\n'

    # Check if code is input dependent
    for i in range(len(config.function_args)):
        arg = config.function_args[i]
        if arg.input_or_output == 'input':
            input_dependent = True

    # Create code to produce random input
    num_reps = config.repetitions_input
    loop_start = '\tfor(long j = 0; j < ' + str(num_reps) + '; j++){\n'
    input = typedef_text + diff_max_decl + temp_decl + time_decl + loop_start
    for i in range(len(config.function_args)):
        arg = config.function_args[i]
        type = types[i]
        length = arg.length
        pointer = arg.ptr_type
        inputORoutput = arg.input_or_output
        if pointer == 'pointer':
            input1 = ''
            input1 += '\t' + type + '* x_' + str(i) + ';\n'
            input1 += '\tif(j==0){\n'
            input1 += '\tx_' + str(i) + ' = aligned_alloc(32, ' + str(length) + ' * sizeof(' + type + '));\n' # sizeof(long double) potentially to big
            input1 += '\t}\n\tfor(int i = 0; i < ' + str(length) + '; i++){\n'
            if inputORoutput == 'input':
                if type == "long double" and config.input_precision == 'dd':
                    input1 += '\t\t' + type + ' h = getRandomDoubleDoubleInterval();\n'
                elif type == "double" or (type == "long double" and config.input_precision == 'd'):
                    input1 += '\t\t' + 'double' + ' h = getRandomDoubleInterval();\n'
                elif type == "float":
                    input1 += '\t\t' + type + ' h = getRandomFloatInterval();\n'
            elif inputORoutput == 'output':
                input1 += '\t\t' + type + ' h = 0;\n'
            else:
                print("Error in config file.")
                sys.exit(-1)
            input1 += '\t\tx_' + str(i) + '[i] = h;\n'
            input1 += '\t}\n'
            input_part = input1
        else:
            print("Non-pointer type not implemented yet")
        input += input_part

    # Init return value, if function returns a value
    if config.return_info[0] == "True":
        return1 = '\t' + config.return_info[1] + ' return_value = 0;\n'
    else:
        return1 = ''

    # Time measurement
    timeS = ''
    timeS += '\tFunctionType func;\n'
    timeS += '\tstart = clock();\n'
    timeS += '\tfor(long i = 0; i < ' + str(config.repetitions) + '; i++){\n'

    # Actual function call
    arguments = ''
    if len(config.function_args) >= 1:
        arguments += 'x_0'
    for i in range(1, len(config.function_args)):
        arguments += ', x_' + str(i)
    call_function = '\t\tfunc = (FunctionType)addresses[i];\n'
    if config.return_info[0] == "True":
        call_function += '\t\treturn_value = ' + 'func' + '(' + arguments + ');\n'
    else:
        call_function += '\t\t' + 'func' + '(' + arguments + ');\n'

    # Time measurment
    timeE = ''
    timeE += '\t}\n'
    timeE += '\tend = clock();\n'
    timeE += '\tdiff_time += end - start;'

    # Placeholder to replace after IGen call
    rep = '\tprintf("BeforeIGenReplacement\\n");\n'

    # Build everything togheter
    main_end = '}\n'
    main = init + input + return1 + timeS + call_function + timeE + rep + main_end
    code = includes + main

    # Save main file
    with open (path + '/chg_main.c', 'w') as myfile:
        myfile.write(code)


def cleanUp(path, config):

    with open(path + '/igen_chg_main.c', 'r') as myfile:
        c_old = myfile.read()

    substitute = '  printf\("BeforeIGenReplacement' + r'\\' + 'n"\);'

    # read in types
    types = []
    try:
        with open('funargs.txt', 'r') as myfile:
            funargs = myfile.read().split('\n')

        for i in range(len(funargs) - 1):
            line = funargs[i]
            fun_name = line.split(',')[0]
            var_type = line.split(',')[2]
            if config.function_name == fun_name:
                if var_type[0] == ' ': # The split from above sometimes contains an uneccessary blank space
                    var_type = var_type[1:]
                if var_type[-1] == '*':
                    var_type = var_type[0:-1]
                if var_type[-1] == ' ':
                    var_type = var_type[:-1]
                types.append(var_type)

    except: # During initialization, no funargs.txt exists
        for arg in config.function_args:
            types.append('long double')


    if config.error_type == 'highest_absolute' or config.error_type == 'highest_relative':
        err = ''

        for i in range(len(config.function_args)):
            arg = config.function_args[i]
            length = arg.length
            pointer = arg.ptr_type
            inputORoutput = arg.input_or_output

            if inputORoutput == 'output':
                if types[i] == 'long double':
                    varName = 'x_' + str(i)
                    err += '\tfor(int i = 0; i < ' + str(length) + '; i++){\n'
                    err += '\t\t\ttemp.v = ' + varName + '[i];\n'
                    err += '\t\t\tdd_I lower_bound = _ia_set_dd(temp.lh, temp.ll, -temp.lh, -temp.ll);\n'
                    err += '\t\t\tdd_I upper_bound = _ia_set_dd(-temp.uh, -temp.ul, temp.uh, temp.ul);\n'
                    if config.error_type == 'highest_relative':
                        err += '\t\t\tdd_I diff = _ia_div_dd(_ia_sub_dd(upper_bound, lower_bound), lower_bound);\n'
                    err += '\t\t\tif(_ia_cmpgt_dd(diff, diff_max)){\n'
                    err += '\t\t\t\tdiff_max = diff;\n'
                    err += '\t\t\t}\n'
                    err += '\t\t}\n'

                else:
                    varName = 'x_' + str(i)
                    err += '\tfor(int i = 0; i < ' + str(length) + '; i++){\n'

                    if types[i] == 'double':
                        err += '\t\t\tu_f64i temp;\n'
                        err += '\t\t\ttemp.v = ' + varName + '[i];\n'
                    else:
                        err += '\t\t\tf32_I temp;\n'
                        err += '\t\t\ttemp = ' + varName + '[i];\n'
                    err += '\t\t\tdd_I lower_bound = _ia_set_dd(temp.lo, ' + str(0) + ', -temp.lo, -' + str(0) + ');\n'
                    err += '\t\t\tdd_I upper_bound = _ia_set_dd(-temp.up, -' + str(0) + ', temp.up, ' + str(0) + ');\n'
                    if config.error_type == 'highest_relative':
                        err += '\tdd_I diff = _ia_div_dd(_ia_sub_dd(upper_bound, lower_bound), lower_bound);\n'
                    if input_dependent == True:
                        err += '\t\t\tif(_ia_cmpgt_dd(diff, diff_max)){\n'
                        err += '\t\t\t\tdiff_max = diff;\n'
                        err += '\t\t\t}\n'
                    else:
                        err += '\t\t\tif(j == 0)){\n'
                        err += '\t\t\t\tdiff_max = diff;\n'
                        err += '\t\t\t}\n'
                    err += '\t\t}\n'

        if config.return_info[0] == "True":
            ret = ''
            ret += '\ttemp.v = return_value;\n'
            ret += '\tdd_I lower_bound = _ia_set_dd(temp.lh, temp.ll, -temp.lh, -temp.ll);\n'
            ret += '\tdd_I upper_bound = _ia_set_dd(-temp.uh, -temp.ul, temp.uh, temp.ul);\n'
            if config.error_type == 'highest_relative':
                ret += '\tdd_I diff = _ia_div_dd(_ia_sub_dd(upper_bound, lower_bound), lower_bound);\n'
            if input_dependent == True:
                ret += '\tif(_ia_cmpgt_dd(diff, diff_max)){\n'
                ret += '\t\tdiff_max = diff;\n'
                ret += '\t}\n'
            else:
                ret += '\tif(j==0){\n'
                ret += '\t\tdiff_max = diff;\n'
                ret += '\t}\n'
            err += ret
    else:
        print("This error type is not supported:", err_type)
        sys.exit(-1)
    ans = ''
    ans += '\t}\n'
    ans += '\tchar* answer = "false";\n'
    ans += '\tdouble th = ' + str(10**(-config.precision)) + ';\n'
    ans += '\tif((int)_ia_cmpgt_dd(_ia_set_dd(-th, 0, th, 0), diff_max) == 1){\n'
    ans += '\t\tanswer = "true";\n'
    ans += '\t}\n'
    ans += '\tFILE* file = fopen("score.cov", "w");\n'
    ans += '\tfprintf(file, "%ld' + r"\\n" + '", diff_time);\n'
    ans += '\tfclose(file);\n'
    ans += '\tfile = fopen("sat.cov", "w");\n'
    ans += '\tfprintf(file, "%s' + r"\\n" + '", answer);\n'
    ans += '\tfclose(file);\n'
    ans += '\tfile = fopen("precision.cov", "w");\n'
    ans += '\tdouble prec = ((u_f64i)_ia_cast_dd_to_f64(diff_max)).up;\n'
    ans += '\tfprintf(file, "%.17g' + r"\\n" + '", prec);\n'
    ans += '\tfclose(file);\n'
    ans += '\tprintf("Time: %ld' + r"\\n" + '", diff_time);\n'
    #ans += '\tprintf("Accuracy constraint: %s' + r"\\n" + '", answer);\n'
    if config.return_info[0] == "True":
        ans += '\tfile = fopen("result.cov", "w");\n'
        ans += '\tfprintf(file, "result: %.17g' + r"\\n" + '", temp.uh);\n'
        ans += '\tfclose(file);\n'
    ans += '\tprintf("Accuracy: %.17g' + r"\\n" + '", prec);\n'

    code = err + ans

    c_new = re.sub(substitute, code, c_old)

    substitute = '#include "random_range.c"'
    code = '#include "cleaned_igen_random_range.c"'
    c_new = re.sub(substitute, code, c_new)

    substitute = '#include "' + config.file_name + '"'
    code = '#include "igen_chg_rmd_' + config.file_name + '"'


    c_new = re.sub(substitute, code, c_new)

    # Add IGen libraries, as sometimes IGen doesn't add them
    c_new = '#include "igen_math.h"\n' + c_new
    c_new = '#include "igen_dd_math.h"\n' + c_new

    with open(path + '/cleaned_igen_chg_main.c', 'w') as myfile:
        myfile.write(c_new)

def run(main_path, config_name, config):
    
    # Create main
    path = main_path + '/analysis_' + config_name + '/igen_setup'
    createMain(path, config)
    igen_src = getEnvVar('IGEN_PATH')
    call_background('cd ' + path + ' && python3 ' + igen_src + '/bin/igen.py chg_main.c')

    # add accuracy measurement
    cleanUp(path, config)
