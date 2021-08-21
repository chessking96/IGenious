from helper import call
import os

folders = ['funarc', 'linear', 'newton_root', 'DFT16', 'DFT16dd', 'dot', 'matmul', 'simpsons']
precisions = [2, 4, 6, 8, 10, 12, 14, 16]
vectorized = [True, False]
tunings = ['hifptuner', 'precimonious']
input_precisions = ['dd', 'd']
input_ranges = [1, 10, 30]

for folder in folders:
    for prec in precisions:
        for vec in vectorized:
            for tuning in tunings:
                for inp in input_precisions:
                    for range in input_ranges:
                        config_name = 'config_' + str(prec) + '#' + inp + '#' + str(range)
                        if vec:
                            config_name += '#vec'
                        config_name += '#' + tuning
                        config_folder = 'analysis_' + config_name
                        path = 'examples/' + folder + '/' + config_folder

                        try:
                            call('cd ' + path + ' && rm -rf CMakefiles')
                        except:
                            print(path)

                        num = 0
                        while(True):
                            run_path = path + '/' + str(num)
                            # Check if this run exists
                            if not os.path.exists(run_path):
                                break

                            try:
                                call('cd ' + run_path + ' && rm -rf CMakeFiles')
                                call('cd ' + run_path + ' && rm -rf CMakeCache.txt')
                                call('cd ' + run_path + ' && rm -rf cmake_install.cmake')
                                call('cd ' + run_path + ' && rm -rf Makefile')
                                call('cd ' + run_path + ' && rm -rf some_app')

                            except:
                                print(run_path)

                            num += 1

print('Finished')
