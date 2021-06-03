#!/usr/bin/python
import sys, os, json
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from helper import call, getEnvVar, call_background, load_json

if __name__ == "__main__":
    # arguments: path, filename without extension
    if len(sys.argv) != 3:
        print("Incorrect number of arguments: " + str(len(sys.argv)))
        sys.exit(-1)

    file_path = sys.argv[1]
    file_name = sys.argv[2] # without extension

    scripts_path = getEnvVar('SOURCE_PATH') + '/scripts'

    # for now, to make sure, that c++ is compiled and run
    call('cd ' + scripts_path + '/changeTypes && cmake . && make')
    call(scripts_path + '/changeTypes/clang_ast_visitor IGen/rmd_' + file_name + ' -- ' + file_path + ' ' + file_name + ' > IGen/chg_rmd_' + file_name)

    with open('IGen/funargs.txt', 'r') as myfile:
        funargs = myfile.read()

    with open('config_temp.json', 'r') as myfile:
        config = myfile.read()
