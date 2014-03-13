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

aprun -n 200 /u/sciteam/jdh33/projects/runp 'python /u/sciteam/jdh33/scratch/vic_hypercube_output_10K/get_error_values_from_raw.py'

aprun -n 15836 /u/sciteam/jdh33/projects/runp 'python /u/sciteam/jdh33/scratch/vic_hypercube_output_10K/pull_good_param_sets.py'

aprun -n 15836 /u/sciteam/jdh33/projects/runp 'python /u/sciteam/jdh33/scratch/vic_hypercube_output_10K/convert_param_sets_max_100.py'

