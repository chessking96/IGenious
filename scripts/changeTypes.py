#!/usr/bin/python
import sys, os, json
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from helper import call, getEnvVar, call_background, load_json

def run(file_name):

    scripts_path = getEnvVar('SOURCE_PATH') + '/scripts'
    igen_src = getEnvVar('IGEN_PATH')

    # Make sure, that the clang_ast_vistor latest version is compiled
    call_background('cd ' + scripts_path + '/changeTypes && cmake . && make')

    # Run clang_ast_visitor
    call_background(scripts_path + '/changeTypes/clang_ast_visitor ../igen_setup/rmd_' + file_name + ' -- ' + ' > ../igen_setup/chg_rmd_' + file_name)

    # Call IGen
    call_background('python3 ' + igen_src + '/bin/igen.py ../igen_setup/chg_rmd_' + file_name)
