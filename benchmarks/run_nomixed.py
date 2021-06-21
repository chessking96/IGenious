#!/usr/bin/python
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '../scripts'))
from helper import call, readConfig, json, getEnvVar

vectorized = [False]

error_types = ['highestAbsolute']

src_path = getEnvVar('SOURCE_PATH') + '/src'

#folders = ['DFT16', 'DFT16dd', 'dot', 'matmul', 'simpsons']
folders = ['DFT16', 'DFT16dd', 'dot', 'matmul', 'simpsons', 'bisection_root']
file_names = ['DFT16.c', 'DFT16.c', 'dot.c', 'matmul.c', 'simpsons.c', 'bisection_root.c']
types = ['dd', 'd', 'f']

for i in range(len(folders)):
    print('Run:', folders[i])
    folder = folders[i]
    file_name = file_names[i]
    for type in types:
        path = 'examples/' + folder + '/no_mixed/' + type

        call('rm -rf ' + path + '/build')
        call('mkdir ' + path + '/build')

        # copy CMakeLists.txt
        call('cp ' + src_path + '/igen_CMakeLists_nomixed.txt ' + path + '/build/CMakeLists.txt')

        # copy code
        call('cp ' + path + '/' + file_name + ' ' + path + '/build')
        call('cp ' + path + '/main.c ' + path + '/build')
        call('cp ' + src_path + '/random_range_igen.c ' + path + '/build/random_range.c')

        # compile
        call('cd ' + path + '/build && cmake . && make')

        # execute
        call('cd ' + path + '/build && ./some_app')
