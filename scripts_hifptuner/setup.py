#!/usr/bin/env python

import subprocess
import sys

def call(arg):
	subprocess.call([arg], shell=True) #remove shell...

def call_30(arg):
	command = r"docker exec -ti hi bash -c 'export LLVM_VERSION=llvm-3.0 " +\
	r"&& export CPATH=/root/llvm-3.0/include:.  && export PATH=/root/llvm" +\
	r"-3.0/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin && export "+\
	r"LD_LIBRARY_PATH=/root/HiFPTuner/precimonious/logging:/root/llvm-3.0/lib: &&"
	subprocess.call([command + arg + "'"], shell=True) #remove shell...

def call_38(arg):
		command = r"docker exec -ti hi bash -c 'export LLVM_VERSION=llvm-3.8 " +\
		r"&& export CPATH=/root/llvm-3.8/include:.  && export PATH=/root/llvm" +\
		r"-3.8/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin && export "+\
		r"LD_LIBRARY_PATH=/root/HiFPTuner/precimonious/logging:/root/llvm-3.8/lib: &&"
		subprocess.call([command + arg + "'"], shell=True) #remove shell...

def main():
	if len(sys.argv) != 2:
		print("Argument missing or to many.")
		exit(-1)
	filename = sys.argv[1]
	print(filename)

	call_30(r"cd " + filename + r" && clang -c -emit-llvm " + filename + r".c -o " + filename + r".bc")
	call_30(r"cd " + filename + r" && ../HiFPTuner/scripts/compile.sh " + filename + r".bc")
	call_38(r"cd " + filename + r" && ../HiFPTuner/scripts/analyze.sh json_" + filename + r".bc")



if __name__ == "__main__":
	main()
