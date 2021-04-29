from helper import call, getEnvVar, nameWithoutExtension
import sys, re

def createMain():
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

    input = ''
    if is_input:
        input1 = '\tlong double* x = malloc(' + str(num_input) + ' * sizeof(long double));\n'
        input2 = '\tfor(int i = 0; i < ' + str(num_input) + '; i++){\n'
        input3 = '\t\tlong double h = getRandomDouble();\n'
        input4 = '\t\tx[i] = h;\n'
        input5 = '\t}\n'
        input = input1 + input2 + input3 + input4 + input5

    output = ''
    if is_output:
        output1 = '\tlong double* y = malloc(' + str(num_output) + ' * sizeof(long double));\n'
        output = output1

    timeS1 = '\tclock_t start = clock();\n'
    timeS2 = '\tfor(int i = 0; i < ' + str(repetitions) + '; i++){\n'
    timeS = timeS1 + timeS2

    arguments = ''
    if is_output:
        arguments += 'y'
    if is_input:
        arguments += ', x'

    call = '\t\t' + function_name + '(' + arguments + ');\n'

    timeE1 = '\t}\n'
    timeE2 = '\tclock_t end = clock();\n'
    timeE3 = '\tlong diff_time = (long)(end-start);\n'
    timeE4 = '\tFILE* file = fopen("score.cov", "w");\n'
    timeE5 = '\tfprintf(file, "%ld\\n", diff_time);\n'
    timeE6 = '\tfclose(file);\n'
    timeE = timeE1 + timeE2 + timeE3 + timeE4 + timeE5 + timeE6

    rep = '\tprintf("BeforeIGenReplacement");\n'

    main_end = '}\n'

    main = main_start + init + input + output + timeS + call + timeE + rep + main_end
    code = include + main

    with open (file_path + 'main.c', 'w') as myfile:
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
        call('python3 ' + scripts_path + '/multidecl.py ' + file_path + 'IGen/ ' + file_name)
        call('cd ' + file_path + 'IGen && python3 ' + igen_path + '/bin/igen.py main.c')
        call('cd ' + file_path + 'IGen && python3 ' + igen_path + '/bin/igen.py random_range.c')
        call('cd ' + file_path + 'IGen && python3 ' + igen_path + '/bin/igen.py rmd_' + file_name)

        call('cp ' + src_path + '/igen_CMakeLists.txt ' + file_path + 'IGen/CMakeLists.txt')

def cleanUp():
    # main
    with open(file_path + 'IGen/igen_main.c', 'r') as myfile:
        c_old = myfile.read()
    substitute = 'printf\("BeforeIGenReplacement"\);'

    err1 = '\tint max = 0;\n'
    err2 = '\tdd_I diff_max = _ia_zero_dd();\n'
    err3 = '\tfor(int i = 0; i < ' + str(num_output) + '; i++){\n'
    err4 = '\t\tdd_I lower_bound = _ia_set_dd(y[i].lh, y[i].ll, -y[i].lh, -y[i].ll);\n'
    err5 = '\t\tdd_I upper_bound = _ia_set_dd(-y[i].uh, -y[i].ul, y[i].uh, y[i].ul);\n'
    err6 = '\t\tdd_I diff = _ia_sub_dd(upper_bound, lower_bound);\n'
    err7 = '\t\tif(_ia_cmpgt_dd(diff, diff_max)){\n'
    err8 = '\t\t\tdiff_max = diff;\n'
    err9 = '\t\t\tmax = i;\n'
    err10 = '\t\t}\n'
    err11 = '\t}\n'
    err = err1 + err2 + err3 + err4 + err5 + err6 + err7 + err8 + err9 + err10 + err11

    ans1 = '\tchar* answer = "false";\n'
    ans2 = '\tdouble th = ' + str(precision) + ';\n'
    ans3 = '\tprintf("%i' + r"\\n" + '", (int)_ia_cmpgt_dd(_ia_set_dd(-th, 0, th, 0), diff_max));\n'
    ans4 = '\tif((int)_ia_cmpgt_dd(_ia_set_dd(-th, 0, th, 0), diff_max) == 1){\n'
    ans5 = '\t\tanswer = "true";\n'
    ans6 = '\t}\n'
    ans7 = '\tfile = fopen("sat.cov", "w");\n'
    ans8 = '\tfprintf(file, "%s' + r"\\n" + '", answer);\n'
    ans9 = '\tfclose(file);\n'
    ans = ans1 + ans2 + ans3 + ans4 + ans5 + ans6 + ans7 + ans8 + ans9

    p1 = '\tprintf("1: %.20f %.20f' + r"\\n" + '", y[max].lh, y[max].ll);\n'
    p2 = '\tprintf("2: %.20f %.20f' + r"\\n" + '", y[max].uh, y[max].ul);\n'
    p3 = '\tprintf("3: %.20f %.20f' + r"\\n" + '", diff_max.lh, diff_max.ll);\n'
    p4 = '\tprintf("4: %.20f %.20f' + r"\\n" + '", diff_max.uh, diff_max.ul);\n'
    p = p1 + p2 + p3 + p4

    code = err + ans + p

    c_new = re.sub(substitute, code, c_old)

    substitute = '#include "random_range.c"'
    code = '#include "cleaned_igen_random_range.c"'
    c_new = re.sub(substitute, code, c_new)

    substitute = '#include "' + file_name + '"'
    code = '#include "igen_chg_rmd_' + file_name + '"'
    c_new = re.sub(substitute, code, c_new)

    with open(file_path + 'IGen/cleaned_igen_main.c', 'w') as myfile:
        myfile.write(c_new)

    # random_range
    c1 = '#include <stdlib.h>\n'
    c2 = 'void initRandomSeed(){\n'
    c3 = '\tsrand(42);\n'
    c4 = '}\n'
    c5 = 'dd_I getRandomDouble() {\n'
    c6 = '\tlong double r1 = ((long double)rand())/(RAND_MAX);\n'
    c7 = '\tlong double r2 = ((long double)rand())/(RAND_MAX);\n'
    c8 = '\treturn _ia_set_dd(-r1, -r2, r1, r2);\n'
    c9 = '}\n'

    c = c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8 + c9


    with open (file_path + 'IGen/cleaned_igen_random_range.c', 'w') as myfile:
            myfile.write(c)

if __name__ == "__main__":
    is_input = False
    num_input = 32
    is_output = True
    num_output = 32
    repetitions = 1
    precision = 0.0000001

    # arguments: filepath filename, functionname
    if len(sys.argv) != 4:
        print("Wrong number of arguments.")
        sys.exit(-1)

    file_path = sys.argv[1] + 'analysis/'
    file_name = sys.argv[2]
    function_name = sys.argv[3]

    nameWOExt = nameWithoutExtension(file_name)
    prec_path = getEnvVar('CORVETTE_PATH') # path to precimonious
    scripts_path = getEnvVar('SOURCE_PATH') + '/scripts' # path to scripts
    src_path = getEnvVar('SOURCE_PATH') + '/src'
    igen_path = getEnvVar('IGEN_PATH')
    shared_lib = prec_path + '/src/Passes.so'

    createMain()
    precimoniousSetup()
    print("Precimonious setup finished.")
    igenSetup()
    cleanUp()
    print("IGen setup finished.")
