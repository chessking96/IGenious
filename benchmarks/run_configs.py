#!/usr/bin/python
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '../scripts'))
from helper import call, readConfig, json

fast = True # change here to make a quick test
path = 'examples/'

if fast:
    precisions =  [4]
else:
    precisions = [4, 6, 8, 10, 12, 14, 16, 18]

if fast:
    max_prec_iters = [5]
else:
    max_prec_iters = [200]

if fast:
    vectorized = [False]
else:
    vectorized = [False]

error_types = ['highestAbsolute']

if fast:
    folders = ['bisection_root', 'DFT16', 'DFT16dd', 'dot', 'matmul', 'simpsons']
else:
    folders = ['bisection_root', 'DFT16', 'DFT16dd', 'dot', 'matmul', 'simpsons']

tunings = ['precimonious', 'hifptuner']

for prec in precisions:
    for max_iter in max_prec_iters:
        for vec in vectorized:
            for err in error_types:
                for tuning in tunings:
                    for i in range(len(folders)):
                        folder_name = folders[i]
                        std_config_name = 'std_config.json'
                        file_name, function_name, args, ret, rep, _precision, _err_type, _use_vectorized, _maxpreciterations, _tuning = readConfig(path + folder_name + '/' + std_config_name)
                        args_prepared = '['
                        for i in range(len(args) - 1):
                            arg = args[i]
                            args_prepared += '"' + str(arg[0]) + '", ' + str(arg[1]) + ', "' + str(arg[2]) + '", "' + str(arg[3]) + '", '
                        if len(args) >= 1:
                            arg = args[-1]
                            args_prepared += '"' + str(arg[0]) + '", ' + str(arg[1]) + ', "' + str(arg[2]) + '", "' + str(arg[3]) + '"'
                        args_prepared  += ']'


                        new_config = '{\n'
                        new_config += '\t"filename": "' + file_name + '",\n'
                        new_config += '\t"functionname": "' + function_name + '",\n'
                        new_config += '\t"args": ' + args_prepared + ',\n'
                        new_config += '\t"return": ' + json.dumps(ret) + ',\n'
                        new_config += '\t"repetitions": ' + str(rep) + ',\n'
                        new_config += '\t"precision": ' + str(prec) + ',\n'
                        new_config += '\t"errortype": "' + err + '",\n'
                        new_config += '\t"vectorized": "' + str(vec) + '",\n'
                        new_config += '\t"maxpreciterations": ' + str(max_iter) + ',\n'
                        new_config += '\t"tuning": "' + tuning + '"\n'
                        new_config += '}'

                        config_name = 'config_' + str(prec)
                        if vec:
                            config_name += '#vec'

                        config_name += '#' + tuning

                        config_name += '.json'


                        with open(path + folder_name + '/' + config_name, 'w') as myfile:
                            myfile.write(new_config)

                        print('Run:', folder_name, config_name)
                        call('python scripts/runConfig.py examples/' + folder_name + ' ' + config_name)
