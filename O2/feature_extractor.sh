#!/bin/bash
#SBATCH  -p short
#SBATCH  -t 0-5:00
#SBATCH  -c 8
#SBATCH  --mem=100G
#SBATCH  -J feature_extractor
#SBATCH  -o feature_extractor.o
#SBATCH  -e feature_extractor.e
module load matlab/2018b
matlab -nodesktop -r "addpath(genpath('/n/groups/lsp/cycif/histoCAT/'));Headless_histoCAT_loading('../example_dataimage_1/registration','image_1.ome.tif','../example_dataimage_1/segmentation/image_1','cellMask.tif','../example_datamarkers.csv','5','no')"
matlab -nodesktop -r "addpath(genpath('/n/groups/lsp/cycif/histoCAT/'));Headless_histoCAT_loading('../example_dataimage_2/registration','image_2.ome.tif','../example_dataimage_2/segmentation/image_2','cellMask.tif','../example_datamarkers.csv','5','no')"
mv ./output ../example_data
