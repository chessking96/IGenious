#!/usr/bin/env python

import sys, os
import json
import re
import subprocess
from helper import call, getEnvVar

def main():
    file_path = sys.argv[1]
    file_name = sys.argv[2]
    #read original code
    with open ('IGen/rmd_' + file_name + '.c', 'r') as myfile:
        c = myfile.read()

    #read original config
    orig_types = json.loads(open('config_' + file_name + '.json', 'r').read())["config"]

    #read config file
    with open("config_temp.json", "r") as myfile:
        replacements = load_json(myfile.read())

    dict = {}

    for i in range(len(orig_types)):
        if 'call' in orig_types[i].keys():
            continue

        dict[(orig_types[i]['localVar']['function'], orig_types[i]['localVar']['name'])] = orig_types[i]['localVar']['type']

    for rep in replacements:
        #new
        fname = rep[0]
        new_type = rep[1]
        if new_type == 'longdouble':
            new_type = 'long double'
        varname = rep[2]

        #orig
        orig_type = dict[rep[0], rep[2]]
        if orig_type == 'longdouble':
            orig_type = 'long double'
        regexpr1 = r'([\t\r (]+)' + orig_type + r'([\t\r (]+)' + varname
        regexpr2 = r'\1' + new_type + r'\2' + varname
        c = re.sub(regexpr1, regexpr2, c)



    with open('IGen/chg_rmd_' + file_name + '.c', 'w') as f:
        f.write(c)

    igen_path = getEnvVar('IGEN_PATH')
    call('python3 ' + igen_path + '/bin/igen.py IGen/chg_rmd_' + file_name + '.c')

    call('cp IGen/chg_rmd_' + file_name + '.c ' + 'IGen/make_code.c')

    call("cd IGen && cmake . && make")
    call("./IGen/some_app")

    return 0


#Get function name, variable name and type out of json file
def load_json(string):
    x = re.findall("localVar\": {\n\t\t\"function\": \"(.+(?=\"))\",\n\t\t\"type\": \"(.+(?=\"))\",\n\t\t\"name\": \"(.+(?=\"))", string, re.MULTILINE)
    return x


if __name__ == "__main__":
    main()
