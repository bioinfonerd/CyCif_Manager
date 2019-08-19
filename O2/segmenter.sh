#!/bin/bash
#SBATCH  -p short
#SBATCH  -t 0-5:00
#SBATCH  -c 1
#SBATCH  --mem=100G
#SBATCH  -J segmenter
#SBATCH  -o segmenter.o
#SBATCH  -e segmenter.e
module load matlab/2018b
matlab -nodesktop -r "addpath(genpath('../environments/segmenter/'));O2batchS3segmenterWrapperR('../example_data','HPC','true','fileNum',1,'TissueMaskChan',[2],'logSigma',[3 30],'mask','tissue','segmentCytoplasm','ignoreCytoplasm')"
matlab -nodesktop -r "addpath(genpath('../environments/segmenter/'));O2batchS3segmenterWrapperR('../example_data','HPC','true','fileNum',1,'TissueMaskChan',[2],'logSigma',[3 30],'mask','tissue','segmentCytoplasm','ignoreCytoplasm')"
