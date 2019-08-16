#!/bin/bash
#SBATCH  -p short
#SBATCH  -t 0-2:00
#SBATCH  --mem=64G
#SBATCH  -J ashlar
#SBATCH  -o ashlar.o
#SBATCH  -e ashlar.e
module load conda2/4.2.13
source activate  /n/groups/lsp/cycif/ashlar
python /n/groups/lsp/cycif/ashlar/lib/run_ashlar_csv_batch_v1.7.0.py ashlar_dirs.csv
conda deactivate
