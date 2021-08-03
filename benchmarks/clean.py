import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '../scripts'))
from helper import call

folders = ['bisection_root', 'DFT16', 'DFT16dd', 'dot', 'funarc', 'linear', 'matmul', 'newton_root', 'simpsons']

for folder in folders:
    call('cd examples/' + folder + ' && find . -name "non*" -exec rm -rf {} \;')
