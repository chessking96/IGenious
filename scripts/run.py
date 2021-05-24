#!/usr/bin/env python

import sys, os
import json
import re
import subprocess
from helper import call, call_background, getEnvVar

# self made json load, as standard json load doesn't work for this file
def load_json(string):
    return re.findall("localVar\": {\n\t\t\"function\": \"(.+(?=\"))\",\n\t\t\"type\": \"(.+(?=\"))\",\n\t\t\"name\": \"(.+(?=\"))", string, re.MULTILINE)


def main():
    if len(sys.argv) != 3:
        print("Incorrect number of arguments: " + str(len(sys.argv)))
        sys.exit(-1)

    file_path = sys.argv[1] + 'analysis/'
    file_name_wo = sys.argv[2]
    file_name = file_name_wo + '.c'

    # change variable types
    scripts_path = getEnvVar("SOURCE_PATH") + '/scripts'
    call('python ' + scripts_path + '/changeTypes.py ' + file_path + 'IGen/ ' + file_name)
    # call IGen
    igen_path = getEnvVar('IGEN_PATH')
    call_background('python3 ' + igen_path + '/bin/igen.py' + ' IGen/chg_rmd_' + file_name)
    # compile and execute
    call('cp' + ' IGen/chg_rmd_' + file_name + ' IGen/make_code.c')
    call_background("cd IGen && cmake . && make")
    call("./IGen/some_app")


if __name__ == "__main__":
    main()
