#!/usr/bin/python
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '../scripts'))
from helper import call, Config, json, Config, nameWithoutExtension
from runConfig import run

fast = True # change here to make a quick test
path = 'examples/'

if fast:
    precisions =  [-10]
else:
    precisions = [2, 4, 6, 8, 10, 12, 14, 16]

if fast:
    max_prec_iters = [5]
else:
    max_prec_iters = [200]

if fast:
    vectorized = [False]
else:
    vectorized = [True, False]

error_types = ['highestAbsolute']

if fast:
    #folders = ['funarc', 'linear', 'newton_root', 'bisection_root', 'DFT16', 'DFT16dd', 'dot', 'matmul', 'simpsons']
    folders = ['DFT16', 'dot']
else:
    folders = ['funarc', 'linear', 'newton_root', 'bisection_root', 'DFT16', 'DFT16dd', 'dot', 'matmul', 'simpsons']
    #folders = ['dot']
if fast:
    tunings = ['precimonious']
else:
    tunings = ['precimonious', 'hifptuner']

if fast:
    input_precisions = ['dd']
else:
    input_precisions = ['dd', 'd']


if fast:
    input_ranges = [10]
else:
    input_ranges = [1, 10, 30]

# Start docker container
call('docker start hi')

for prec in precisions:
    for max_iter in max_prec_iters:
        for vec in vectorized:
            for err in error_types:
                for tuning in tunings:
                    for input_precision in input_precisions:
                        for input_range in input_ranges:
                            for folder_name in folders:

                                # Read standard config
                                std_config_name = 'std_config.json'
                                config = Config.read_config_from_file(path + folder_name + '/' + std_config_name)

                                # Apply changes accoring to current config
                                config.precision = prec
                                config.error_type = err
                                config.vectorized = vec
                                config.max_iterations = max_iter
                                config.tuning_algo = tuning
                                config.input_precision = input_precision
                                config.rng_range = input_range

                                # Get new config name
                                config_name = 'config_' + str(prec)
                                config_name += '#' + str(input_precision)
                                config_name += '#' + str(input_range)
                                if vec:
                                    config_name += '#vec'
                                config_name += '#' + tuning


                                # Save config as a file
                                config_str = config.get_config_as_string()
                                main_folder = 'examples/' + nameWithoutExtension(folder_name)
                                with open(main_folder + '/' + config_name + '.json', 'w') as myfile:
                                    myfile.write(config_str)

                                # Run config
                                print('Run:', folder_name, config_name)
                                run(main_folder, config_name, config)
