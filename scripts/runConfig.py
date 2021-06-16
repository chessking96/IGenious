#!/usr/bin/python
import sys, os
from helper import call, getEnvVar, nameWithoutExtension, readConfig
import setupNew as setup

if __name__ == "__main__":
    # Arguments: folder_path, config_name
    if len(sys.argv) != 3:
        print("Wrong number of arguments:", len(sys.argv))
        sys.exit(-1)

    path = sys.argv[1]
    config_file = sys.argv[2]

    # Delete old run (may or may not exist) and create new folder
    config_name = nameWithoutExtension(config_file)
    config_folder_path = path + '/analysis_' + config_name
    call('rm -rf ' + config_folder_path)
    call('mkdir ' + config_folder_path)

    # Read information from config file
    config_path = os.path.join(path, config_file)
    file_name, function_name, args, ret, rep, prec, err_type, is_vect, max_iter = readConfig(config_path)
    file_name_wo = nameWithoutExtension(file_name)

    # Run setup
    setup.run(path, config_folder_path, file_name, function_name, args, ret, rep, prec, err_type, is_vect)

    # Run precimonious
    corvette_path = getEnvVar('CORVETTE_PATH') # precimonious path
    prec_path = config_folder_path + '/precimonious_setup'
    ret = call('cd ' + prec_path + ' && python2 -O ' + corvette_path
    + '/scripts/dd2.py ' + file_name_wo + '.bc search_' + file_name_wo
    + '.json config_' + file_name_wo + '.json ' + path + ' ' + config_file + ' ' + str(max_iter))

    print('Run succeeded')
