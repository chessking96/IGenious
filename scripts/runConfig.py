#!/usr/bin/python
import sys, os
from helper import call, getEnvVar, nameWithoutExtension, Config, dockerCall30
import setupCode

def run(main_folder, config_name, config):

    # Delete old run (may or may not exist) and create new folder
    config_folder_path = main_folder + '/analysis_' + config_name
    call('rm -rf ' + config_folder_path)
    call('mkdir ' + config_folder_path)

    # Run setup
    setupCode.run(main_folder, config_name, config)

    print('Until here')
    sys.exit(-1)

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
