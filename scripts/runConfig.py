#!/usr/bin/python
import sys, os
from helper import call, getEnvVar, nameWithoutExtension, readConfig, dockerCall30
import setupCode

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
    file_name, function_name, args, ret, rep, prec, err_type, is_vect, max_iter, tuning, input_prec, input_range = readConfig(config_path)
    file_name_wo = nameWithoutExtension(file_name)

    # Run setup
    setupCode.run(config_name, path, config_folder_path, file_name, function_name, args, ret, rep, prec, err_type, is_vect, tuning, input_prec, input_range)

    # Run precimonious/hifptuner
    if tuning == 'precimonious':
        tuner_folder_name = '/precimonious_setup'
    else:
        tuner_folder_name = '/hifptuner_setup'

    corvette_path = getEnvVar('CORVETTE_PATH') # precimonious path
    hifptuner_path = getEnvVar('HIFP_PATH') # HiFPTuner path
    tuner_path = config_folder_path + tuner_folder_name

    if tuning == 'precimonious':
        call('cd ' + tuner_path + ' && python2 -O ' + corvette_path
        + '/scripts/dd2.py ' + file_name_wo + '.bc search_' + file_name_wo
        + '.json config_' + file_name_wo + '.json ' + path + ' ' + config_file + ' ' + str(max_iter))
    else:
        call('cd ' + tuner_path + ' && python2 -O ' + hifptuner_path + '/precimonious/scripts/dd2_prof.py ' + file_name_wo + '.bc search_' + file_name_wo
        + '.json config_' + file_name_wo + '.json sorted_partition.json ' + path + ' ' + config_file + ' ' + str(max_iter))

    print('Run succeeded')
