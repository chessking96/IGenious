#!/usr/bin/python
from helper import call
import sys

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Wrong number of arguments.")
        sys.exit(-1)

    path = sys.argv[1]
    file_name = sys.argv[2]
    config = sys.argv[3]

    call('rm -rf ' + path + 'analysis_' + config)
    call('rm -rf ' + path + 'analysis')
    call('mkdir ' + path + 'analysis')
    call('cp ' + path + file_name + ' ' + path + '/analysis/' + file_name)

    print(file_name + 'restored.')
