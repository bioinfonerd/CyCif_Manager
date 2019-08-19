#!/bin/bash
#SBATCH  -p short
#SBATCH  -t 0-1:00
#SBATCH  -J QC
#SBATCH  -o QC.o
#SBATCH  -e QC.e
module load conda2/4.2.13
source activate  ../environments/cycif_pipeline
python 
conda deactivate
