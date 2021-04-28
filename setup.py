#!/usr/bin/env python

import subprocess

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
	call_30(r"cd DFT16 && clang -c -emit-llvm DFT16.c -o DFT16.bc")
	call_30(r"cd DFT16 && ../HiFPTuner/scripts/compile.sh DFT16.bc")
	call_38(r"cd DFT16 && ../HiFPTuner/scripts/analyze.sh json_DFT16.bc")



if __name__ == "__main__":
	main()
