#!/usr/bin/env python
import sys, os
import matplotlib.pyplot as plt
sys.path.insert(1, os.path.join(sys.path[0], '../scripts'))
from helper import load_json

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Incorrect number of arguments: " + str(len(sys.argv)))
        sys.exit(-1)
    folder_name = sys.argv[1]


    x = []
    y = []
    z = []

    itr = 0
    while(True):
        path = 'examples/' + folder_name + '/analysis/config_' + str(itr)
        if os.path.exists(path):
            # get time
            with open(path + '/score.cov', 'r') as myfile:
                time = int(myfile.read())
            # get result
            with open(path + '/sat.cov', 'r') as myfile:
                sat = myfile.read()
            if sat == 'true\n':
                sat = True
            else:
                sat = False

            # read config
            with open(path + '/config_temp.json', 'r') as myfile:
                config = load_json(myfile.read())

            f_type = ['float', 'float*']
            d_type = ['double', 'double*']
            dd_type = ['longdouble', 'longdouble*']

            count_float = 0
            count_double = 0
            count_dd = 0

            for i in range(len(config)):
                ty = config[i][1]
                if ty in f_type:
                    count_float += 1
                elif ty in d_type:
                    count_double += 1
                elif ty in dd_type:
                    count_dd += 1
                else:
                    print('Error', ty)

            if sat:
                text = 'dd: ' + str(count_dd) + ' d: ' + str(count_double) + ' f: ' + str(count_float)
                x.append(text)
                y.append(time)
                z.append(itr)

        else:
            break
        itr += 1

    print(x)
    plt.scatter(x, y)
    for i, txt in enumerate(z):
        plt.annotate(txt, (x[i], y[i]))
    plt.show()
