import subprocess, signal, json
import os, sys, re, time

class Argument:
    type = 'long double'
    length = 100
    ptr_type = 'pointer'
    input_or_output = 'input'

    def __init__(self, type, length, ptr_type, in_or_out):
        self.type = type
        self.length = length
        self.ptr_type = ptr_type
        self.input_or_output = in_or_out

    def get_argument_as_string(self):
        return '"' + self.type + '", ' + str(self.length) + ', "'\
        + self.ptr_type + '", "' + self.input_or_output + '"'

class Config:
    file_name = ''
    function_name = ''
    function_args = []
    return_info = ['False', 'long double', 1, 'scalar']
    repetitions = 1
    precision = -10
    error_type = 'highest_absolute'
    vectorized = False
    max_iterations = 200
    tuning_algo = 'precimonious'
    input_precision = 'dd'
    rng_range = 1

    def __init__(self, file, fun, args, ret, rep, prec, err_t, vec, max_iter, algo, input_prec, rng_range):
        self.file_name = file
        self.function_name = fun
        self.function_args = args
        self.return_info = ret
        self.repetitions = rep
        self.precision = prec
        self.error_type = err_t
        self.vectorized = vec
        self.max_iterations = max_iter
        self.tuning_algo = algo
        self.input_precision = input_prec
        self.rng_range = rng_range

    def get_config_as_string(self):

        # Build string for arguments
        args_string = '['
        for i in range(len(self.function_args) - 1):
            arg = self.function_args[i]
            args_string += arg.get_argument_as_string() + ', '
        if len(self.function_args) >= 1:
            arg = self.function_args[-1]
            args_string += arg.get_argument_as_string()
        args_string  += ']'

        # Build string for configuration file
        config = '{\n'
        config += '\t"filename": "' + self.file_name + '",\n'
        config += '\t"functionname": "' + self.function_name + '",\n'
        config += '\t"args": ' + args_string + ',\n'
        config += '\t"return": ' + json.dumps(self.return_info) + ',\n' # Maybe change this
        config += '\t"repetitions": ' + str(self.repetitions) + ',\n'
        config += '\t"precision": ' + str(self.precision) + ',\n'
        config += '\t"errortype": "' + self.error_type + '",\n'
        config += '\t"vectorized": "' + str(self.vectorized) + '",\n'
        config += '\t"maxpreciterations": ' + str(self.max_iterations) + ',\n'
        config += '\t"tuning": "' + self.tuning_algo + '",\n'
        config += '\t"input_prec": "' + self.input_precision + '",\n'
        config += '\t"input_range": ' + str(self.rng_range)
        config += '}'

        return config

    @staticmethod
    def read_config_from_file(file_path):
        with open(file_path, 'r') as myfile:
            data = json.load(myfile)
        file_name = data['filename']
        function_name = data['functionname']
        args_list = data['args']

        # Read arguments
        if len(args_list) % 4 != 0:
            printf('Args in config file are not valid.')
            sys.exit(-1)
        args = []
        for i in range(int(len(args_list) / 4)):
            args.append(Argument(args_list[4 * i + 0], args_list[4 * i + 1]
            , args_list[4 * i + 2], args_list[4 * i + 3]))

        ret = data["return"]
        rep = data["repetitions"]
        prec = data["precision"]
        err_type = data["errortype"]
        use_vectorized = data["vectorized"]
        max_prec_iterations = data["maxpreciterations"]
        tuning = data["tuning"]
        input_prec = data["input_prec"]
        input_range = data["input_range"]

        return Config(file_name, function_name, args, ret, rep, prec, err_type
        , use_vectorized, max_prec_iterations, tuning, input_prec, input_range)



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


# Standart docker call
def dockerCall(arg):
    call_background('docker exec hi ' + arg)

# Docker call with llvm 3.0 activated
def dockerCall30(arg):
    dockerCall('bash -c "export LLVM_VERSION=llvm-3.0 && export LD_LIBRARY_PATH=/root/llvm-3.0/lib && export CPATH=/root/llvm-3.0/include:. && export PATH=/root/llvm-3.0/bin:/root/llvm-3.0/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin && ' + arg + '"')

# Docker call with llvm 3.8 activated
def dockerCall38(arg):
    dockerCall('bash -c "export LLVM_VERSION=llvm-3.8 && export LD_LIBRARY_PATH=/root/llvm-3.8/lib && export CPATH=/root/llvm-3.8/include:. && export PATH=/root/llvm-3.8/bin:/root/llvm-3.8/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin && ' + arg + '"')
