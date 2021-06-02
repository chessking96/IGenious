import subprocess
import os, sys, re

def call(arg):
    res = subprocess.call([arg], shell=True) #remove shell...
    if res != 0:
        print("Call Error", arg)
        sys.exit(-1)

def call_background(arg):
    res = subprocess.call([arg], shell=True, stdout=open(os.devnull, 'w')) #remove shell...
    if res != 0:
        print("Call Error", arg)
        sys.exit(-1)

def getEnvVar(arg):
    return os.getenv(arg)

def nameWithoutExtension(arg):
    return os.path.splitext(arg)[0]

# self made json load, as standard json load doesn't work for this file
def load_json(string):
    return re.findall("localVar\": {\n\t\t\"function\": \"(.+(?=\"))\",\n\t\t\"type\": \"(.+(?=\"))\",\n\t\t\"name\": \"(.+(?=\"))", string, re.MULTILINE)
