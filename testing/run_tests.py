#!/usr/bin/python
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '../scripts'))
from helper import call

print('Test DFT16')
call('python3 scripts/rerun.py examples/DFT16/ DFT16.c DFT16 DFT16')
print('Test DFT16dd')
call('python3 scripts/rerun.py examples/DFT16dd/ DFT16.c DFT16 DFT16')
print('Test dot')
call('python3 scripts/rerun.py examples/Dot/ dot.c dot dot')
print('Test simpsons')
call('python3 scripts/rerun.py examples/simpsons/ simpsons.c simpsons simpsons')
