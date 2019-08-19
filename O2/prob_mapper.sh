#!/bin/bash
#SBATCH  -p gpu
#SBATCH  -n 1
#SBATCH  -c 12
#SBATCH  --gres=gpu:1
#SBATCH  -t 0-1:00
#SBATCH  --mem=64000
#SBATCH  -e probability_mapper.e
#SBATCH  -o probability_mapper.o
#SBATCH  -J prob_mapper
module load gcc/6.2.0
module load cuda/9.0
module load conda2/4.2.13
source activate  ../environments/unet
python run_batchUNet2DtCycif_V1.py ../example_data 0 0 1
conda deactivate
