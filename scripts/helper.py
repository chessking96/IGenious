import subprocess
import os, sys

def call(arg):
    res = subprocess.call([arg], shell=True) #remove shell...
    if res != 0:
        print("Error")
        sys.exit(-1)

def call_background(arg):
    res = subprocess.call([arg], shell=True, stdout=open(os.devnull, 'w')) #remove shell...
    if res != 0:
        print("Call Error")
        sys.exit(-1)

def getEnvVar(arg):
    return os.getenv(arg)

def nameWithoutExtension(arg):
    return os.path.splitext(arg)[0]
