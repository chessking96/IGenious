#!/usr/bin/env python

import sys, os
import json
import re
import subprocess

def main():

  #read original code
  with open ("code_temp.c", "r") as myfile:
    c = myfile.read()

  #read original config
  orig_types = json.loads(open('config_orig.json', 'r').read())["config"]

  #read config file
  with open("config_temp.json", "r") as myfile:
    replacements = load_json(myfile.read())

  #print(c)
  #print()
  #print(orig_types)
  #print()
  #print(replacements)





  dict = {}
  #print("origtypes: " + str(orig_types[0]['localVar']['name']))
  for i in range(len(orig_types)):
    #print(replacements[i])
    dict[(orig_types[i]['localVar']['function'], orig_types[i]['localVar']['name'])] = orig_types[i]['localVar']['type']

  #print(dict)

  for rep in replacements:
    #new
    #print("or: " + str(rep))
    fname = rep[0]
    new_type = rep[1]
    if new_type == 'longdouble':
      new_type = 'long double'
    varname = rep[2]

    #orig
    orig_type = dict[rep[0], rep[2]]
    if orig_type == 'longdouble':
      orig_type = 'long double'
    #print("to: " + new_type)
    regexpr1 = r'([\t\r (]+)' + orig_type + r'([\t\r (]+)' + varname
    regexpr2 = r'\1' + new_type + r'\2' + varname
    c = re.sub(regexpr1, regexpr2, c)
  

  #print(c)
  #subprocess.call(["python3 ../sleep.py"], shell=True) #remove shell...
  #print(json_str)
  #data = json.loads(json_str)
  #print(json.dumps(data, indent=4, sort_keys=True))
  #print(data["localVar"])

  f = open("code_rep.c", "w+")
  f.write(c)
  f.close()

  subprocess.call(["python3 ../../IGen/bin/igen.py code_rep.c"], shell=True) #remove shell...

  
  subprocess.call(["cp code_rep.c orig_code_rep.c"], shell=True) #remove shell...
  subprocess.call(["cp igen_code_rep.c code_rep.c"], shell=True) #remove shell...

  #subprocess.call(["python3 ../sleep.py"], shell=True) #remove shell...

  
  subprocess.call(["cmake . && make"], shell=True) #remove shell...
  subprocess.call(["./some_app"], shell=True) #remove shell...

  

  return 0


#Get function name, variable name and type out of json file
def load_json(string):
  x = re.findall("localVar\": {\n\t\t\"function\": \"(.+(?=\"))\",\n\t\t\"type\
\": \"(.+(?=\"))\",\n\t\t\"name\": \"(.+(?=\"))", string, re.MULTILINE)
  #print(x)
  return x


if __name__ == "__main__":
  main()
