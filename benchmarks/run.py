#!/usr/bin/python

import run_fixed_precision_benchmarks
import run_mixed_precision_benchmarks
import create_plots
import create_table_data

# This script is to (re)produce the data from/for the master thesis
# This might take several days

# Run fixed-precision settings
run_fixed_precision_benchmarks.run()

# Run mixed-precision settings
run_mixed_precision_benchmarks.run()

# Create plots
create_plots.run()

# Create table
create_table_data.run()
