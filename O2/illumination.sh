#!/bin/bash
#SBATCH  -p short
#SBATCH  -t 0-2:00
#SBATCH  --mem=64G
#SBATCH  -J ashlar
#SBATCH  -o ashlar.o
#SBATCH  -e ashlar.e
module load conda2/4.2.13
source activate  ../environments/ImageJ
python 
conda deactivate
