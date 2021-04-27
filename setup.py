#!/usr/bin/env python

import subprocess

def call(arg):
	subprocess.call([arg], shell=True) #remove shell...

def call_30(arg):
	command = r"docker exec -ti hi bash -c 'export LLVM_VERSION=3.0 " +\
	r"&& export CPATH=/root/llvm-3.0/include:.  && export PATH=/root/llvm" +\
	r"-3.0/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/sbin:/bin && export "+\
	r"LD_LIBRARY_PATH=/bla && llvm-config --version &&"
	subprocess.call([command + arg + "'"], shell=True) #remove shell...

def call_38(arg):
	command = r"docker exec -ti hi bash -c 'export LLVM_VERSION=3.8 " +\
	r"&& export CPATH=/root/llvm-3.8/include:. && export PATH=/root/llvm" +\
	r"-3.8/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/sbin:/bin && export "+\
	r"LD_LIBRARY_PATH=/root/llvm-3.8/lib && llvm-config --version &&"
	subprocess.call([command + arg + "'"], shell=True) #remove shell...], shell=True) #remove shell...


def main():
	call_30(r"cd DFT16 && clang --version && clang -emit-llvm DFT16.c -o DFT6.bc")




if __name__ == "__main__":
	main()
