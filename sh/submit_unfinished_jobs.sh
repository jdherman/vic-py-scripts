#!/bin/bash

for FILENUM in `cat did_not_finish.txt` 
do
  NAME=hcube_${FILENUM}_9p_50
  echo "Submitting: ${NAME}"

  qsub -N ${NAME} -v NUM=${FILENUM} Run_Hcube.sh
  
  sleep 0.5

done
