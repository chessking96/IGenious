#!/usr/bin/env python

# This file creates the plots for the thesis

import sys, os, math
sys.path.insert(1, os.path.join(sys.path[0], '../scripts'))
from helper import nameWithoutExtension, Config

import matplotlib.pyplot as plt
import matplotlib.ticker
from matplotlib.ticker import MaxNLocator

# Function to import data from fixed-precision run
def getFixedData(input_precision, rng_range, vectorized, folder_name):
    types_fix = ['dd', 'd', 'f']
    acc_fix = []
    times_fix = []

    config_name = 'non_mixed_' + str(input_precision) + '#' + str(rng_range) + '#'
    path = 'examples/' + folder_name
    for type in types_fix:
        run_path = 'examples/' + folder_name + '/analysis_' + config_name + type
        if vectorized:
            run_path += '#vec'

        # Get number of repetions from configuration file
        config_file_path = 'examples/' + folder_name + '/' + config_name + type
        if vectorized:
            config_file_path += '#vec'
        config_file_path += '.json'
        reps = Config.read_config_from_file_old(config_file_path).repetitions

        # Get time
        with open(run_path + '/igen_setup/score.cov', 'r') as myfile:
            time = int(myfile.read())
        # Get precision
        with open(run_path + '/igen_setup/precision.cov', 'r') as myfile:
            prec = float(myfile.read())

        # Fix temporary issue
        fn = folder_name
        if fn == 'simpsons' or fn == 'arclength' or fn == 'newton_root':
            time /= 10

        times_fix.append(time / reps)
        acc_fix.append(prec)

    return acc_fix, times_fix


# Create plots where just a single setting is shown
def create_single():
    precisions = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    input_types = ['d', 'dd']
    input_ranges = [10]
    vectorized = [True, False]
    folder_names = [['simpsons', 'matmul'], ['dot', 'DFT16'], ['arclength', 'linear'], ['newton_root']]

    #for input_type in input_types:
    for input_range in input_ranges:
        for vec in vectorized:
            for in_type in input_types:

                # Prepare figure and subplots
                fig, ax = plt.subplots(4,2, figsize=(10,10))
                fig.tight_layout()
                fig.delaxes(ax[3, 1])
                plt.subplots_adjust(hspace=0.7, wspace=0.3, top=0.95, left=0.08, bottom=0.05)

                for folder_i in range(len(folder_names)):
                    folder_one = folder_names[folder_i]
                    for folder_j in range(len(folder_one)):
                        folder = folder_one[folder_j]

                        # Read mixed-precision data
                        times_p = []
                        precs_p = []
                        for prec in precisions:
                            config_name = 'config_' + str(prec) + '#' + in_type + '#' + str(input_range)
                            if vec:
                                config_name += '#vec'
                            config_name += '#' + 'precimonious'
                            config_folder = 'analysis_' + config_name
                            path = 'examples/' + folder + '/' + config_folder
                            with open(path + '/result.txt') as myfile:
                                result = myfile.read().split(',')
                            if int(result[0]) != -1:
                                times_p.append(float(result[1]))
                                precs_p.append(float(result[2]))
                        times_h = []
                        precs_h = []
                        for prec in precisions:
                            config_name = 'config_' + str(prec) + '#' + in_type + '#' + str(input_range)
                            if vec:
                                config_name += '#vec'
                            config_name += '#' + 'hifptuner'
                            config_folder = 'analysis_' + config_name
                            path = 'examples/' + folder + '/' + config_folder
                            with open(path + '/result.txt') as myfile:
                                result = myfile.read().split(',')
                            if int(result[0]) != -1:
                                times_h.append(float(result[1]))
                                precs_h.append(float(result[2]))

                        # Read fixed-precision data
                        precs_fix_p, times_fix_p = getFixedData(in_type, input_range, vec, folder)

                        # Calculate speedup and accuracy in bits
                        time_ref = times_fix_p[0]
                        for i in range(len(precs_p)):
                            precs_p[i] = -math.log10(precs_p[i]) * math.log2(10)
                            times_p[i] = time_ref / times_p[i]

                        for i in range(len(precs_h)):
                            precs_h[i] = -math.log10(precs_h[i]) * math.log2(10)
                            times_h[i] = time_ref / times_h[i]

                        for i in range(len(precs_fix_p)):
                            precs_fix_p[i] = -math.log10(precs_fix_p[i]) * math.log2(10)
                            times_fix_p[i] = time_ref / times_fix_p[i]

                        # Prepare subfigure
                        ax[folder_i, folder_j].xaxis.set_major_locator(MaxNLocator(integer=True))
                        ax[folder_i, folder_j].yaxis.set_major_locator(MaxNLocator(integer=True))
                        ax[folder_i, folder_j].set_title(folder, size=18)
                        ax[folder_i, folder_j].set_ylabel('speedup', fontsize=14)
                        ax[folder_i, folder_j].set_xlabel('#correct bits', fontsize=14)

                        # Plot data
                        colors = len(precs_p) * ['blue']
                        l1 = ax[folder_i, folder_j].scatter(precs_p, times_p, c = colors, s = 100)
                        colors = len(precs_fix_p) * ['red']
                        l3 = ax[folder_i, folder_j].scatter(precs_fix_p, times_fix_p, c = colors, s= 40)

                        # Adjust fontsize
                        ax[folder_i, folder_j].tick_params(axis='both', which='major', labelsize=14)

                # Plot legend and save figure
                plt.legend([l1, l3], [r'Mixed-precision - IGenious', 'Fixed-precision'], bbox_to_anchor=(2.28, 0.8), fontsize=16)
                plt.savefig('plots/singles/single_' + in_type + str(vec) + str(input_range) + '.png')
                plt.close('all')

# Create plots for Presimonious vs. HiFPTuner
def create_tuner():
    precisions = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    input_types = ['d', 'dd']
    input_ranges = [10]
    vectorized = [True, False]
    folder_names = [['simpsons', 'matmul'], ['dot', 'DFT16'], ['arclength', 'linear'], ['newton_root']]

    for input_range in input_ranges:
        for vec in vectorized:
            for in_type in input_types:

                # Prepare subplots
                fig, ax = plt.subplots(4,2, figsize=(10,10))
                fig.tight_layout()
                fig.delaxes(ax[3, 1])
                plt.subplots_adjust(hspace=0.7, wspace=0.3, top=0.95, left=0.08, bottom=0.05)

                for folder_i in range(len(folder_names)):
                    folder_one = folder_names[folder_i]
                    for folder_j in range(len(folder_one)):
                        folder = folder_one[folder_j]

                        # Read mixed-precision results
                        times_p = []
                        precs_p = []
                        for prec in precisions:
                            config_name = 'config_' + str(prec) + '#' + in_type + '#' + str(input_range)
                            if vec:
                                config_name += '#vec'
                            config_name += '#' + 'precimonious'
                            config_folder = 'analysis_' + config_name
                            path = 'examples/' + folder + '/' + config_folder
                            with open(path + '/result.txt') as myfile:
                                result = myfile.read().split(',')
                            if int(result[0]) != -1:
                                times_p.append(float(result[1]))
                                precs_p.append(float(result[2]))
                        times_h = []
                        precs_h = []
                        for prec in precisions:
                            config_name = 'config_' + str(prec) + '#' + in_type + '#' + str(input_range)
                            if vec:
                                config_name += '#vec'
                            config_name += '#' + 'hifptuner'
                            config_folder = 'analysis_' + config_name
                            path = 'examples/' + folder + '/' + config_folder
                            with open(path + '/result.txt') as myfile:
                                result = myfile.read().split(',')
                            if int(result[0]) != -1:
                                times_h.append(float(result[1]))
                                precs_h.append(float(result[2]))


                        # Read fixed-precision results
                        precs_fix_p, times_fix_p = getFixedData(in_type, input_range, vec, folder)

                        # Calculate speedup and accuracy in bits
                        time_ref = times_fix_p[0]
                        for i in range(len(precs_p)):
                            precs_p[i] = -math.log10(precs_p[i]) * math.log2(10)
                            times_p[i] = time_ref / times_p[i]

                        for i in range(len(precs_h)):
                            precs_h[i] = -math.log10(precs_h[i]) * math.log2(10)
                            times_h[i] = time_ref / times_h[i]

                        for i in range(len(precs_fix_p)):
                            precs_fix_p[i] = -math.log10(precs_fix_p[i]) * math.log2(10)
                            times_fix_p[i] = time_ref / times_fix_p[i]

                        # Prepare subplot
                        ax[folder_i, folder_j].xaxis.set_major_locator(MaxNLocator(integer=True))
                        ax[folder_i, folder_j].yaxis.set_major_locator(MaxNLocator(integer=True))
                        ax[folder_i, folder_j].set_title(folder, size=18)
                        ax[folder_i, folder_j].set_ylabel('speedup', fontsize=14)
                        ax[folder_i, folder_j].set_xlabel('#correct bits', fontsize=14)


                        # Plot data
                        colors = len(precs_p) * ['blue']
                        l1 = ax[folder_i, folder_j].scatter(precs_p, times_p, c = colors, s = 110)
                        colors = len(precs_h) * ['green']
                        l2 = ax[folder_i, folder_j].scatter(precs_h, times_h, c = colors, s = 60)
                        colors = len(precs_fix_p) * ['red']
                        l3 = ax[folder_i, folder_j].scatter(precs_fix_p, times_fix_p, c = colors, s= 40)

                        # Adjust fontsize
                        ax[folder_i, folder_j].tick_params(axis='both', which='major', labelsize=14)

                # Save figure
                plt.legend([l1, l2, l3], ['Mixed-precision with Precimonious', 'Mixed-precision with HiFPTuner', 'Fixed-precision'], bbox_to_anchor=(2.325, 0.9), fontsize=16)
                plt.savefig('plots/pVSh/tuner_' + in_type + str(vec) + str(input_range) + '.png')
                plt.close('all')

# Create plots for dd input vs d input
def create_input():
    precisions = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    tunings = ['precimonious', 'hifptuner']
    input_ranges = [10]
    vectorized = [True, False]
    folder_names = [['linear', 'matmul'], ['dot', 'DFT16']]

    for input_range in input_ranges:
        for vec in vectorized:
            for tuner in tunings:

                # Prepare subfigures
                fig, ax = plt.subplots(2,2, figsize=(10,7.5))
                fig.tight_layout()
                plt.subplots_adjust(hspace=0.7, wspace=0.3, top=0.94, left=0.08, bottom=0.3)

                for folder_i in range(len(folder_names)):
                    folder_one = folder_names[folder_i]
                    for folder_j in range(len(folder_one)):
                        folder = folder_one[folder_j]

                        # Read mixed-precision results
                        times_d = []
                        precs_d = []
                        for prec in precisions:
                            config_name = 'config_' + str(prec) + '#' + 'd' + '#' + str(input_range)
                            if vec:
                                config_name += '#vec'
                            config_name += '#' + tuner
                            config_folder = 'analysis_' + config_name
                            path = 'examples/' + folder + '/' + config_folder
                            with open(path + '/result.txt') as myfile:
                                result = myfile.read().split(',')
                            if int(result[0]) != -1:
                                times_d.append(float(result[1]))
                                precs_d.append(float(result[2]))
                        times_dd = []
                        precs_dd = []
                        for prec in precisions:
                            config_name = 'config_' + str(prec) + '#' + 'dd' + '#' + str(input_range)
                            if vec:
                                config_name += '#vec'
                            config_name += '#' + tuner
                            config_folder = 'analysis_' + config_name
                            path = 'examples/' + folder + '/' + config_folder
                            with open(path + '/result.txt') as myfile:
                                result = myfile.read().split(',')
                            if int(result[0]) != -1:
                                times_dd.append(float(result[1]))
                                precs_dd.append(float(result[2]))

                        # Read fixed-precision results
                        precs_fix_dd, times_fix_dd = getFixedData('dd', input_range, vec, folder)
                        precs_fix_d, times_fix_d = getFixedData('d', input_range, vec, folder)

                        # Calculate speedup and accuracy in bits
                        time_ref = times_fix_dd[0]
                        for i in range(len(precs_d)):
                            precs_d[i] = -math.log10(precs_d[i]) * math.log2(10)
                            times_d[i] = time_ref / times_d[i]

                        for i in range(len(precs_dd)):
                            precs_dd[i] = -math.log10(precs_dd[i]) * math.log2(10)
                            times_dd[i] = time_ref / times_dd[i]

                        for i in range(len(precs_fix_d)):
                            precs_fix_d[i] = -math.log10(precs_fix_d[i]) * math.log2(10)
                            times_fix_d[i] = time_ref / times_fix_d[i]

                        for i in range(len(precs_fix_dd)):
                            precs_fix_dd[i] = -math.log10(precs_fix_dd[i]) * math.log2(10)
                            times_fix_dd[i] = time_ref / times_fix_dd[i]

                        # Prepare subfigure
                        ax[folder_i, folder_j].xaxis.set_major_locator(MaxNLocator(integer=True))
                        ax[folder_i, folder_j].yaxis.set_major_locator(MaxNLocator(integer=True))
                        ax[folder_i, folder_j].set_title(folder, size=18)
                        ax[folder_i, folder_j].set_ylabel('speedup', fontsize=14)
                        ax[folder_i, folder_j].set_xlabel('#correct bits', fontsize=14)

                        # Plot data
                        colors = len(precs_d) * ['blue']
                        l1 = ax[folder_i, folder_j].scatter(precs_d, times_d, c = colors, s = 140)
                        colors = len(precs_dd) * ['green']
                        l2 = ax[folder_i, folder_j].scatter(precs_dd, times_dd, c = colors, s = 80)
                        colors = len(precs_fix_d) * ['red']
                        l3 = ax[folder_i, folder_j].scatter(precs_fix_d, times_fix_d, c = colors, s= 60)
                        colors = len(precs_fix_dd) * ['orange']
                        l4 = ax[folder_i, folder_j].scatter(precs_fix_dd, times_fix_dd, c = colors, s = 40)

                        # Adjust fontsize
                        ax[folder_i, folder_j].tick_params(axis='both', which='major', labelsize=14)

                # Save figure
                plt.legend([l1, l2, l3, l4], ['Mixed-precision with double input', 'Mixed-precision with double-double input', 'Fixed-precision with double input', 'Fixed-precision with double-double input'], bbox_to_anchor=(0.55, -0.4), fontsize=16)
                plt.savefig('plots/ddVSd/input_' + str(vec) + tuner + str(input_range) + '.png')
                plt.close('all')

# Create plots for vectorized vs non-vectorized
def create_vec():
    precisions = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    input_types = ['dd', 'd']
    tunings = ['precimonious', 'hifptuner']
    input_ranges = [10]
    folder_names = [['simpsons', 'matmul'], ['dot', 'DFT16'], ['arclength', 'linear'], ['newton_root']]

    for input_type in input_types:
        for input_range in input_ranges:
            for tuner in tunings:

                # Prepare subfigures
                fig, ax = plt.subplots(4,2, figsize=(10,10))
                fig.tight_layout()
                fig.delaxes(ax[3, 1])
                plt.subplots_adjust(hspace=0.7, wspace=0.3, top=0.95, left=0.08, bottom=0.05)


                for folder_i in range(len(folder_names)):
                    folder_one = folder_names[folder_i]

                    for folder_j in range(len(folder_one)):
                        folder = folder_one[folder_j]

                        # Read mixed-precision tuning results
                        times_v = []
                        precs_v = []
                        for prec in precisions:
                            config_name = 'config_' + str(prec) + '#' + input_type + '#' + str(input_range)
                            config_name += '#vec'
                            config_name += '#' + tuner
                            config_folder = 'analysis_' + config_name
                            path = 'examples/' + folder + '/' + config_folder
                            with open(path + '/result.txt') as myfile:
                                result = myfile.read().split(',')
                            if int(result[0]) != -1:
                                times_v.append(float(result[1]))
                                precs_v.append(float(result[2]))
                        times_n = []
                        precs_n = []
                        for prec in precisions:
                            config_name = 'config_' + str(prec) + '#' + input_type + '#' + str(input_range)
                            config_name += '#' + tuner
                            config_folder = 'analysis_' + config_name
                            path = 'examples/' + folder + '/' + config_folder
                            with open(path + '/result.txt') as myfile:
                                result = myfile.read().split(',')
                            if int(result[0]) != -1:
                                times_n.append(float(result[1]))
                                precs_n.append(float(result[2]))

                        # Read fixed-precision data
                        precs_fix_v, times_fix_v = getFixedData(input_type, input_range, True, folder)
                        precs_fix_n, times_fix_n = getFixedData(input_type, input_range, False, folder)

                        # Calculate speedup and accuracy in bits
                        time_ref = times_fix_n[0]
                        for i in range(len(precs_v)):
                            precs_v[i] = -math.log10(precs_v[i]) * math.log2(10)
                            times_v[i] = time_ref / times_v[i]

                        for i in range(len(precs_n)):
                            precs_n[i] = -math.log10(precs_n[i]) * math.log2(10)
                            times_n[i] = time_ref / times_n[i]

                        for i in range(len(precs_fix_v)):
                            precs_fix_v[i] = -math.log10(precs_fix_v[i]) * math.log2(10)
                            times_fix_v[i] = time_ref / times_fix_v[i]

                        for i in range(len(precs_fix_n)):
                            precs_fix_n[i] = -math.log10(precs_fix_n[i]) * math.log2(10)
                            times_fix_n[i] = time_ref / times_fix_n[i]

                        # Prepare subfigure
                        ax[folder_i, folder_j].xaxis.set_major_locator(MaxNLocator(integer=True))
                        ax[folder_i, folder_j].yaxis.set_major_locator(MaxNLocator(integer=True))
                        ax[folder_i, folder_j].set_title(folder, size=18)
                        ax[folder_i, folder_j].set_ylabel('speedup', fontsize=14)
                        ax[folder_i, folder_j].set_xlabel('#correct bits', fontsize=14)

                        # Plot data
                        colors = len(precs_v) * ['blue']
                        l1 = ax[folder_i, folder_j].scatter(precs_v, times_v, c = colors, s = 100)
                        colors = len(precs_n) * ['green']
                        l2 = ax[folder_i, folder_j].scatter(precs_n, times_n, c = colors, s = 60)
                        colors = len(precs_fix_v) * ['red']
                        l3 = ax[folder_i, folder_j].scatter(precs_fix_v, times_fix_v, c = colors, s= 45)
                        colors = len(precs_fix_n) * ['orange']
                        l4 = ax[folder_i, folder_j].scatter(precs_fix_n, times_fix_n, c = colors, s = 30)

                        # Adjust fontsize
                        ax[folder_i, folder_j].tick_params(axis='both', which='major', labelsize=14)


                # Save data
                plt.legend([l1, l2, l3, l4], ['Mixed-precision vectorized', 'Mixed-precision non-vectorized', 'Fixed-precision vectorized', 'Fixed-precision non-vectorized'], bbox_to_anchor=(1.164, 1.0), fontsize=16)
                plt.savefig('plots/vVSn/vec_' + tuner + input_type + str(input_range) + '.png')
                plt.close('all')

def run():
    create_single()
    create_tuner()
    create_input()
    create_vec()

run()
