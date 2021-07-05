import subprocess, signal, json
import os, sys, re, time

def call(arg):
    res = subprocess.call([arg], shell=True) #remove shell...
    if res != 0:
        if res == 10:
            print('Timeout1')
        else:
            print("Call Error", arg)
            sys.exit(-1)

def call_background(arg):
    res = subprocess.call([arg], shell=True, stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w')) #remove shell...
    if res != 0:
        if res == 10:
            print('Timeout2')
        else:
            print("Call Error", arg)
            sys.exit(-1)


def getEnvVar(arg):
    return os.getenv(arg)

def nameWithoutExtension(arg):
    return os.path.splitext(arg)[0]

# self made json load, as standard json load doesn't work for this file
def load_json(string):
    return re.findall("localVar\": {\n\t\t\"function\": \"(.+(?=\"))\",\n\t\t\"type\": \"(.+(?=\"))\",\n\t\t\"name\": \"(.+(?=\"))", string, re.MULTILINE)

def readConfig(path):
    with open(path, 'r') as myfile:
        data = json.load(myfile)
    file_name = data['filename']
    function_name = data['functionname']
    args_list = data['args']
    if len(args_list) % 4 != 0:
        printf('Args in config file are not valid.')
        sys.exit(-1)
    args = []
    for i in range(int(len(args_list) / 4)):
        args.append((args_list[4 * i + 0], args_list[4 * i + 1], args_list[4 * i + 2], args_list[4 * i + 3]))
    ret = data["return"]
    rep = data["repetitions"]
    prec = data["precision"]
    err_type = data["errortype"]
    use_vectorized = data["vectorized"]
    max_prec_iterations = data["maxpreciterations"]
    tuning = data["tuning"]
    input_prec = data["input_prec"]
    input_range = data["input_range"]

    return file_name, function_name, args, ret, rep, prec, err_type, use_vectorized, max_prec_iterations, tuning, input_prec, input_range

# Standart docker call
def dockerCall(arg):
    call_background('docker exec hi ' + arg)

# Docker call with llvm 3.0 activated
def dockerCall30(arg):
    dockerCall('bash -c "export LLVM_VERSION=llvm-3.0 && export LD_LIBRARY_PATH=/root/llvm-3.0/lib && export CPATH=/root/llvm-3.0/include:. && export PATH=/root/llvm-3.0/bin:/root/llvm-3.0/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin && ' + arg + '"')

# Docker call with llvm 3.8 activated
def dockerCall38(arg):
    dockerCall('bash -c "export LLVM_VERSION=llvm-3.8 && export LD_LIBRARY_PATH=/root/llvm-3.8/lib && export CPATH=/root/llvm-3.8/include:. && export PATH=/root/llvm-3.8/bin:/root/llvm-3.8/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin && ' + arg + '"')
