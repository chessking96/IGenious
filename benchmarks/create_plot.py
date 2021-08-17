#!/usr/bin/env python

import read_config as rc
import sys, math
from helper import nameWithoutExtension, Config
import matplotlib.pyplot as plt
import matplotlib.ticker

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
    #if vectorized == 'yes':
    #    config_file_path += '#vec'
    config_file_path += '.json'

    reps = Config.read_config_from_file(config_file_path).repetitions

    # Get data
    return rc.read_results(path, reps)



def createAllSinglePlots():

    precisions = [6, 8, 10, 12]
    input_types = ['dd', 'd']
    input_ranges = [1]
    vectorized = ['yes', 'no']
    tunings = ['precimonious', 'hifptuner']
    #folder_names = ['linear', 'dot', 'DFT16dd', 'simpsons', 'funarc']
    folder_names = ['simpsons', 'matmul', 'dot', 'DFT16', 'funarc', 'linear', 'newton_root']

    for precision in precisions:
        for input_type in input_types:
            for input_range in input_ranges:
                for vec in vectorized:
                    for tuning in tunings:
                        for folder in folder_names:
                            times, precs, names = getData(precision, input_type, input_range, vec, tuning, folder)
                            precs_fix, times_fix = getFixedData(input_type, input_range, vec, folder)

                            for i in range(len(precs)):
                                precs[i] = -math.log10(precs[i]) * math.log2(10)

                            for i in range(len(precs_fix)):
                                precs_fix[i] = -math.log10(precs_fix[i]) * math.log2(10)

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
                            # plt.xscale('log') #only if accuracy is not measured in bits

                            plt.legend()
                            plot_title = folder + ', precision = 10-' + str(precision) + ', inputPrecision: ' + input_type + ', inputRange: ' + str(input_range) + ', ' + tuning
                            file_name = folder + str(precision) + input_type + str(input_range) + tuning
                            if vec == 'yes':
                                plot_title += ', vectorized'
                            #plt.title(plot_title)

                            plt.ylim(ymin=0)
                            #plt.xlim(xmin=0)


                            plt.savefig('plots_new/singles/' + file_name, bbox_inches='tight')
                            #plt.show()
                            plt.clf()

def createPrecVsHifptuner():

    precisions = [6, 8, 10, 12]
    input_types = ['dd']
    input_ranges = [1]
    vectorized = ['yes']
    folder_names = ['simpsons', 'matmul', 'dot', 'DFT16', 'funarc', 'linear', 'newton_root']

    for precision in precisions:
        for input_type in input_types:
            for input_range in input_ranges:
                for vec in vectorized:
                        for folder in folder_names:
                            times_prec, precs_prec, names_prec = getData(precision, input_type, input_range, vec, 'precimonious', folder)
                            times_hi, precs_hi, names_hi = getData(precision, input_type, input_range, vec, 'hifptuner', folder)

                            precs_fix, times_fix = getFixedData(input_type, input_range, vec, folder)

                            for i in range(len(precs_prec)):
                                precs_prec[i] = -math.log10(precs_prec[i]) * math.log2(10)


                            for i in range(len(precs_hi)):
                                precs_hi[i] = -math.log10(precs_hi[i]) * math.log2(10)

                            for i in range(len(precs_fix)):
                                precs_fix[i] = -math.log10(precs_fix[i]) * math.log2(10)

                            colors = len(precs_prec) * ['blue']
                            plt.scatter(precs_prec, times_prec, c = colors, s = 60, label = 'IGenious with Precimonious')
                            colors = len(precs_hi) * ['green']
                            plt.scatter(precs_hi, times_hi, c = colors, s = 30, label = 'IGenious with HiFPTuner')
                            colors = len(precs_fix) * ['red']
                            plt.scatter(precs_fix, times_fix, c = colors, label = 'No mixed tuning')
                            #for i, txt in enumerate(names_sat_prec):
                            #    plt.annotate(txt, (precs_sat_prec[i], times_sat_prec[i]))


                            # Plot fixed points
                            #colors = len(precs_fix) * ['red']
                            #plt.scatter(precs_fix, times_fix, c = colors, label = 'No mixed tuning')
                            #for i, txt in enumerate(types_fix):
                            #    plt.annotate(txt, (precs_fix[i], times_fix[i]))
                            # plt.xscale('log') #only if accuracy is not measured in bits

                            plt.legend()
                            #plot_title = folder + ', precision = 10-' + str(precision) + ', inputPrecision: ' + input_type + ', inputRange: ' + str(input_range)
                            file_name = folder + str(precision) + input_type + str(input_range)
                            #if vec == 'yes':
                            #    plot_title += ', vectorized'
                            #plt.title(plot_title)

                            plt.ylim(ymin=0)
                            #plt.xlim(xmin=0)


                            plt.savefig('plots_new/precVShifp/' + file_name, bbox_inches='tight')
                            #plt.show()
                            plt.clf()

def createddVSd():
    fig, ax = plt.subplots(4,2, figsize=(10,10))
    fig.delaxes(ax[3, 1])
    fig.tight_layout()

    precisions = [8]
    #input_types = ['dd']
    tunings = ['precimonious']
    input_ranges = [1]
    vectorized = ['yes']
    folder_names = [['simpsons', 'matmul'], ['dot', 'DFT16'], ['funarc', 'linear'], ['newton_root']]

    for precision in precisions:
            #for input_type in input_types:
            for input_range in input_ranges:
                for vec in vectorized:
                    for tuning in tunings:
                        for folder_i in range(len(folder_names)):
                            folder_one = folder_names[folder_i]
                            for folder_j in range(len(folder_one)):
                                folder = folder_one[folder_j]

                                times_d, precs_d, names_d = getData(precision, 'd', input_range, vec, tuning, folder)
                                times_dd, precs_dd, names_dd = getData(precision, 'dd', input_range, vec, tuning, folder)

                                precs_fix_dd, times_fix_dd = getFixedData('dd', input_range, vec, folder)
                                precs_fix_d, times_fix_d = getFixedData('d', input_range, vec, folder)

                                for i in range(len(precs_d)):
                                    precs_d[i] = -math.log10(precs_d[i]) * math.log2(10)

                                for i in range(len(precs_dd)):
                                    precs_dd[i] = -math.log10(precs_dd[i]) * math.log2(10)

                                for i in range(len(precs_fix_d)):
                                    precs_fix_d[i] = -math.log10(precs_fix_d[i]) * math.log2(10)

                                for i in range(len(precs_fix_dd)):
                                    precs_fix_dd[i] = -math.log10(precs_fix_dd[i]) * math.log2(10)

                                colors = len(precs_d) * ['blue']
                                l1 = ax[folder_i, folder_j].scatter(precs_d, times_d, c = colors, s = 60)
                                colors = len(precs_dd) * ['green']
                                l2 = ax[folder_i, folder_j].scatter(precs_dd, times_dd, c = colors, s = 30)
                                colors = len(precs_fix_d) * ['red']
                                l3 = ax[folder_i, folder_j].scatter(precs_fix_d, times_fix_d, c = colors)
                                colors = len(precs_fix_dd) * ['orange']
                                l4 = ax[folder_i, folder_j].scatter(precs_fix_dd, times_fix_dd, c = colors, s = 20)


                                ax[folder_i, folder_j].title.set_text(folder)
                                ax[folder_i, folder_j].yaxis.major.formatter.set_powerlimits((0,0))

                                #for i, txt in enumerate(names_sat_prec):
                                #    plt.annotate(txt, (precs_sat_prec[i], times_sat_prec[i]))

                                #ax[folder_i, folder_j].legend()
                                # Plot fixed points
                                #colors = len(precs_fix) * ['red']
                                #plt.scatter(precs_fix, times_fix, c = colors, label = 'No mixed tuning')
                                #for i, txt in enumerate(types_fix):
                                #    plt.annotate(txt, (precs_fix[i], times_fix[i]))
                                # plt.xscale('log') #only if accuracy is not measured in bits



                                #plot_title = folder + ', precision = 10-' + str(precision) + ', inputRange: ' + str(input_range)
                                file_name = folder + str(precision) + str(input_range) + tuning
                                if vec == 'yes':
                                    file_name += ', vectorized'
                                #plt.title(plot_title)
                                plt.ylim(ymin=0)
                                #plt.xlim(xmin=0)


                                #plt.show()
                        plt.legend([l1, l2, l3, l4], ['Double type', 'Double-Double type', 'Fixed precision Double type', 'Fixed precision Double-Double type'], bbox_to_anchor=(2.05, 0.6))
    plt.subplots_adjust(hspace=0.3, top=0.95)
    plt.savefig('plots_new/ddVSd.png')


def createvecVSnovec():
    precisions = [12]
    input_types = ['dd']
    tunings = ['precimonious']
    input_ranges = [1]
    #ectorized = ['yes']
    folder_names = ['simpsons', 'matmul', 'dot', 'DFT16', 'funarc', 'linear', 'newton_root']

    for precision in precisions:
        for input_type in input_types:
            for input_range in input_ranges:
                    #for vec in vectorized:
                    for tuning in tunings:
                        for folder in folder_names:
                            times_vec, precs_vec, names_vec = getData(precision, input_type, input_range, 'yes', tuning, folder)
                            times_novec, precs_novec, names_novec = getData(precision, input_type, input_range, 'no', tuning, folder)

                            precs_fix, times_fix = getFixedData(input_type, input_range, 'yes', folder)

                            for i in range(len(precs_vec)):
                                precs_vec[i] = -math.log10(precs_vec[i]) * math.log2(10)

                            for i in range(len(precs_novec)):
                                precs_novec[i] = -math.log10(precs_novec[i]) * math.log2(10)

                            for i in range(len(precs_fix)):
                                precs_fix[i] = -math.log10(precs_fix[i]) * math.log2(10)

                            colors = len(precs_vec) * ['blue']
                            plt.scatter(precs_vec, times_vec, c = colors, s = 60, label = 'Vectorized')
                            colors = len(precs_novec) * ['green']
                            plt.scatter(precs_novec, times_novec, c = colors, s = 30, label = 'Non vectorized')
                            colors = len(precs_fix) * ['red']
                            plt.scatter(precs_fix, times_fix, c = colors, label = 'No mixed tuning')
                            #for i, txt in enumerate(names_sat_prec):
                            #    plt.annotate(txt, (precs_sat_prec[i], times_sat_prec[i]))


                            # Plot fixed points
                            #colors = len(precs_fix) * ['red']
                            #plt.scatter(precs_fix, times_fix, c = colors, label = 'No mixed tuning')
                            #for i, txt in enumerate(types_fix):
                            #    plt.annotate(txt, (precs_fix[i], times_fix[i]))
                            # plt.xscale('log') #only if accuracy is not measured in bits

                            plt.legend()
                            #plot_title = folder + ', precision = 10-' + str(precision) + ', inputRange: ' + str(input_range)
                            file_name = folder + str(precision) + input_type + str(input_range) + tuning
                            #plt.title(plot_title)
                            plt.ylim(ymin=0)
                            #plt.xlim(xmin=0)


                            plt.savefig('plots_new/vecVSnovec/' + file_name, bbox_inches='tight')
                            #plt.show()
                            plt.clf()


if __name__ == "__main__":
    #createAllSinglePlots()
    #createPrecVsHifptuner()
    createddVSd()
    #createvecVSnovec()
