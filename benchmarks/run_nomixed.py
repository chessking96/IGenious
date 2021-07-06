#!/usr/bin/python
import sys, os, re
sys.path.insert(1, os.path.join(sys.path[0], '../scripts'))
import setupCode, changeTypes, rsld, createChgMain
from helper import call, readConfig, json, getEnvVar, nameWithoutExtension, call_background

src_path = getEnvVar('SOURCE_PATH') + '/src'
scripts_path = getEnvVar('SOURCE_PATH') + '/scripts'

#folders = ['DFT16', 'DFT16dd', 'dot', 'matmul', 'simpsons']
#folders = ['newton_root', 'funarc', 'DFT16', 'DFT16dd', 'dot', 'matmul', 'simpsons', 'bisection_root']
#file_names = ['newton_root.c', 'funarc.c', 'DFT16.c', 'DFT16.c', 'dot.c', 'matmul.c', 'simpsons.c', 'bisection_root.c']

folders = ['dot']

types = ['dd', 'd', 'f']
vectorized = [True, False]
input_ranges = [1, 10, 100]
input_precisions = ['dd', 'd']
error_types = ['highestAbsolute']
max_iter = 1

for err in error_types:
    for input_precision in input_precisions:
        for input_range in input_ranges:
            for vec in vectorized:
                for type in types:
                    for folder in folders:
                        print('Run:', folder, input_precision, input_range, vec, type)

                        # Read standard config
                        path_folder = 'examples/' + folder
                        file_name, function_name, args, ret, rep, prec, _err_type, _use_vectorized, _max_iter, tuning, _input_prec, _input_range = readConfig(path_folder + '/std_config.json')

                        # Create new folder
                        config_name = input_precision + '#' + str(input_range) + '#' + type
                        path = path_folder + '/no_mixed/' + config_name
                        corvette_path = getEnvVar('CORVETTE_PATH') # precimonious path
                        igen_src = getEnvVar('IGEN_PATH')
                        if vec:
                            config_name += '#vec'

                        call('rm -rf ' + path)
                        call('mkdir ' + path)

                        # Copy CMakeLists.txt, random_number_generator
                        call('cp ' + src_path + '/random_range_igen.c ' + path)
                        call('cp ' + src_path + '/random_range.c ' + path)
                        if vec:
                            call('cp ' + src_path + '/igen_CMakeLists_vec.txt ' + path + '/CMakeLists.txt')
                        else:
                            call('cp ' + src_path + '/igen_CMakeLists_novec.txt ' + path + '/CMakeLists.txt')


                        new_config = '{\n'
                        new_config += '\t"filename": "' + file_name + '",\n'
                        new_config += '\t"functionname": "' + function_name + '",\n'
                        new_config += '\t"args": ' + str(args) + ',\n'
                        new_config += '\t"return": ' + json.dumps(ret) + ',\n'
                        new_config += '\t"repetitions": ' + str(rep) + ',\n'
                        new_config += '\t"precision": ' + str(prec) + ',\n'
                        new_config += '\t"errortype": "' + err + '",\n'
                        new_config += '\t"vectorized": "' + str(vec) + '",\n'
                        new_config += '\t"maxpreciterations": ' + str(max_iter) + ',\n'
                        new_config += '\t"tuning": "' + tuning + '",\n'
                        new_config += '\t"input_prec": "' + input_precision + '",\n'
                        new_config += '\t"input_range": ' + str(input_range)
                        new_config += '}'

                        with open(path + '/config.json', 'w') as myfile:
                            myfile.write(new_config)


                        setupCode.createMain(path, file_name, function_name, args, ret, rep, input_precision)

                        # Copy code
                        file_name_wo_ext = nameWithoutExtension(file_name)
                        shared_lib = os.path.join(getEnvVar('CORVETTE_PATH'), 'src/Passes.so')

                        call('cp ' + path_folder + '/' + file_name + ' ' + path)


                        # Precimonious config file
                        call('cd ' + path + ' && clang -emit-llvm -c ' + 'main.c' + ' -o ' + file_name_wo_ext + '.bc')
                        call('cd ' + path + ' && opt -load ' + shared_lib + ' -create-call-dependency '
                        + file_name_wo_ext + '.bc --call-main ' + function_name + ' > '
                        + file_name_wo_ext +  '.tmp')
                        call('rm ' + path + '/' + file_name_wo_ext +  '.tmp')
                        call('touch ' + os.path.join(path, 'exclude.txt')) # would allow to exclude variables from analysis
                        call('cd ' + path + ' && opt -load ' + shared_lib + ' -config-file --only-arrays --only-scalars --funs --pformat '
                        + file_name_wo_ext + '.bc --filename config_' + file_name_wo_ext + '.json > '
                        + file_name_wo_ext + '.tmp')
                        call('rm ' + path + '/' + file_name_wo_ext +  '.tmp')
                        call('cd ' + path + ' && opt -load ' + shared_lib + ' -search-file --original-type --only-arrays --only-scalars --funs '
                        + file_name_wo_ext + '.bc --filename search_' + file_name_wo_ext + '.json > '
                        + file_name_wo_ext +  '.tmp')
                        call('rm ' + path + '/' + file_name_wo_ext +  '.tmp')

                        # Create config file
                        call('cd ' + path + ' && python2 -O ' + corvette_path
                        + '/scripts/dd2_minimal.py search_' + file_name_wo_ext
                        + '.json config_' + file_name_wo_ext + '.json ')

                        # Change types in temp config
                        with open(path + '/config_temp.json', 'r') as myfile:
                            text_old = myfile.read()

                        substitute = 'longdouble'
                        if type == 'd':
                            replace = 'double'
                        elif type == 'f':
                            replace = 'float'
                        else:
                            replace = 'longdouble'
                        text_new = re.sub(substitute, replace, text_old)

                        with open(path + '/config_temp.json', 'w') as myfile:
                            myfile.write(text_new)

                        # Change types of file
                        # Make sure, that the clang_ast_vistor latest version is compiled
                        call_background('cd ' + scripts_path + '/changeTypes && cmake . && make')

                        # Run clang_ast_visitor
                        rsld.run(path, file_name)
                        call('cd ' + path + ' && ' + scripts_path + '/changeTypes/clang_ast_visitor rmd_' + file_name + ' -- ' + ' > chg_rmd_' + file_name)

                        # Run IGen
                        call_background('python ' + igen_src + '/bin/igen.py ' + path + '/chg_rmd_' + file_name)

                        # create main file
                        call('cp ' + path + '/funargs.txt .')
                        main_path = '' # probably useless argument


                        createChgMain.createMain(file_name, function_name, args, ret, rep, input_precision)
                        call('mv chg_main.c ' + path)
                        call_background('cd ' + path + ' && python3 ' + igen_src + '/bin/igen.py chg_main.c')
                        call('cp ' + path + '/igen_chg_main.c .')
                        createChgMain.cleanUp(file_name, function_name, err, args, ret, prec)

                        call('rm -rf funargs.txt')
                        call('rm -rf igen_chg_main.c')

                        call('mv cleaned_igen_chg_main.c ' + path + '/cleaned_igen_main.c')

                        # compile
                        call_background('cd ' + path + ' && mkdir build && cd build && cmake .. && make')

                        # execute
                        call('cd ' + path + '/build && ./some_app')
