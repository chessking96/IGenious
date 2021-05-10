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
    # change variable types
    scripts_path = getEnvVar("SOURCE_PATH") + '/scripts'
    call('python ' + scripts_path + '/changeTypes.py ' + sys.argv[1] + ' ' + sys.argv[2])

    # call IGen
    igen_path = getEnvVar('IGEN_PATH')
    call_background('python3 ' + igen_path + '/bin/igen.py' + ' IGen/chg_rmd_' + sys.argv[2] + '.c')

    # compile and execute
    call('cp' + ' IGen/chg_rmd_' + sys.argv[2]+ '.c' + ' IGen/make_code.c')
    call_background("cd IGen && cmake . && make")
    call("./IGen/some_app")


if __name__ == "__main__":
    main()
