#!/usr/bin/python

# This file rans the mixed-precision tuning benchmarks

import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '../scripts'))
from helper import call, Config, json, Config, nameWithoutExtension
import run_igenious

def run():

    precisions = [6, 8, 10, 12, 11, 13, 14, 15, 16, 2, 3, 4, 5, 7, 9]
    max_prec_iters = [500]
    vectorized = [True, False]
    error_types = ['highest_relative']
    folders = ['arclength', 'linear', 'newton_root', 'DFT16', 'dot', 'matmul', 'simpsons']
    tunings = ['hifptuner', 'precimonious']
    input_precisions = ['dd', 'd']
    input_ranges = [10]
    rep_input = 100

    path = 'examples/'

    for prec in precisions:
        for max_iter in max_prec_iters:
            for vec in vectorized:
                for err in error_types:
                    for tuning in tunings:
                        for input_precision in input_precisions:
                            for input_range in input_ranges:
                                for folder_name in folders:

                                    # Read standard config
                                    std_config_name = 'settings.json'
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
                                    run_igenious.run(main_folder, config_name, config)

run()
