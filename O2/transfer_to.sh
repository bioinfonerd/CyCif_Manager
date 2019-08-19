#!/bin/bash
#SBATCH  -p transfer
#SBATCH  -t 0-2:00
#SBATCH  -J copy
#SBATCH  -o copy.o
#SBATCH  -e copy.e
rsync -arP /n/scratch2/${USER}example_data ../example_data/
