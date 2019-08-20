#!/bin/bash
#SBATCH  -p transfer
#SBATCH  -t 0-2:00
#SBATCH  -J copy
#SBATCH  -o copy.o
#SBATCH  -e copy.e
rsync -arP $1 $2
