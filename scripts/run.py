#!/usr/bin/env python

import sys, os
import json
import re
import subprocess
from helper import call, call_background, getEnvVar, load_json, readConfig
import changeTypes, createChgMain

def main():
    if len(sys.argv) != 4:
        print("Incorrect number of arguments: " + str(len(sys.argv)))
        sys.exit(-1)

    path = sys.argv[1]
    config_file = sys.argv[2]
    search_counter = sys.argv[3]

    # Read information from config file
    config_path = os.path.join(path, config_file)
    file_name, function_name, args, ret, rep, prec, err_type, is_vect, max_iter, tuning = readConfig('../../' + config_file)

    # Change variable types in source file
    changeTypes.run(file_name)

    # Add casts to main file
    createChgMain.run(path, file_name, function_name, args, ret, rep, prec, err_type, search_counter)

    # Create folder of current run and move created files into it
    new_folder = '../' + str(search_counter)
    call('mkdir ' + new_folder)
    call('cp cleaned_igen_chg_main.c ' + new_folder + '/cleaned_igen_main.c')
    call('cp ../igen_setup/random_range_igen.c ' + new_folder)
    call('cp igen_chg_rmd_' + file_name + ' ' + new_folder)
    call('cp ../igen_setup/CMakeLists.txt ' + new_folder)

    #Add IGen dd lib and math lib, as IGen sometimes doesn't add it
    with open(new_folder + '/igen_chg_rmd_' + file_name, 'r') as myfile:
        code = myfile.read()
        code = '#include "igen_dd_lib.h"\n' + code
        code = '#include "igen_lib.h"\n' + code
        code = '#include "igen_math.h"\n' + code
        code = '#include "igen_dd_math.h"\n' + code

    with open(new_folder + '/igen_chg_rmd_' + file_name, 'w') as myfile:
        myfile.write(code)

    # Compile and execute
    call_background('cd ' + new_folder + ' && cmake . && make')
    print('Start exec')
    call(new_folder + '/some_app')
    print('Finish exec')
    print()

    # Copy results into folder
    call('cp sat.cov ' + new_folder)
    call('cp score.cov ' + new_folder)
    call('cp precision.cov ' + new_folder)
    call('cp config_temp.json ' + new_folder)



if __name__ == "__main__":
    main()
