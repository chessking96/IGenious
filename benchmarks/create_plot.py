#!/usr/bin/env python

import read_config as rc
import sys
from helper import nameWithoutExtension, Config
import matplotlib.pyplot as plt

def getFixedData(input_precision, rng_range, vectorized, folder_name):
    types_fix = ['dd', 'd', 'f']
    precs_fix = []
    times_fix = []

    config_name = 'non_mixed_' + str(input_precision) + '#' + str(rng_range) + '#'

    path = 'examples/' + folder_name
    for type in types_fix:
        run_path = 'examples/' + folder_name + '/analysis_' + config_name + type

        # Get number of repetions from configuration file
        config_file_path = 'examples/' + folder_name + '/' + config_name + type
        if vectorized == 'yes':
            config_file_path += '#vec'
        config_file_path += '.json'

        reps = Config.read_config_from_file(config_file_path).repetitions


        if vectorized == 'yes':
            run_path += '#vec'
        # Get time
        with open(run_path + '/igen_setup/score.cov', 'r') as myfile:
            time = int(myfile.read())
        # Get precision
        with open(run_path + '/igen_setup/precision.cov', 'r') as myfile:
            prec = float(myfile.read())

            times_fix.append(time / reps)
            precs_fix.append(prec)

    return precs_fix, times_fix

def getData(precision, input_type, input_range, vectorized, tuning, folder_name):
    # Build path
    config_base_name = 'config_' + str(precision) + '#' + str(input_type) + '#' + str(input_range) + '#'
    if vectorized == "yes":
        config_base_name += 'vec#'
    if tuning == 'precimonious':
        config_name = config_base_name + 'precimonious'
    else:
        config_name = config_base_name + 'hifptuner'
    name_wo_ext = config_name

    path = 'examples/' + folder_name + '/analysis_' + name_wo_ext

    # Get number of repetions from configuration file
    config_file_path = 'examples/' + folder_name + '/' + config_name
    if vectorized == 'yes':
        config_file_path += '#vec'
    config_file_path += '.json'

    reps = Config.read_config_from_file(config_file_path).repetitions

    # Get data
    return rc.read_results(path, reps)

def createAllSinglePlots():

    precisions = [6, 8, 10, 12, 14]
    input_types = ['dd']
    input_ranges = [1, 10]
    vectorized = ['no']
    tunings = ['precimonious']
    folder_names = ['linear', 'dot', 'DFT16dd', 'simpsons', 'funarc']

    for precision in precisions:
        for input_type in input_types:
            for input_range in input_ranges:
                for vec in vectorized:
                    for tuning in tunings:
                        for folder in folder_names:
                            times, precs, names = getData(precision, input_type, input_range, vec, tuning, folder)
                            precs_fix, times_fix = getFixedData(input_type, input_range, vec, folder)

                            colors = len(precs) * ['blue']
                            plt.scatter(precs, times, c = colors, s = 60, label = tuning)
                            colors = len(precs_fix) * ['red']
                            plt.scatter(precs_fix, times_fix, c = colors, label = 'No mixed tuning')
                            #for i, txt in enumerate(names_sat_prec):
                            #    plt.annotate(txt, (precs_sat_prec[i], times_sat_prec[i]))


                            # Plot fixed points
                            #colors = len(precs_fix) * ['red']
                            #plt.scatter(precs_fix, times_fix, c = colors, label = 'No mixed tuning')
                            #for i, txt in enumerate(types_fix):
                            #    plt.annotate(txt, (precs_fix[i], times_fix[i]))
                            plt.xscale('log')

                            plt.legend()
                            plot_title = folder + ', precision = 10-' + str(precision) + ', inputPrecision: ' + input_type + ', inputRange: ' + str(input_range) + ', ' + tuning
                            if vec == 'yes':
                                plot_title += ', vectorized'
                            plt.title(plot_title)

                            plt.show()

if __name__ == "__main__":
    createAllSinglePlots()
