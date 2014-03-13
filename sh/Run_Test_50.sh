#!/bin/bash
### set the number of nodes
### set the number of PEs per node
### set the XE feature
#PBS -l nodes=512:ppn=32:xe
### set the wallclock time
#PBS -l walltime=4:00:00
## set email notification
#PBS -m bea
#PBS -M jdh366@cornell.edu

# Note: using file_20 because we haven't used it yet. 

aprun -n 15836 /u/sciteam/jdh33/code/VIC/vicNl /u/sciteam/nchaney/projects/PSU_AERO_PU/GLOBAL_PARAMETER.txt 50 0

