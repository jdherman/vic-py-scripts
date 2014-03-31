#!/bin/bash
### set the number of nodes
### set the number of PEs per node
### set the XE feature
#PBS -l nodes=512:ppn=32:xe
### set the wallclock time
#PBS -l walltime=3:00:00
## set email notification
#PBS -m bea
#PBS -M jdh366@cornell.edu

# Get % below error values for simple maps
aprun -n 200 /u/sciteam/jdh33/projects/runp 'python /u/sciteam/jdh33/scratch/vic_hypercube_output_10K/get_error_values_from_raw.py'
# Note: still need to do "combine error value files" after this step

# Pull out parameter sets satisfying error thresholds: 1, 5, 10
aprun -n 15836 /u/sciteam/jdh33/projects/runp 'python /u/sciteam/jdh33/scratch/vic_hypercube_output_10K/pull_good_param_sets.py 1'
aprun -n 15836 /u/sciteam/jdh33/projects/runp 'python /u/sciteam/jdh33/scratch/vic_hypercube_output_10K/pull_good_param_sets.py 5'
aprun -n 15836 /u/sciteam/jdh33/projects/runp 'python /u/sciteam/jdh33/scratch/vic_hypercube_output_10K/pull_good_param_sets.py 10'

# Right now not using this "max 100" -- this is being capped in Nate's script
# aprun -n 15836 /u/sciteam/jdh33/projects/runp 'python /u/sciteam/jdh33/scratch/vic_hypercube_output_10K/convert_param_sets_max_100.py'

# then run Nate's "main.py" file ...
