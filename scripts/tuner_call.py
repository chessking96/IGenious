#!/usr/bin/env python

# This file gets called by Precimonious/HIFPTuner when a new configuration is proposed

import sys, os
import json
import re
import subprocess
from helper import call, call_background, getEnvVar, load_json, Config, nameWithoutExtension, print_debug
import change_types, create_main

def main():
    if len(sys.argv) != 4:
        print("Incorrect number of arguments: " + str(len(sys.argv)))
        sys.exit(-1)

    path = sys.argv[1]
    config_file = sys.argv[2]
    search_counter = sys.argv[3]

    print('Explore configuration #' + search_counter)

    # Read information from config file
    config_path = os.path.join(path, config_file)
    config = Config.read_config_from_file('../../' + config_file)

    # Change variable types in source file
    change_types.run(config.file_name)

    # Create suitable main file
    create_main.run('../..', nameWithoutExtension(config_file), config)

    # Create folder of current run and move created files into it
    new_folder = '../' + str(search_counter)
    call('mkdir ' + new_folder)
    call('cp ../igen_setup/cleaned_igen_chg_main.c ' + new_folder + '/cleaned_igen_main.c')
    call('cp ../igen_setup/random_range_igen.c ' + new_folder)
    call('cp ../igen_setup/igen_chg_rmd_' + config.file_name + ' ' + new_folder)
    call('cp ../igen_setup/CMakeLists.txt ' + new_folder)

    #Add IGen dd lib and math lib, as IGen sometimes doesn't add it
    with open(new_folder + '/igen_chg_rmd_' + config.file_name, 'r') as myfile:
        code = myfile.read()
        code = '#include "igen_dd_lib.h"\n' + code
        code = '#include "igen_lib.h"\n' + code
        code = '#include "igen_math.h"\n' + code
        code = '#include "igen_dd_math.h"\n' + code

    with open(new_folder + '/igen_chg_rmd_' + config.file_name, 'w') as myfile:
        myfile.write(code)

    # Compile and execute
    call_background('cd ' + new_folder + ' && cmake . && make')
    print_debug('Start exec')
    call(new_folder + '/some_app')
    print_debug('Finish exec')
    print()

    # Copy results into folder
    call('cp sat.cov ' + new_folder)
    call('cp score.cov ' + new_folder)
    call('cp precision.cov ' + new_folder)
    call('cp config_temp.json ' + new_folder)

    # Delte some files, to save storage
    run_path = new_folder
    call('cd ' + run_path + ' && rm -rf CMakeFiles')
    call('cd ' + run_path + ' && rm -rf CMakeCache.txt')
    call('cd ' + run_path + ' && rm -rf cmake_install.cmake')
    call('cd ' + run_path + ' && rm -rf Makefile')
    call('cd ' + run_path + ' && rm -rf some_app')

if __name__ == "__main__":
    main()
