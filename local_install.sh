#!/bin/bash

#Author: Nathan T. Johnson
#Email: johnsonnathant@gmail.com, nathan_johnson@hms.havard.edu
#Purpose: Download pipeline environments to run on local machine
#Assumption: In main directory where 'local' directory is one level below
#To Run: ./local_install.sh

echo 'Setting Up CyCif Pipeline for Local Machine Run'
echo 'Downloading Ashlar Environment'
wget --output-document=ashlar.tar.gz https://www.dropbox.com/s/uhm7qrhvq5b6po6/ashlar.tar.gz?dl=0
echo 'Downloading Unet Environment'
wget --output-document=cycif-segment-tf-umap.tar.gz https://www.dropbox.com/s/dgx46cwykjwsolh/cycif-segment-tf-umap.tar.gz?dl=0
echo 'Downloading Segmenter via Clarence'
wget --output-document=segmenter.tar.gz https://www.dropbox.com/s/c84o10x7n1mdpdx/segmenter.tar.gz?dl=0
echo 'Downloading Feature Extractor via HistoCat'
wget --output-document=histoCAT.tar.gz https://www.dropbox.com/s/lwyrlcc8tej301d/histoCAT.tar.gz?dl=0
echo 'Uncompressing Ashlar'
tar -zxf ashlar.tar.gz -C local
echo 'Uncompressing Unet'
tar -zxf cycif-segment-tf-umap.tar.gz -C local
echo 'Uncompressing Segmenter'
tar -zxf segmenter.tar.gz -C local
echo 'Uncompressing Feature Extractor'
tar -zxf histoCAT.tar.gz -C local
