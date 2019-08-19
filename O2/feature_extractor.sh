#!/bin/bash
#SBATCH  -p short
#SBATCH  -t 0-5:00
#SBATCH  -c 8
#SBATCH  --mem=100G
#SBATCH  -J feature_extractor
#SBATCH  -o feature_extractor.o
#SBATCH  -e feature_extractor.e
module load matlab/2018b
python../bin/run_ashlar_csv_batch.py'../example_dataimage_1/registration','image_1.ome.tif','../example_dataimage_1/segmentation/image_1','cellMask.tif','../example_datamarkers.csv','/','n')"
python../bin/run_ashlar_csv_batch.py'../example_dataimage_2/registration','image_2.ome.tif','../example_dataimage_2/segmentation/image_2','cellMask.tif','../example_datamarkers.csv','/','n')"
mv ./output ../example_data
