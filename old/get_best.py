#!/usr/bin/python
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '../scripts'))
from helper import call, Config

folders = ['funarc', 'linear', 'newton_root', 'DFT16', 'dot', 'matmul', 'simpsons']
precisions = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
input_types = ['d', 'dd']
input_precisions = [10]
vectorized = [True, False]
tuning_algos = ['precimonious', 'hifptuner']

for folder in folders:
    for prec in precisions:
        for in_type in input_types:
            for in_prec  in input_precisions:
                for vec in vectorized:
                    for tuner in tuning_algos:
                        config_name = 'config_' + str(prec) + '#' + in_type + '#' + str(in_prec)
                        if vec:
                            config_name += '#vec'
                        config_name += '#' + tuner
                        config_folder = 'analysis_' + config_name
                        path = 'examples/' + folder + '/' + config_folder

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
                                time = int(myfile.read())
                            # Get result
                            with open(run_path + '/sat.cov', 'r') as myfile:
                                sat = myfile.read()
                            if sat == 'true\n':
                                sat = True
                            else:
                                sat = False
                            with open(run_path + '/precision.cov', 'r') as myfile:
                                accuracy = (myfile.read()[0:-1])

                            if sat and time < best_time:
                                best_run = run
                                best_time = time
                                best_acc = accuracy

                            run += 1


                        with open(path + '/number_tunings.txt', 'w') as myfile:
                            myfile.write(str(run))

                        reps = Config.read_config_from_file('examples/' + folder + '/' + config_name + '.json').repetitions
                        best_time /= reps
                        with open(path + '/result.txt', 'w') as myfile:
                            myfile.write(str(best_run) + ',' + str(best_time) + ',' + str(best_acc))
