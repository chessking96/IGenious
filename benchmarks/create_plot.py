#!/usr/bin/env python

import read_config as rc
import sys, math
from helper import nameWithoutExtension, Config
import matplotlib.pyplot as plt
import matplotlib.ticker
from matplotlib.ticker import MaxNLocator

class OOMFormatter(matplotlib.ticker.ScalarFormatter):
    def _init_(self, order=0, fformat="%1.1f", offset=True, mathText=True):
        self.oom = order
        self.fformat = fformat
        matplotlib.ticker.ScalarFormatter._init_(self,useOffset=offset,useMathText=mathText)
    def _set_order_of_magnitude(self):
        self.orderOfMagnitude = self.oom
    def _set_format(self, vmin=None, vmax=None):
        self.format = self.fformat
        if self._useMathText:
             self.format = r'$\mathdefault{%s}$' % self.format

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
        if vectorized:
            config_file_path += '#vec'
        config_file_path += '.json'

        reps = Config.read_config_from_file(config_file_path).repetitions


        if vectorized:
            run_path += '#vec'
        # Get time
        with open(run_path + '/igen_setup/score.cov', 'r') as myfile:
            time = int(myfile.read())
        # Get precision
        with open(run_path + '/igen_setup/precision.cov', 'r') as myfile:
            prec = float(myfile.read())

        # temporary issue
        if folder_name == 'funarc' or folder_name == 'simpsons' or folder_name == 'newton_root':
            time /= 10

        times_fix.append(time / reps)
        precs_fix.append(prec)

    return precs_fix, times_fix

def getData(precision, input_type, input_range, vectorized, tuning, folder_name):
    # Build path
    config_base_name = 'config_' + str(precision) + '#' + str(input_type) + '#' + str(input_range) + '#'
    if vectorized:
        config_base_name += 'vec#'
    if tuning == 'precimonious':
        config_name = config_base_name + 'precimonious'
    else:
        config_name = config_base_name + 'hifptuner'
    name_wo_ext = config_name

    path = 'examples/' + folder_name + '/analysis_' + name_wo_ext

    # Get number of repetions from configuration file
    config_file_path = 'examples/' + folder_name + '/' + config_name

    config_file_path += '.json'

    reps = Config.read_config_from_file(config_file_path).repetitions

    # Get data
    return rc.read_results(path, reps)



def createAllSinglePlots():
    precisions = [6, 8, 10, 12]

    input_types = ['d', 'dd']
    #tunings = ['precimonious', 'hifptuner']
    input_ranges = [10]
    vectorized = [True, False]
    folder_names = [['simpsons', 'matmul'], ['dot', 'DFT16'], ['funarc', 'linear'], ['newton_root']]

    #for input_type in input_types:
    for input_range in input_ranges:
        for vec in vectorized:
            for in_type in input_types:

                fig, ax = plt.subplots(4,2, figsize=(10,10))
                fig.tight_layout()
                fig.delaxes(ax[3, 1])

                plt.subplots_adjust(hspace=0.7, wspace=0.3, top=0.95, left=0.08, bottom=0.05)

                for folder_i in range(len(folder_names)):
                    folder_one = folder_names[folder_i]

                    for folder_j in range(len(folder_one)):
                        folder = folder_one[folder_j]
                        ax[folder_i, folder_j].xaxis.set_major_locator(MaxNLocator(integer=True))
                        ax[folder_i, folder_j].yaxis.set_major_locator(MaxNLocator(integer=True))
                        #ax[folder_i, folder_j].set_ylim(0, 12)


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



                        #times_d, precs_d, names_d = getData(precision, 'd', input_range, vec, tuning, folder)
                        #times_dd, precs_dd, names_dd = getData(precision, 'dd', input_range, vec, tuning, folder)

                        precs_fix_p, times_fix_p = getFixedData(in_type, input_range, vec, folder)


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


                        ax[folder_i, folder_j].set_title(folder, size=18)
                        #ax[folder_i, folder_j].yaxis.major.formatter.set_powerlimits((0,0))
                        ax[folder_i, folder_j].set_ylabel('speedup', fontsize=14)
                        ax[folder_i, folder_j].set_xlabel('#correct bits', fontsize=14)


                        colors = len(precs_p) * ['blue']
                        l1 = ax[folder_i, folder_j].scatter(precs_p, times_p, c = colors, s = 100)
                        colors = len(precs_fix_p) * ['red']
                        l3 = ax[folder_i, folder_j].scatter(precs_fix_p, times_fix_p, c = colors, s= 40)

                        ax[folder_i, folder_j].tick_params(axis='both', which='major', labelsize=14)



                plt.legend([l1, l3], ['IGenious', 'Fixed precision'], bbox_to_anchor=(2.1, 0.8), fontsize=16)
                plt.savefig('plots_new/singles/single_' + in_type + str(vec) + str(input_range) + '.png')
                plt.close('all')


def createPrecVsHifptuner():
    precisions = [6, 8, 10, 12]

    input_types = ['d', 'dd']
    #tunings = ['precimonious', 'hifptuner']
    input_ranges = [10]
    vectorized = [True, False]
    folder_names = [['simpsons', 'matmul'], ['dot', 'DFT16'], ['funarc', 'linear'], ['newton_root']]

    #for input_type in input_types:
    for input_range in input_ranges:
        for vec in vectorized:
            for in_type in input_types:

                fig, ax = plt.subplots(4,2, figsize=(10,10))
                fig.tight_layout()
                fig.delaxes(ax[3, 1])

                plt.subplots_adjust(hspace=0.7, wspace=0.3, top=0.95, left=0.08, bottom=0.05)

                for folder_i in range(len(folder_names)):
                    folder_one = folder_names[folder_i]

                    for folder_j in range(len(folder_one)):
                        folder = folder_one[folder_j]
                        ax[folder_i, folder_j].xaxis.set_major_locator(MaxNLocator(integer=True))
                        ax[folder_i, folder_j].yaxis.set_major_locator(MaxNLocator(integer=True))
                        #ax[folder_i, folder_j].set_ylim(0, 12)


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



                        #times_d, precs_d, names_d = getData(precision, 'd', input_range, vec, tuning, folder)
                        #times_dd, precs_dd, names_dd = getData(precision, 'dd', input_range, vec, tuning, folder)

                        precs_fix_p, times_fix_p = getFixedData(in_type, input_range, vec, folder)


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


                        ax[folder_i, folder_j].set_title(folder, size=18)
                        #ax[folder_i, folder_j].yaxis.major.formatter.set_powerlimits((0,0))
                        ax[folder_i, folder_j].set_ylabel('speedup', fontsize=14)
                        ax[folder_i, folder_j].set_xlabel('#correct bits', fontsize=14)


                        colors = len(precs_p) * ['blue']
                        l1 = ax[folder_i, folder_j].scatter(precs_p, times_p, c = colors, s = 110)
                        colors = len(precs_h) * ['green']
                        l2 = ax[folder_i, folder_j].scatter(precs_h, times_h, c = colors, s = 60)
                        colors = len(precs_fix_p) * ['red']
                        l3 = ax[folder_i, folder_j].scatter(precs_fix_p, times_fix_p, c = colors, s= 40)

                        ax[folder_i, folder_j].tick_params(axis='both', which='major', labelsize=14)



                plt.legend([l1, l2, l3], ['Precimonious', 'HiFPTuner', 'Fixed precision'], bbox_to_anchor=(2.1, 0.9), fontsize=16)
                plt.savefig('plots_new/pVSh/tuner_' + in_type + str(vec) + str(input_range) + '.png')
                plt.close('all')


def createddVSd():
    precisions = [6, 8, 10, 12]

    #input_types = ['dd']
    tunings = ['precimonious', 'hifptuner']
    input_ranges = [10]
    vectorized = [True, False]
    folder_names = [['linear', 'matmul'], ['dot', 'DFT16']]

    #for input_type in input_types:
    for input_range in input_ranges:
        for vec in vectorized:
            for tuner in tunings:

                fig, ax = plt.subplots(2,2, figsize=(10,7.5))
                fig.tight_layout()
                #fig.delaxes(ax[3, 1])

                plt.subplots_adjust(hspace=0.7, wspace=0.3, top=0.94, left=0.08, bottom=0.3)


                for folder_i in range(len(folder_names)):
                    folder_one = folder_names[folder_i]

                    for folder_j in range(len(folder_one)):
                        folder = folder_one[folder_j]
                        ax[folder_i, folder_j].xaxis.set_major_locator(MaxNLocator(integer=True))
                        ax[folder_i, folder_j].yaxis.set_major_locator(MaxNLocator(integer=True))
                        #ax[folder_i, folder_j].set_ylim(0, 12)


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



                        #times_d, precs_d, names_d = getData(precision, 'd', input_range, vec, tuning, folder)
                        #times_dd, precs_dd, names_dd = getData(precision, 'dd', input_range, vec, tuning, folder)

                        precs_fix_dd, times_fix_dd = getFixedData('dd', input_range, vec, folder)
                        precs_fix_d, times_fix_d = getFixedData('d', input_range, vec, folder)

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

                        ax[folder_i, folder_j].set_title(folder, size=18)
                        #ax[folder_i, folder_j].yaxis.major.formatter.set_powerlimits((0,0))
                        ax[folder_i, folder_j].set_ylabel('speedup', fontsize=14)
                        ax[folder_i, folder_j].set_xlabel('#correct bits', fontsize=14)


                        colors = len(precs_d) * ['blue']
                        l1 = ax[folder_i, folder_j].scatter(precs_d, times_d, c = colors, s = 140)
                        colors = len(precs_dd) * ['green']
                        l2 = ax[folder_i, folder_j].scatter(precs_dd, times_dd, c = colors, s = 80)
                        colors = len(precs_fix_d) * ['red']
                        l3 = ax[folder_i, folder_j].scatter(precs_fix_d, times_fix_d, c = colors, s= 60)
                        colors = len(precs_fix_dd) * ['orange']
                        l4 = ax[folder_i, folder_j].scatter(precs_fix_dd, times_fix_dd, c = colors, s = 40)

                        ax[folder_i, folder_j].tick_params(axis='both', which='major', labelsize=14)



                plt.legend([l1, l2, l3, l4], ['Double input', 'Double-double input', 'Fixed precision double input', 'Fixed precision double-double input'], bbox_to_anchor=(0.5, -0.4), fontsize=16)
                plt.savefig('plots_new/ddVSd/input_' + str(vec) + tuner + str(input_range) + '.png')
                plt.close('all')


def createvecVSnovec():
    precisions = [6, 8, 10, 12]
    input_types = ['dd', 'd']
    tunings = ['precimonious', 'hifptuner']
    input_ranges = [10]
    #vectorized = [True, False]
    folder_names = [['simpsons', 'matmul'], ['dot', 'DFT16'], ['funarc', 'linear'], ['newton_root']]

    for input_type in input_types:
        for input_range in input_ranges:
        #for vec in vectorized:
            for tuner in tunings:

                fig, ax = plt.subplots(4,2, figsize=(10,10))
                fig.tight_layout()
                fig.delaxes(ax[3, 1])

                plt.subplots_adjust(hspace=0.7, wspace=0.3, top=0.95, left=0.08, bottom=0.05)


                for folder_i in range(len(folder_names)):
                    folder_one = folder_names[folder_i]

                    for folder_j in range(len(folder_one)):
                        folder = folder_one[folder_j]
                        ax[folder_i, folder_j].xaxis.set_major_locator(MaxNLocator(integer=True))
                        ax[folder_i, folder_j].yaxis.set_major_locator(MaxNLocator(integer=True))
                        #ax[folder_i, folder_j].set_ylim(0, 12)


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
                            #if vec:
                            #    config_name += '#vec'
                            config_name += '#' + tuner
                            config_folder = 'analysis_' + config_name
                            path = 'examples/' + folder + '/' + config_folder
                            with open(path + '/result.txt') as myfile:
                                result = myfile.read().split(',')
                            if int(result[0]) != -1:
                                times_n.append(float(result[1]))
                                precs_n.append(float(result[2]))

                        precs_fix_v, times_fix_v = getFixedData(input_type, input_range, True, folder)
                        precs_fix_n, times_fix_n = getFixedData(input_type, input_range, False, folder)

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

                        ax[folder_i, folder_j].set_title(folder, size=18)
                        ax[folder_i, folder_j].set_ylabel('speedup', fontsize=14)
                        ax[folder_i, folder_j].set_xlabel('#correct bits', fontsize=14)


                        colors = len(precs_v) * ['blue']
                        l1 = ax[folder_i, folder_j].scatter(precs_v, times_v, c = colors, s = 100)
                        colors = len(precs_n) * ['green']
                        l2 = ax[folder_i, folder_j].scatter(precs_n, times_n, c = colors, s = 60)
                        colors = len(precs_fix_v) * ['red']
                        l3 = ax[folder_i, folder_j].scatter(precs_fix_v, times_fix_v, c = colors, s= 45)
                        colors = len(precs_fix_n) * ['orange']
                        l4 = ax[folder_i, folder_j].scatter(precs_fix_n, times_fix_n, c = colors, s = 30)

                        ax[folder_i, folder_j].tick_params(axis='both', which='major', labelsize=14)



                plt.legend([l1, l2, l3, l4], ['Vectorized', 'Non-vectorized', 'Fixed precision vectorized', 'Fixed precision non-vectorized'], bbox_to_anchor=(1.2, 1.0), fontsize=16)
                plt.savefig('plots_new/vVSn/vec_' + tuner + input_type + str(input_range) + '.png')
                plt.close('all')


if __name__ == "__main__":
    #createAllSinglePlots()
    #createPrecVsHifptuner()
    #createddVSd()
    createvecVSnovec()
