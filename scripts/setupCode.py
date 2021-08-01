#!/usr/bin/python

from helper import call, call_background, getEnvVar, nameWithoutExtension, dockerCall, dockerCall30, dockerCall38
import sys, re, json, os
import rsld
import createChgMain

def createMain(prec_path, config):

    # Includes
    inc = ''
    inc += '#include "random_range.c"\n'
    inc += '#include "' + config.file_name + '"\n'
    inc += '#include <time.h>\n'
    inc += '#include <stdio.h>\n'
    inc += '#include <fenv.h>\n'
    inc += '#include <stdlib.h>\n'
    inc += '#include <math.h>\n'
    #inc += '#include "igen_dd_lib.h"\n'
    includes = inc

    # Main init
    init = ''
    init += 'int main(){\n'
    init += '\tfesetround(FE_UPWARD);\n'
    init += '\tinitRandomSeed();\n'

    # Process arguments
    arg_code = ''
    for i in range(len(config.function_args)):

        # read argument
        arg = config.function_args[i]
        type = arg.type
        length = arg.length
        if arg.ptr_type == 'pointer':
            is_pointer = True
        else:
            is_pointer = False
        if arg.input_or_output == 'input':
            is_input = True
        elif arg.input_or_output == 'output':
            is_input = False
        else:
            print('Error in config file, inputoroutput:', arg.input_or_output)
            sys.exit(-1)

        # Write code for argument
        if is_pointer:
            input = ''
            input += '\t' + type + '* x_' + str(i) + ';\n'
            input += '\tx_' + str(i) + ' = aligned_alloc(32, ' + str(length) + ' * sizeof(' + type + '));\n' # sizeof(long double) potentially to big
            input += '\tfor(int i = 0; i < ' + str(length) + '; i++){\n'
            if is_input:
                if type == "long double" and config.input_precision == 'dd':
                    input += '\t\t' + type + ' h = getRandomDoubleDoubleInterval();\n'
                elif type == "double" or (type == "long double" and input_prec == 'd'):
                    input += '\t\t' + 'double' + ' h = getRandomDoubleInterval();\n'
                elif type == "float":
                    input += '\t\t' + type + ' h = getRandomFloatInterval();\n'
                else:
                    print('Type not recognized', type)
                    sys.exit(-1)
            else:
                input += '\t\t' + type + ' h = 0;\n'
            input += '\t\tx_' + str(i) + '[i] = h;\n'
            input += '\t}\n'

        else:
            print("Non pointer type as argument is not implemented yet:", arg.ptr_type)
            sys.exit(-1)


        arg_code += input

    # Process return stmt
    if config.return_info[0] == "True":
        ret_code = '\t' + config.return_info[1] + ' return_value = 0;\n'
    else:
        ret_code = ''

    # Start Time measurement
    timeS = ''
    timeS += '\tclock_t start = clock();\n'
    timeS += '\tfor(long i = 0; i < ' + str(config.repetitions) + '; i++){\n'
    timeStart = timeS

    # Function call
    arguments = ''
    if int(len(config.function_args)) >= 1:
        arguments += 'x_0'
    for i in range(1, int(len(config.function_args))):
        arguments += ', x_' + str(i)

    if config.return_info[0] == "True":
        call = '\t\treturn_value = ' + config.function_name + '(' + arguments + ');\n'
    else:
        call = '\t\t' + config.function_name + '(' + arguments + ');\n'

    # Stop Time measurement
    timeE = ''
    timeE += '\t}\n'
    timeE += '\tclock_t end = clock();\n'
    timeE += '\tlong diff_time = (long)(end - start);\n'
    timeE += '\tFILE* file = fopen("score.cov", "w");\n'
    timeE += '\tfprintf(file, "%ld\\n", diff_time);\n'
    timeE += '\tfclose(file);\n'
    timeEnd = timeE

    # Probably not necessary later
    rep = '\tprintf("BeforeIGenReplacement\\n");\n'

    main_end = '}\n'

    main = init + arg_code + ret_code + timeStart + call + timeEnd + rep + main_end
    code = includes + main

    with open(os.path.join(prec_path, 'main.c'), 'w') as myfile:
        myfile.write(code)


def precimoniousSetup(main_path, config_name, config):

    config_folder_path = main_path + '/analysis_' + config_name

    if config.tuning_algo == 'precimonious':
        # Get some important locations
        src_path = getEnvVar('SOURCE_PATH') + '/src'
        prec_path = os.path.join(config_folder_path, 'precimonious_setup')
        file_name_wo_ext = nameWithoutExtension(config.file_name)
        shared_lib = os.path.join(getEnvVar('CORVETTE_PATH'), 'src/Passes.so')

        # Create folder for precimonious and copy files into it
        call('mkdir ' + prec_path)
        call('cp ' + os.path.join(src_path, 'random_range.c') + ' ' + prec_path)
        call('cp ' + os.path.join(src_path, 'random_range_igen.c') + ' ' + prec_path)
        call('cp ' + os.path.join(main_path, config.file_name) + ' ' + prec_path)
        call('cp ' + src_path + '/normal_CMakeLists.txt ' + os.path.join(prec_path, 'CMakeLists.txt'))

        # Create main file for Precimonious setupCode
        createMain(prec_path, config)

        # Test build
        call_background('cd ' + prec_path + ' && mkdir build && cd build && cmake .. && make && ./some_app')

        # Precimonious calls, clang throws some WARNINGS!!!
        call('cd ' + prec_path + ' && clang -emit-llvm -c ' + 'main.c' + ' -o '
        + file_name_wo_ext + '.bc')
        call('cd ' + prec_path + ' && opt -load ' + shared_lib + ' -create-call-dependency '
        + file_name_wo_ext + '.bc --call-main ' + config.function_name + ' > '
        + file_name_wo_ext +  '.tmp')
        call('rm ' + prec_path + '/' + file_name_wo_ext +  '.tmp')
        call('touch ' + os.path.join(prec_path, 'exclude.txt')) # would allow to exclude variables from analysis
        call('cd ' + prec_path + ' && opt -load ' + shared_lib + ' -config-file --only-arrays --only-scalars --funs --pformat '
        + file_name_wo_ext + '.bc --filename config_' + file_name_wo_ext + '.json > '
        + file_name_wo_ext + '.tmp')
        call('rm ' + prec_path + '/' + file_name_wo_ext +  '.tmp')
        call('cd ' + prec_path + ' && opt -load ' + shared_lib + ' -search-file --original-type --only-arrays --only-scalars --funs '
        + file_name_wo_ext + '.bc --filename search_' + file_name_wo_ext + '.json > '
        + file_name_wo_ext +  '.tmp')
        call('rm ' + prec_path + '/' + file_name_wo_ext +  '.tmp')

    # not working now
    elif tuning == 'hifptuner':
        # Get some location
        src_path = getEnvVar('SOURCE_PATH') + '/src'
        hifp_path = os.path.join(config_folder_path, 'hifptuner_setup')
        file_name_wo_ext = nameWithoutExtension(file_name)
        shared_lib = '/root/precimonious/src/Passes.so'

        # Create folder for HiFPTuner and copy files into it
        call('mkdir ' + hifp_path)
        createMain(hifp_path, file_name, function_name, args, ret, rep, input_prec)
        call('cp ' + os.path.join(src_path, 'random_range.c') + ' ' + hifp_path)
        call('cp ' + os.path.join(src_path, 'random_range_igen.c') + ' ' + hifp_path)
        call('cp ' + os.path.join(main_path, file_name) + ' ' + hifp_path)
        call('cp ' + src_path + '/normal_CMakeLists.txt ' + os.path.join(hifp_path, 'CMakeLists.txt'))

        # Prepare container for hifptuner
        dockerCall('rm -rf analysis')
        dockerCall('mkdir analysis')
        curr_path =  config_folder_path + '/hifptuner_setup/'
        call('docker cp ' + curr_path + file_name + ' hi:/root/analysis')
        call('docker cp ' + curr_path + 'main.c hi:/root/analysis')
        call('docker cp ' + curr_path + 'random_range.c hi:/root/analysis')

        # Run HiFPTuner
        dockerCall30('clang -emit-llvm -c ' + 'analysis/main.c' + ' -o ' + 'analysis/' + file_name_wo_ext + '.bc')
        dockerCall30('cd analysis && opt -load ' + shared_lib + ' -create-call-dependency '
        + file_name_wo_ext + '.bc --call-main ' + function_name + ' > '
        + file_name_wo_ext +  '.tmp')
        dockerCall('rm /root/analysis/' + file_name_wo_ext +  '.tmp')
        dockerCall('touch analysis/exclude.txt')
        dockerCall30('cd analysis && opt -load ' + shared_lib + ' -config-file --only-arrays --only-scalars --funs --pformat '
        + file_name_wo_ext + '.bc --filename config_' + file_name_wo_ext + '.json > '
        + file_name_wo_ext + '.tmp')
        dockerCall('rm /root/analysis/' + file_name_wo_ext +  '.tmp')
        dockerCall30('cd analysis && opt -load ' + shared_lib + ' -search-file --original-type --only-arrays --only-scalars --funs '
        + file_name_wo_ext + '.bc --filename search_' + file_name_wo_ext + '.json > '
        + file_name_wo_ext +  '.tmp')
        dockerCall('rm /root/analysis/' + file_name_wo_ext +  '.tmp')
        dockerCall30('cd analysis && ../HiFPTuner/scripts/compile.sh ' + file_name_wo_ext + '.bc')
        dockerCall38('cd analysis && ../HiFPTuner/scripts/analyze.sh json_' + file_name_wo_ext + '.bc')
        dockerCall38('cd analysis && python -O ../HiFPTuner/src/graphAnalysis/varDepGraph_pro.py')

        # Get configs out of docker
        call('docker cp hi:/root/analysis/ ' + hifp_path)
        call('mv ' + hifp_path + '/analysis/* ' + hifp_path)
        call('rm -r ' + hifp_path + '/analysis')

    else:
        print("This tuning algorithm is not supported:", tuning)
        sys.exit(-1)

# def addPrecisionSupport(file_name, prec_path, igen_path, err_type, args, ret, precision):
#
#     # Open main code from precimonios folder
#     with open(igen_path + '/igen_main.c', 'r') as myfile:
#         code_old = myfile.read()
#
#     # This string gets substituted in the main file
#     substitute = '  printf\("BeforeIGenReplacement' + r'\\' + 'n"\);'
#
#     # Simplest Error type
#     if err_type == 'highestAbsolute':
#
#         # Decl
#         decl = '\tu_ddi temp;\n'
#
#         # Error Intro
#         pre_err1 = '\tint max = 0;\n'
#         pre_err2 = '\tint imax = 0;\n'
#         pre_err3 = '\tdd_I diff_max = _ia_zero_dd();\n'
#         err = decl + pre_err1 + pre_err2 + pre_err3
#
#         # Iterate over all arguments, add error for each output argument
#         for i in range(len(args)):
#             arg = args[i]
#
#             # read argument
#             type = arg[0]
#             length = arg[1]
#             if arg[2] == 'pointer':
#                 is_pointer = True
#             else:
#                 is_pointer = False
#             if arg[3] == 'input':
#                 is_input = True
#             else:
#                 is_input = False
#
#             if not is_input:
#                 if type == "long double":
#                     varName = 'x_' + str(i)
#                     err1 = '\tfor(int i = 0; i < ' + str(length) + '; i++){\n'
#                     err1 += '\ttemp.v = ' + varName + '[i];\n'
#                     err2 = '\t\tdd_I lower_bound = _ia_set_dd(' + 'temp' + '.lh, ' + 'temp' + '.ll, -' + 'temp' + '.lh, -' + 'temp' + '.ll);\n'
#                     err3 = '\t\tdd_I upper_bound = _ia_set_dd(-' + 'temp' + '.uh, -' + 'temp' + '.ul, ' + 'temp' + '.uh, ' + 'temp' + '.ul);\n'
#                     err4 = '\t\tdd_I diff = _ia_sub_dd(upper_bound, lower_bound);\n'
#                     err5 = '\t\tif(_ia_cmpgt_dd(diff, diff_max)){\n'
#                     err6 = '\t\t\tdiff_max = diff;\n'
#                     err7 = '\t\t\tmax = i;\n'
#                     err8 = '\t\t}\n'
#                     err9 = '\t}\n'
#                     err += err1 + err2 + err3 + err4 + err5 + err6 + err7 + err8 + err9
#                 else:
#                     varName = 'x_' + str(i)
#                     err1 = '\tfor(int i = 0; i < ' + str(length) + '; i++){\n'
#
#                     if types[i] == 'double':
#                         err1 += '\tu_f64i temp;\n'
#                         err1 += 'temp.v = ' + varName + '[i];\n'
#                     else:
#                         err1 += '\tf32_I temp;\n'
#                         err1 += 'temp = ' + varName + '[i];\n'
#                     err2 = '\t\tdd_I lower_bound = _ia_set_dd(' + 'temp' + '.lo, ' + str(0) + ', -' + 'temp' + '.lo, -' + str(0) + ');\n'
#                     err3 = '\t\tdd_I upper_bound = _ia_set_dd(-' + 'temp' + '.up, -' + str(0) + ', ' + 'temp' + '.up, ' + str(0) + ');\n'
#                     err4 = '\t\tdd_I diff = _ia_sub_dd(upper_bound, lower_bound);\n'
#                     err5 = '\t\tif(_ia_cmpgt_dd(diff, diff_max)){\n'
#                     err6 = '\t\t\tdiff_max = diff;\n'
#                     err7 = '\t\t\tmax = i;\n'
#                     err8 = '\t\t}\n'
#                     err9 = '\t}\n'
#                     err += err1 + err2 + err3 + err4 + err5 + err6 + err7 + err8 + err9
#
#         # Add error for return value
#         if ret[0] == "True":
#             ret1 = '\ttemp.v = ' + 'return_value' + ';\n'
#             ret1 += '\tdd_I lower_bound = _ia_set_dd(' + 'temp' + '.lh, ' + 'temp' + '.ll, -' + 'temp' + '.lh, -' + 'temp' + '.ll);\n'
#             ret2 = '\tdd_I upper_bound = _ia_set_dd(-' + 'temp' + '.uh, -' + 'temp' + '.ul, ' + 'temp' + '.uh, ' + 'temp' + '.ul);\n'
#             ret3 = '\tdd_I diff = _ia_sub_dd(upper_bound, lower_bound);\n'
#             ret4 = '\tif(_ia_cmpgt_dd(diff, diff_max)){\n'
#             ret5 = '\t\tdiff_max = diff;\n'
#             ret6 = '\t\tmax = -1;\n'
#             ret7 = '\t}\n'
#             err += ret1 + ret2 + ret3 + ret4 + ret5 + ret6 + ret7
#
#     else:
#         print("This error type is currently not supported:", err_type)
#         sys.exit(-1)
#
#     ans1 = '\tchar* answer = "false";\n'
#     ans2 = '\tdouble th = ' + str(10**(-precision)) + ';\n'
#     ans3 = '\tif((int)_ia_cmpgt_dd(_ia_set_dd(-th, 0, th, 0), diff_max) == 1){\n'
#     ans4 = '\t\tanswer = "true";\n'
#     ans5 = '\t}\n'
#     ans6 = '\tfile = fopen("sat.cov", "w");\n'
#     ans7 = '\tfprintf(file, "%s' + r"\\n" + '", answer);\n'
#     ans8 = '\tfclose(file);\n'
#     ans9 = '\tfile = fopen("precision.cov", "w");\n'
#     ans10 = '\tdouble prec = ((u_f64i)_ia_cast_dd_to_f64(diff_max)).up;\n'
#     ans11 = '\tfprintf(file, "%.17g' + r"\\n" + '", prec);\n'
#     ans12 = '\tprintf("Precision constraint: %s' + r"\\n" + '", answer);\n'
#     ans = ans1 + ans2 + ans3 + ans4 + ans5 + ans6 + ans7 + ans8 + ans9 + ans10 + ans11 + ans12
#
#     print = '\tprintf("Precision: %.17g' + r"\\n" + '", prec);\n'
#     code_replace = err + ans + print
#
#     # Substitue error analysis
#     code_new = re.sub(substitute, code_replace, code_old)
#
#     # Substitute headers
#     substitute = '#include "random_range.c"'
#     code_replace = '#include "random_range_igen.c"'
#     code_new = re.sub(substitute, code_replace, code_new)
#
#     substitute = '#include "' + file_name + '"'
#     code_replace = '#include "igen_rmd_' + file_name + '"'
#     code_new = re.sub(substitute, code_replace, code_new)
#
#     with open(igen_path + '/cleaned_igen_main.c', 'w') as myfile:
#         myfile.write(code_new)

# def fixHeaderIssue(igen_path, file_name):
#     with open(igen_path + '/main.c', 'r') as myfile:
#         code_old = myfile.read()
#
#     substitute = '#include "random_range.c"'
#     code_replace = '#include "random_range_igen.c"'
#     code_new = re.sub(substitute, code_replace, code_old)
#
#     with open(igen_path + '/main.c', 'w') as myfile:
#         myfile.write(code_new)
#
#     chg_file_name = 'igen_rmd_' + file_name
#
#     with open(igen_path + '/' + chg_file_name, 'r') as myfile:
#         code_old = myfile.read()
#
#     #inc1 = '#include "igen_lib.h"\n'
#     #inc2 = '#include "igen_dd_lib.h"\n'
#     inc1 = '#include "igen_math.h"\n'
#     inc2 = '#include "igen_dd_math.h"\n'
#
#     code_new = inc1 + inc2 + code_old
#
#     with open(igen_path + '/' + chg_file_name, 'w') as myfile:
#         myfile.write(code_new)

def igenSetup(main_folder, config_name, config):

    # Get some important locations
    config_folder_path = main_folder + '/analysis_' + config_name
    src_path = getEnvVar('SOURCE_PATH') + '/src'
    igen_src = getEnvVar('IGEN_PATH')
    igen_path = os.path.join(config_folder_path, 'igen_setup') # Folder for newly creaded IGen files
    prec_path = os.path.join(config_folder_path, 'precimonious_setup')
    hifp_path = os.path.join(config_folder_path, 'hifptuner_setup')
    if config.tuning_algo == 'precimonious':
        tuner_path = prec_path
    elif config.tuning_algo == 'hifptuner':
        tuner_path = hifp_path
    else:
        print('This tuning algorithm is not supported:', config.tuning_algo)
        sys.exit(-1)

    # Create folder for precimonious and copy files into it
    call('mkdir ' + igen_path)
    call('cp ' + src_path + '/random_range_igen.c ' + igen_path)
    #call('cp ' + tuner_path + '/main.c ' + igen_path) Dont use this anymore, create new main
    call('cp ' + os.path.join(main_folder, config.file_name) + ' ' + igen_path)
    if config.vectorized:
        cmake = '/igen_CMakeLists_vec.txt'
    else:
        cmake = '/igen_CMakeLists_novec.txt'
    call('cp ' + src_path + cmake + ' ' + os.path.join(igen_path, 'CMakeLists.txt'))

    # Add rng range constraint to random_range_igen.c
    with open(igen_path + '/random_range_igen.c', 'r') as myfile:
        code_old = myfile.read()
    substitute = 'int factor = 1;'
    code_replace = 'int factor = ' + str(config.rng_range) + ';'
    code_new = re.sub(substitute, code_replace, code_old)
    with open(igen_path + '/random_range_igen.c', 'w') as myfile:
        myfile.write(code_new)

    # Remove same line declarations from source file
    rsld.run(igen_path, config.file_name)

    # Call IGen on source file
    call_background('cd ' + igen_path + ' && python3 ' + igen_src + '/bin/igen.py rmd_' + config.file_name)

    # Create main file
    createChgMain.run(main_folder, config_name, config)

    #DONT USE THIS ANYMORE!! use code frome createChgMain.py instead
    # Add precision support
    #fixHeaderIssue(igen_path, config.file_name)
    #call_background('cd ' + igen_path + ' && python3 ' + igen_src + '/bin/igen.py main.c')
    #addPrecisionSupport(file_name, tuner_path, igen_path, err_type, args, ret, precision)

    # For some reason, the main file and function need to be renamed here (will be changed later)
    call('cp ' + config_folder_path + '/igen_setup/cleaned_igen_chg_main.c ' + config_folder_path + '/igen_setup/cleaned_igen_main.c')
    call('cp ' + config_folder_path + '/igen_setup/igen_rmd_' + config.function_name + '.c ' + config_folder_path + '/igen_setup/igen_chg_rmd_' + config.function_name + '.c')

    # Test build and execution
    call('cd ' + igen_path + ' && mkdir build && cd build && cmake .. && make && ./some_app')

# Function from precimonious
def get_dynamic_score(path):
  scorefile = open(path)
  score = scorefile.readline()
  score = score.strip()
  return int(score)


def run(main_folder, config_name, config):

    # Precimonious/HiFPTuner setup
    precimoniousSetup(main_folder, config_name, config)
    print("Precimonious setup finished.")

    # IGen setup
    igenSetup(main_folder, config_name, config)
    print("IGen setup finished.")

    print('until heere 2')
    sys.exit(-1)

    # Test runtime, to find an adequate number of repetitions (later add only do this if rep == 0)
    igen_path = os.path.join(config_folder_path, 'igen_setup') # Folder for newly creaded IGen files
    prec_path = os.path.join(config_folder_path, 'precimonious_setup')
    hifp_path = os.path.join(config_folder_path, 'hifptuner_setup')

    if tuning == 'precimonious':
        tuner_path = prec_path
    else:
        tuner_path = hifp_path

    with open(main_path + '/std_config.json') as myfile:
        text = myfile.read()

    substitute = '"repetitions": ' + r"[0-9]+" + ','
    replace = '"repetitions": 1,'

    text_new = re.sub(substitute, replace, text)

    print(text_new)
    print(config_folder_path)
    print(file_name)


    with open(main_path + '/std_config.json', 'w') as myfile:
        myfile.write(text_new)

    print('start')

    call('cd ' + igen_path + ' && mkdir build && cd build && cmake .. && make && ./some_app')
    score = get_dynamic_score(igen_path + '/build/score.cov')
    print(igen_path + '/build/score.cov')
    factor = 1
    print('score', score)
    if score < 10000:
        factor = int(10000 / score)

    with open(main_path + '/' + config_name + '.json') as myfile:
        text = myfile.read()

    substitute = '"repetitions": ' + r"[0-9]+" + ','
    replace = '"repetitions": ' + str(factor) + ','

    text_new = re.sub(substitute, replace, text)

    with open(main_path + '/' + config_name + '.json', 'w') as myfile:
        myfile.write(text_new)

    print(text_new)
