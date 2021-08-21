#!/usr/bin/python
import sys, os, re
sys.path.insert(1, os.path.join(sys.path[0], '../scripts'))
import rsld, create_main
from helper import print_debug, call, Config, json, getEnvVar, nameWithoutExtension, call_background, get_dynamic_score
import setup_igenious

src_path = getEnvVar('SOURCE_PATH') + '/src'
scripts_path = getEnvVar('SOURCE_PATH') + '/scripts'

fast = True

if fast:
    folders = ['arclength', 'linear', 'newton_root', 'DFT16', 'dot', 'matmul', 'simpsons']
    types = ['dd', 'd', 'f']
    vectorized = [True]
    input_ranges =  [10]
    input_precisions = ['dd']
    error_types = ['highestAbsolute']
else:
    folders = ['arclength', 'linear', 'newton_root', 'DFT16', 'dot', 'matmul', 'simpsons']
    types = ['dd', 'd', 'f']
    vectorized = [True, False]
    input_ranges =  [10]
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
                        main_folder = 'examples/' + folder
                        config = Config.read_config_from_file(main_folder + '/std_config.json')
                        config.error_type = err
                        config.input_precision = input_precision
                        config.vectorized = vec
                        config.max_iterations = max_iter
                        config.rng_range = input_range
                        config.tuning_algo = 'precimonious'
                        config.repetitions = 1

                        # Create new folder
                        config_name = 'non_mixed_' + input_precision + '#' + str(input_range) + '#' + type
                        if vec:
                            config_name += '#vec'
                        config_folder = main_folder + '/analysis_' + config_name
                        corvette_path = getEnvVar('CORVETTE_PATH') # precimonious path
                        igen_src = getEnvVar('IGEN_PATH')

                        new_config = config.get_config_as_string()
                        with open(main_folder + '/' + config_name + '.json', 'w') as myfile:
                            myfile.write(new_config)

                        # Delete old run (may or may not exist) and create new folder
                        print_debug('Cleaning up directory')
                        call('rm -rf ' + config_folder)
                        call('mkdir ' + config_folder)
                        # Run setup
                        print_debug('Run setup')
                        setup_igenious.run(main_folder, config_name, config)

                        # Run precimonious once to get some files
                        tuner_folder_name = '/precimonious_setup'
                        tuner_path = config_folder + tuner_folder_name
                        file_name_wo = nameWithoutExtension(config.file_name)
                        path = main_folder
                        config_file = config_name + '.json'
                        corvette_path = getEnvVar('CORVETTE_PATH') # precimonious path

                        call_background('cd ' + tuner_path + ' && python2 -O ' + corvette_path
                        + '/scripts/dd2.py ' + file_name_wo + '.bc search_' + file_name_wo
                        + '.json config_' + file_name_wo + '.json ' + path + ' ' + config_file + ' ' + str(config.max_iterations))

                        # Replace all types
                        # Change types in temp config
                        with open(config_folder + '/precimonious_setup/config_temp.json', 'r') as myfile:
                            text_old = myfile.read()

                        substitute = 'longdouble'
                        if type == 'd':
                            replace = 'double'
                        elif type == 'f':
                            replace = 'float'
                        else:
                            replace = 'longdouble'
                        text_new = re.sub(substitute, replace, text_old)

                        with open(config_folder + '/precimonious_setup/config_temp.json', 'w') as myfile:
                            myfile.write(text_new)

                        # changeTypes
                        file_name = config.file_name
                        scripts_path = getEnvVar('SOURCE_PATH') + '/scripts'
                        igen_src = getEnvVar('IGEN_PATH')

                        # Make sure, that the clang_ast_vistor latest version is compiled
                        call_background('cd ' + scripts_path + '/changeTypes && cmake . && make')

                        # Run clang_ast_visitor
                        call_background('cd examples/' + folder + '/analysis_' + config_name + '/precimonious_setup && ' + scripts_path + '/changeTypes/clang_ast_visitor ../igen_setup/rmd_' + file_name + ' -- ' + ' >  ../igen_setup/chg_rmd_' + file_name)

                        # Call IGen
                        call_background('python3 ' + igen_src + '/bin/igen.py examples/' + folder + '/analysis_' + config_name + '/igen_setup/chg_rmd_' + file_name)

                        # Create suitable main file
                        call_background('cp examples/' + folder + '/analysis_' + config_name + '/precimonious_setup/funargs.txt .')
                        create_main.run('examples/' + folder, config_name, config)
                        call_background('rm -rf funargs.txt')

                        # Some renaming necessary (Will be removed)
                        call_background('cp examples/' + folder + '/analysis_' + config_name + '/igen_setup/cleaned_igen_chg_main.c examples/' + folder + '/analysis_' + config_name + '/igen_setup/cleaned_igen_main.c ')

                        # Make and run configuration
                        call_background('cd examples/' + folder + '/analysis_' + config_name + '/igen_setup && cmake . && make && ./some_app')
                        print()
                        print()
