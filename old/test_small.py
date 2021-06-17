#!/usr/bin/python
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '../scripts'))
from helper import call

call('cp src/igen_CMakeLists_no_vec.txt igen_CMakeLists.txt')

print('Test Dot')
call('python3 scripts/rerun.py examples/Dot/ dot.c dot dot 2')
