#!/usr/bin/env python
import sys, os
import matplotlib.pyplot as plt
sys.path.insert(1, os.path.join(sys.path[0], '../scripts'))
from helper import load_json

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Incorrect number of arguments: " + str(len(sys.argv)))
        sys.exit(-1)
    folder_name = sys.argv[1]
    config_num = sys.argv[2]
    is_vec = sys.argv[3]
    plot_type = sys.argv[4]


    x = []
    y = []
    z = []
    precisions = []

    itr = 0
    if is_vec == 'yes':
        print('vectorized')
        folder = 'examples_vectorized/'
    elif is_vec == 'no':
        print('not vectorized')
        folder = 'examples_no_vectorized/'

    folder = 'examples/'

    if is_vec == 'yes' or is_vec == 'no':
        while(True):
            path = folder + folder_name + '/analysis_' + str(config_num) + '/config_' + str(itr)
            print(path)
            if os.path.exists(path):
                # get time
                with open(path + '/score.cov', 'r') as myfile:
                    time = int(myfile.read())
                # get result
                with open(path + '/sat.cov', 'r') as myfile:
                    sat = myfile.read()
                # get precision
                with open(path + '/precision.cov', 'r') as myfile:
                    prec = float(myfile.read())
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
                    text = str(itr) + ' dd: ' + str(count_dd) + ' d: ' + str(count_double) + ' f: ' + str(count_float)
                    x.append(text)
                    y.append(time)
                    z.append(itr)
                    precisions.append(prec)

            else:
                break
            itr += 1

        print(x)
        if plot_type == 'tr':
            plt.scatter(x, y)
            for i, txt in enumerate(z):
                plt.annotate(txt, (x[i], y[i]))
            plt.show()
        elif plot_type == 'er':
            plt.scatter(precisions, y)
            for i, txt in enumerate(x):
                plt.annotate(txt, (precisions[i], y[i]))

            plt.xscale("log")
            plt.xlabel('precision')
            plt.ylabel('time')
            plt.show()
    else:
        x_vec = []
        y_vec = []
        z_vec = []
        precisions_vec = []
        folder = 'examples_vectorized/'
        while(True):
            path = folder + folder_name + '/analysis_' + str(config_num) + '/config_' + str(itr)
            print(path)
            if os.path.exists(path):
                # get time
                with open(path + '/score.cov', 'r') as myfile:
                    time = int(myfile.read())
                # get result
                with open(path + '/sat.cov', 'r') as myfile:
                    sat = myfile.read()
                # get precision
                with open(path + '/precision.cov', 'r') as myfile:
                    prec = float(myfile.read())
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
                    text = str(itr) + ' dd: ' + str(count_dd) + ' d: ' + str(count_double) + ' f: ' + str(count_float)
                    x_vec.append(text)
                    y_vec.append(time)
                    z_vec.append(itr)
                    precisions_vec.append(prec)

            else:
                break
            itr += 1

        itr = 0
        x_no = []
        y_no = []
        z_no = []
        precisions_no = []
        folder = 'examples_no_vectorized/'
        while(True):
            path = folder + folder_name + '/analysis_' + str(config_num) + '/config_' + str(itr)
            print(path)
            if os.path.exists(path):
                # get time
                with open(path + '/score.cov', 'r') as myfile:
                    time = int(myfile.read())
                # get result
                with open(path + '/sat.cov', 'r') as myfile:
                    sat = myfile.read()
                # get precision
                with open(path + '/precision.cov', 'r') as myfile:
                    prec = float(myfile.read())
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
                    text = str(itr) + ' dd: ' + str(count_dd) + ' d: ' + str(count_double) + ' f: ' + str(count_float)
                    x_no.append(text)
                    y_no.append(time)
                    z_no.append(itr)
                    precisions_no.append(prec)

            else:
                break
            itr += 1
        print('time vec', y_vec)
        print('time wo vec', y_no)
        colors = len(x_no) * ['green']
        plt.scatter(x_no, y_no, c = colors)
        for i, txt in enumerate(x_no):
            plt.annotate(txt, (x_no[i], y_no[i]))

        colors = len(x_vec) * ['red']
        plt.scatter(x_vec, y_vec, c=colors)
        for i, txt in enumerate(x_vec):
            plt.annotate(txt, (x_vec[i], y_vec[i]))



        #plt.xscale("log")
        #plt.xlabel('precision')
        #plt.ylabel('time')
        plt.show()
