#!/bin/bash

# This submission will submit 200 jobs in "globs", 
# Where one glob will not begin until the previous one finishes without errors

FILENUMS=$(seq 0 199)
MAX_SIMULT=7 # max number of simultaneous jobs
GLOBNUM=0
GLOBNUM_PREV=0
DEPEND=""
DEPEND_PREV=""

for FILENUM in ${FILENUMS}
do
  NAME=hcube_${FILENUM}_9p_50
  echo "Submitting: ${NAME}"
  GLOBNUM=$(($FILENUM / $MAX_SIMULT))

   # the first MAX_SIMULT jobs have no dependency
   # submit the jobs and append to string
  if [ $GLOBNUM -eq 0 ]
  then
    DEPEND=$DEPEND:`qsub -N ${NAME} -v NUM=${FILENUM} Run_Hcube.sh`

  # Else if the counter ticks ahead to the next "glob" ...
  # Grab the existing job dependencies and start building the next string
  elif [ $GLOBNUM -ne $GLOBNUM_PREV ]
  then
    DEPEND_PREV=$DEPEND
    DEPEND=`qsub -N ${NAME} -W depend=afterok${DEPEND_PREV} -v NUM=${FILENUM} Run_Hcube.sh`
    GLOBNUM_PREV=$GLOBNUM

  # If we're in the same glob as the previous iteration, use the same dependency string
  else
    DEPEND=$DEPEND:`qsub -N ${NAME} -W depend=afterok${DEPEND_PREV} -v NUM=${FILENUM} Run_Hcube.sh`
  fi
  
  sleep 0.5
  echo $DEPEND

done
