#!/usr/bin/python

import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '../scripts'))
from helper import call, Config

def run():
    fast = False

    if fast:
        folders = ['arclength', 'linear', 'newton_root', 'DFT16', 'dot', 'matmul', 'simpsons']
        precisions = [10]
        input_types = ['dd']
        input_precisions = [10]
        vectorized = [True]
        tuning_algos = ['precimonious', 'hifptuner']
    else:
        folders = ['arclength', 'linear', 'newton_root', 'DFT16', 'dot', 'matmul', 'simpsons']
        precisions = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        input_types = ['d', 'dd']
        input_precisions = [10]
        vectorized = [True, False]
        tuning_algos = ['precimonious', 'hifptuner']

    precimonious_time = dict()
    hifptuner_time = dict()
    precimonious_number = dict()
    hifptuner_number = dict()
    counter = 0

    print_string = ''

    for folder in folders:
        precimonious_time[folder] = 0
        hifptuner_time[folder] = 0
        precimonious_number[folder] = 0
        hifptuner_number[folder] = 0
        counter = 0
        for prec in precisions:
            for in_type in input_types:
                for in_prec  in input_precisions:
                    for vec in vectorized:
                        counter += 1
                        tuner = 'precimonious'
                        config_name = 'config_' + str(prec) + '#' + in_type + '#' + str(in_prec)
                        if vec:
                            config_name += '#vec'
                        config_name += '#' + tuner
                        config_folder = 'analysis_' + config_name
                        path = 'examples/' + folder + '/' + config_folder
                        file = path + '/runtime.txt'
                        with open(file, 'r') as myfile:
                            time = float(myfile.read())

                        with open(path + '/number_tunings.txt', 'r') as myfile:
                            number = int(myfile.read())

                        #print(time, number, folder, tuner)
                        precimonious_time[folder] += time
                        precimonious_number[folder] += number

                        tuner = 'hifptuner'
                        config_name = 'config_' + str(prec) + '#' + in_type + '#' + str(in_prec)
                        if vec:
                            config_name += '#vec'
                        config_name += '#' + tuner
                        config_folder = 'analysis_' + config_name
                        path = 'examples/' + folder + '/' + config_folder
                        file = path + '/runtime.txt'
                        with open(file, 'r') as myfile:
                            time = float(myfile.read())

                        with open(path + '/number_tunings.txt', 'r') as myfile:
                            number = int(myfile.read())

                        #print(time, number, folder, tuner)
                        hifptuner_time[folder] += time
                        hifptuner_number[folder] += number

        precimonious_time[folder] /= counter
        hifptuner_time[folder] /= counter
        precimonious_number[folder] /= counter
        hifptuner_number[folder] /= counter

        print_string += 'pr' + ' ' + folder + ' ' + str(precimonious_time[folder]) + ' ' + str(precimonious_number[folder]) + '\n'
        print_string += 'hi' + ' ' + folder + ' ' + str(hifptuner_time[folder]) + ' ' + str(hifptuner_number[folder]) + '\n'

    print(print_string)
    with open('plots/runtimes.txt', 'w') as myfile:
        myfile.write(print_string)

run()
