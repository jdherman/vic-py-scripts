#!/bin/bash

FILENUMS=$(seq 0 199)
MAX_SIMULT=7 # max number of simultaneous jobs

for FILENUM in ${FILENUMS}
do
  NAME=hcube_${FILENUM}_9p_50
  echo "Submitting: ${NAME}"
  JOBCOUNT=$(($FILENUM % $MAX_SIMULT))

  if [ $JOBCOUNT -eq 0]
  then
    DEPEND=`qsub -N ${NAME} -v NUM=${FILENUM} Run_Hcube.sh`
  else
    qsub -N ${NAME} -W depend=afterok:${DEPEND} -v NUM=${FILENUM} Run_Hcube.sh
  fi
  
  sleep 0.5

done
