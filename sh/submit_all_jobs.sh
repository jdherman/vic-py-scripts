#!/bin/bash

FILENUMS=$(seq 0 199)

for FILENUM in ${FILENUMS}
do
  NAME=hcube_${FILENUM}_9p_50
  echo "Submitting: ${NAME}"

  qsub -N ${NAME} -v NUM=${FILENUM} Run_Hcube.sh
  
  sleep 0.5

done
