#!/usr/bin/python
import sys, os, time
from helper import call, call_background, getEnvVar, nameWithoutExtension, Config, dockerCall30, print_debug
import setup_igenious

def run(main_folder, config_name, config):

    # Start time measurent to measure tuning time
    t_start = time.time()

    # Start docker container (for HiFPTuner)
    print_debug('Starting docker container')
    call_background('docker start hi')

    # Delete old run (may or may not exist) and create new folder
    print_debug('Cleaning up directory')
    config_folder_path = main_folder + '/analysis_' + config_name
    call('rm -rf ' + config_folder_path)
    call('mkdir ' + config_folder_path)

    # Run setup
    print_debug('Run setup_igenious')
    setup_igenious.run(main_folder, config_name, config)

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

    # Collect output
    path = config_folder_path
    run = 0
    best_run = -1
    best_time = 10000000000 # some big numbers
    best_acc = -1
    while(True):
        run_path = path + '/' + str(run)
        # Check if this run exists
        if not os.path.exists(run_path):
            break
        # Get time
        with open(run_path + '/score.cov', 'r') as myfile:
            run_time = int(myfile.read())
        # Get result
        with open(run_path + '/sat.cov', 'r') as myfile:
            sat = myfile.read()
        if sat == 'true\n':
            sat = True
        else:
            sat = False
        with open(run_path + '/precision.cov', 'r') as myfile:
            accuracy = (myfile.read()[0:-1])
        if sat and run_time < best_time:
            best_run = run
            best_time = run_time
            best_acc = accuracy
        run += 1
    with open(path + '/number_tunings.txt', 'w') as myfile:
        myfile.write(str(run))

    reps = config.repetitions
    best_time /= reps
    with open(path + '/result.txt', 'w') as myfile:
        myfile.write(str(best_run) + ',' + str(best_time) + ',' + str(best_acc))

    # Stop time measurement and write to file
    t_end = time.time()
    print('Run succeeded')
    print('Elapsed time:', str(t_end - t_start))
    with open(config_folder_path + '/runtime.txt', 'w') as myfile:
        myfile.write(str(t_end - t_start))
