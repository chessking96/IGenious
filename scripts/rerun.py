#!/usr/bin/python
import sys
from helper import call, getEnvVar

if __name__ == "__main__":
    # arguments: path, filename, functionname, filename (only for now, without extension), config_number
    if len(sys.argv) != 6:
        print("Wrong number of arguments.")
        sys.exit(-1)

    path = sys.argv[1]
    file_name = sys.argv[2]
    func_name = sys.argv[3]
    file_name_wo = sys.argv[4]
    config = sys.argv[5]

    # Prepare
    call('cd ' + path + ' && cp config_' + config + '.json config.json')

    # Restore
    source_path = getEnvVar('SOURCE_PATH')
    call('python3 ' + source_path + '/scripts/restore.py ' + path + ' ' + file_name + ' ' + config)
    print('Restore succeeded')

    # Prepare Setup
    call('python3 ' + source_path + '/scripts/setup.py ' + path + ' ' + file_name + ' ' + func_name + ' no')
    print('Setup succeeded')

    # Run
    corvette_path = getEnvVar('CORVETTE_PATH')
    call('cd ' + path + 'analysis && python2 -O ' + corvette_path
    + '/scripts/dd2.py ' + file_name_wo + '.bc search_' + file_name_wo
    + '.json config_' + file_name_wo + '.json ' + path + ' ' + file_name_wo + ' ' + func_name)

    call('cd ' + path + ' && mv analysis analysis_' + config)
    call('cd ' + path + ' && rm config.json')
    print('Run succeeded')
