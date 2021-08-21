#!/usr/bin/python

from helper import print_err, print_debug, call, call_background, getEnvVar, nameWithoutExtension, dockerCall, dockerCall30, dockerCall38, get_dynamic_score
import sys, re, json, os
import rsld
import create_main

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

    # clang is not happy about aligned_alloc not declared
    inc += 'void * aligned_alloc(size_t a, size_t b);\n'

    # Main init
    init = ''
    init += 'int main(){\n'
    init += '\tfesetround(FE_UPWARD);\n'
    init += '\tinitRandomSeed();\n'

    # Process arguments
    args = ''
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
            args += '\t' + type + '* x_' + str(i) + ';\n'
            args += '\tx_' + str(i) + ' = (' + type + ' *)aligned_alloc(32, ' + str(length) + ' * sizeof(' + type + '));\n' # sizeof(long double) potentially to big
            args += '\tfor(int i = 0; i < ' + str(length) + '; i++){\n'
            if is_input:
                if type == "long double" and config.input_precision == 'dd':
                    args += '\t\t' + type + ' h = getRandomDoubleDoubleInterval();\n'
                elif type == "double" or (type == "long double" and config.input_precision == 'd'):
                    args += '\t\t' + 'double' + ' h = getRandomDoubleInterval();\n'
                elif type == "float":
                    args += '\t\t' + type + ' h = getRandomFloatInterval();\n'
                else:
                    print('Type not recognized', type)
                    sys.exit(-1)
            else:
                args += '\t\t' + type + ' h = 0;\n'
            args += '\t\tx_' + str(i) + '[i] = h;\n'
            args += '\t}\n'

        else:
            print_err('Non pointer type as argument is not implemented yet: ' + arg.ptr_type)


    # Process return stmt
    if config.return_info[0] == "True":
        args += '\t' + config.return_info[1] + ' return_value = 0;\n'

    # Start Time measurement
    timeS = ''
    timeS += '\tclock_t start = clock();\n'
    timeS += '\tfor(long i = 0; i < ' + str(config.repetitions) + '; i++){\n'

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

    main = init + args + timeS + call + timeEnd + rep + main_end
    code = inc + main

    with open(os.path.join(prec_path, 'main.c'), 'w') as myfile:
        myfile.write(code)

# This function sets up Precimonious/HiFPTuner
def tuner_setup(main_path, config_name, config):

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

    elif config.tuning_algo == 'hifptuner':
        # Get some location
        src_path = getEnvVar('SOURCE_PATH') + '/src'
        hifp_path = os.path.join(config_folder_path, 'hifptuner_setup')
        file_name_wo_ext = nameWithoutExtension(config.file_name)
        shared_lib = '/root/precimonious/src/Passes.so'

        # Create folder for HiFPTuner and copy files into it
        call('mkdir ' + hifp_path)
        createMain(hifp_path, config)
        call('cp ' + os.path.join(src_path, 'random_range.c') + ' ' + hifp_path)
        call('cp ' + os.path.join(src_path, 'random_range_igen.c') + ' ' + hifp_path)
        call('cp ' + os.path.join(main_path, config.file_name) + ' ' + hifp_path)
        call('cp ' + src_path + '/normal_CMakeLists.txt ' + os.path.join(hifp_path, 'CMakeLists.txt'))

        # Prepare container for hifptuner
        dockerCall('rm -rf analysis')
        dockerCall('mkdir analysis')
        curr_path =  config_folder_path + '/hifptuner_setup/'
        call('docker cp ' + curr_path + config.file_name + ' hi:/root/analysis')
        call('docker cp ' + curr_path + 'main.c hi:/root/analysis')
        call('docker cp ' + curr_path + 'random_range.c hi:/root/analysis')

        # Run HiFPTuner
        dockerCall30('clang -emit-llvm -c ' + 'analysis/main.c' + ' -o ' + 'analysis/' + file_name_wo_ext + '.bc')
        dockerCall30('cd analysis && opt -load ' + shared_lib + ' -create-call-dependency '
        + file_name_wo_ext + '.bc --call-main ' + config.function_name + ' > '
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
        print_err('This tuning algorithm is not supported: ' + config.tuning_algo)

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
        print_err('This tuning algorithm is not supported: ' + config.tuning_algo)

    # Create folder for precimonious and copy files into it
    call('mkdir ' + igen_path)
    call('cp ' + src_path + '/random_range_igen.c ' + igen_path)
    #call('cp ' + tuner_path + '/main.c ' + igen_path) Dont use this anymore, create new main
    call('cp ' + os.path.join(main_folder, config.file_name) + ' ' + igen_path)
    if config.vectorized:
        cmake = '/igen_CMakeLists_vec.txt'
    else:
        cmake = '/igen_CMakeLists_novec.txt'
    call_background('cp ' + src_path + cmake + ' ' + os.path.join(igen_path, 'CMakeLists.txt'))

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
    config.repetitions = 1 # to measure time
    create_main.run(main_folder, config_name, config)

    # For some reason, the main file and function need to be renamed here (will be changed later)
    call('cp ' + config_folder_path + '/igen_setup/cleaned_igen_chg_main.c ' + config_folder_path + '/igen_setup/cleaned_igen_main.c')
    call('cp ' + config_folder_path + '/igen_setup/igen_rmd_' + config.file_name + ' ' + config_folder_path + '/igen_setup/igen_chg_rmd_' + config.file_name)

    # Test build and execution - measure runtime when there is one repetition
    call('cd ' + igen_path + ' && mkdir build && cd build && cmake .. && make && ./some_app')

    score = get_dynamic_score(igen_path + '/build/score.cov')
    factor = 1;
    MIN_RUNTIME = 100000
    if score < MIN_RUNTIME:
        if score == 0: # Rerun measurement with higher factor
            factor = MIN_RUNTIME
            config.repetitions = factor
            createChgMain.run(main_folder, config_name, config)
            call('cp ' + config_folder_path + '/igen_setup/cleaned_igen_chg_main.c ' + config_folder_path + '/igen_setup/cleaned_igen_main.c')
            call('cp ' + config_folder_path + '/igen_setup/igen_rmd_' + config.file_name + ' ' + config_folder_path + '/igen_setup/igen_chg_rmd_' + config.file_name)
            call('cd ' + igen_path + ' && mkdir build && cd build && cmake .. && make && ./some_app')

            score = get_dynamic_score(igen_path + '/build/score.cov')
            if score < MIN_RUNTIME:
                if score == 0:
                    factor = MIN_RUNTIME * MIN_RUNTIME
                else:
                    factor = int(MIN_RUNTIME / score) * MIN_RUNTIME


        else:
            factor = int(MIN_RUNTIME / score)
    print('factor:',factor, score)

    # Save new config to file
    config.repetitions = factor
    with open(main_folder + '/' + config_name + '.json', 'w') as myfile:
        myfile.write(config.get_config_as_string())



def run(main_folder, config_name, config):
    # Precimonious/HiFPTuner setup
    tuner_setup(main_folder, config_name, config)
    print_debug("Tuner setup finished.")

    # IGen setup
    igenSetup(main_folder, config_name, config)
    print_debug("IGen setup finished.")
