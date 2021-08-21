# This script deletes the benchmark data

import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '../scripts'))
from helper import call

folders = ['bisection_root', 'DFT16', 'DFT16dd', 'dot', 'funarc', 'linear', 'matmul', 'newton_root', 'simpsons']

print("WARNING: This deletes all benchmark results! Type 'yes' to continue.")
input = input()
if input != 'yes':
    sys.exit(-1)

for folder in folders:
    call('cd examples/' + folder + ' && find . -name "analysis*" -prune -exec rm -rf {} \;')
    call('cd examples/' + folder + ' && find . -name "config*" -prune -exec rm -rf {} \;')
    call('cd examples/' + folder + ' && find . -name "non_mixed*" -prune -exec rm -rf {} \;')
