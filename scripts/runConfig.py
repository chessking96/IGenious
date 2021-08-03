#!/usr/bin/python
import sys, os
from helper import call, call_background, getEnvVar, nameWithoutExtension, Config, dockerCall30, print_debug
import setupCode

def run(main_folder, config_name, config):

    # Start docker container (for HiFPTuner)
    print_debug('Starting docker container')
    call_background('docker start hi')

    # Delete old run (may or may not exist) and create new folder
    print_debug('Cleaning up directory')
    config_folder_path = main_folder + '/analysis_' + config_name
    call('rm -rf ' + config_folder_path)
    call('mkdir ' + config_folder_path)

    # Run setup
    print_debug('Run setup')
    setupCode.run(main_folder, config_name, config)

    # Run precimonious/hifptuner
    print_debug('Run')
    if config.tuning_algo == 'precimonious':
        tuner_folder_name = '/precimonious_setup'
    elif config.tuning_algo == 'hifptuner':
        tuner_folder_name = '/hifptuner_setup'
    else:
        print_err('This tuning algorithm is not supported: ' + config.tuning_algo)

    tuner_path = config_folder_path + tuner_folder_name
    file_name_wo = nameWithoutExtension(config.file_name)
    path = main_folder
    config_file = config_name + '.json'

    if config.tuning_algo == 'precimonious':
        corvette_path = getEnvVar('CORVETTE_PATH') # precimonious path
        call('cd ' + tuner_path + ' && python2 -O ' + corvette_path
        + '/scripts/dd2.py ' + file_name_wo + '.bc search_' + file_name_wo
        + '.json config_' + file_name_wo + '.json ' + path + ' ' + config_file + ' ' + str(config.max_iterations))
    else:
        hifptuner_path = getEnvVar('HIFP_PATH') # HiFPTuner path
        call('cd ' + tuner_path + ' && python2 -O ' + hifptuner_path + '/precimonious/scripts/dd2_prof.py ' + file_name_wo + '.bc search_' + file_name_wo
        + '.json config_' + file_name_wo + '.json sorted_partition.json ' + path + ' ' + config_file + ' ' + str(config.max_iterations))

    print('Run succeeded')
