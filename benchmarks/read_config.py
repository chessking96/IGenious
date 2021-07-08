#!/usr/bin/env python
import sys, os
import matplotlib.pyplot as plt
sys.path.insert(1, os.path.join(sys.path[0], '../scripts'))
from helper import load_json, nameWithoutExtension

def read_results(path):
    # Variables for results
    times = []
    sats = []
    precs = []
    names = [] # Create some name for each config depending on number of dd/d/f

    # Iterate over runs
    run = 0

    # Read results
    while(True):
        run_path = path + '/' + str(run)
        # Check if this run exists
        if not os.path.exists(run_path):
            break

        # Get time
        with open(run_path + '/score.cov', 'r') as myfile:
            time = int(myfile.read())
        # Get result
        with open(run_path + '/sat.cov', 'r') as myfile:
            sat = myfile.read()
        if sat == 'true\n':
            sat = True
        else:
            sat = False
        # Get precision
        with open(run_path + '/precision.cov', 'r') as myfile:
            prec = float(myfile.read())
        # Read config
        with open(run_path + '/config_temp.json', 'r') as myfile:
            config = load_json(myfile.read())

        # Counters for different types
        c_f = 0
        c_d = 0
        c_dd = 0

        for i in range(len(config)):
            ty = config[i][1]
            if ty in f_type:
                c_f += 1
            elif ty in d_type:
                c_d += 1
            elif ty in dd_type:
                c_dd += 1
            else:
                print('Error', ty)
        name = str(run) + ' dd:' + str(c_dd) + ' d:' + str(c_d) + ' f:' + str(c_f)


        times.append(time)
        sats.append(sat)
        precs.append(prec)
        names.append(name)

        run += 1

    # Filter out non successful runs
    times_sat = []
    precs_sat = []
    names_sat = []

    for i in range(len(sats)):
        if sats[i]:
            times_sat.append(times[i])
            precs_sat.append(precs[i])
            names_sat.append(names[i])

    return times_sat, precs_sat, names_sat

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Incorrect number of arguments: " + str(len(sys.argv)))
        sys.exit(-1)
    folder_name = sys.argv[1]
    precision = sys.argv[2]
    input_type = sys.argv[3]
    input_range = sys.argv[4]
    vectorized = sys.argv[5]
    tuning = sys.argv[6]

    # Helpers to read config_file
    f_type = ['float', 'float*']
    d_type = ['double', 'double*']
    dd_type = ['longdouble', 'longdouble*']


    config_base_name = 'config_' + str(precision) + '#' + str(input_type) + '#' + str(input_range) + '#'
    if vectorized == "yes":
        config_base_name += 'vec#'


    # Precimonious
    # Build path
    if tuning == 'precimonious':
        config_name = config_base_name + 'precimonious.json'
    else:
        config_name = config_base_name + 'hifptuner.json'

    name_wo_ext = nameWithoutExtension(config_name)
    path = 'examples/' + folder_name + '/analysis_' + name_wo_ext

    # Check if path exists
    if not os.path.exists(path):
        print(path)
        print('This folder/configuration pair does not exist.')
        sys.exit(-1)

    times_sat_prec, precs_sat_prec, names_sat_prec = read_results(path)


    # Read nonmixed results
    types_fix = ['dd', 'd', 'f']
    precs_fix = []
    times_fix = []

    path = 'examples/' + folder_name + '/no_mixed/'
    for type in types_fix:
        run_path = 'examples/' + folder_name + '/no_mixed/' + input_type + '#' + str(input_range) + '#' + type
        # Get time
        with open(run_path + '/build/score.cov', 'r') as myfile:
            time = int(myfile.read())
        # Get precision
        with open(run_path + '/build/precision.cov', 'r') as myfile:
            prec = float(myfile.read())

            times_fix.append(time)
            precs_fix.append(prec)

    # Plot points from tuning Precimonious
    colors = len(precs_sat_prec) * ['blue']
    plt.scatter(precs_sat_prec, times_sat_prec, c = colors, label = 'Precimonious')
    for i, txt in enumerate(names_sat_prec):
        plt.annotate(txt, (precs_sat_prec[i], times_sat_prec[i]))


    # Plot fixed points
    colors = len(precs_fix) * ['green']
    plt.scatter(precs_fix, times_fix, c = colors, label = 'No tuning')
    for i, txt in enumerate(types_fix):
        plt.annotate(txt, (precs_fix[i], times_fix[i]))
    plt.xscale('log')

    plt.legend()
    plt.title(folder_name + ', precision = 10' + precision)

    plt.show()
