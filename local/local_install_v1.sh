#!/bin/bash

#Author: Nathan T. Johnson
#Email: johnsonnathant@gmail.com, nathan_johnson@hms.havard.edu
#Purpose: Download pipeline environments to run on local machine
#Assumption: In main directory where 'local' directory is one level below
#To Run: ./local_install.sh

echo 'Setting Up CyCif Pipeline for Local Machine Run'
echo 'Download ImageJ Environment'
wget --output-document=ImageJ.tar.gz https://www.dropbox.com/s/gw0sf7wc44gtjmi/ImageJ.tar.gz?dl=0
echo 'Downloading Ashlar Environment'
wget --output-document=ashlar.tar.gz https://www.dropbox.com/s/uhm7qrhvq5b6po6/ashlar.tar.gz?dl=0
echo 'Downloading Unet Environment'
wget --output-document=cycif-segment-tf-umap.tar.gz 
echo 'Downloading Segmenter via Clarence'
wget --output-document=segmenter.tar.gz https://www.dropbox.com/s/w9fniau7od8c6iv/segmenter.tar.gz?dl=0
echo 'Downloading Feature Extractor via HistoCat'
wget --output-document=histoCAT.tar.gz https://www.dropbox.com/s/8iawjlcwa9jo14o/histoCAT.tar.gz?dl=0
echo 'Uncompressing ImageJ'
tar -zxf ImageJ.tar.gz
echo 'Uncompressing Ashlar'
tar -zxf ashlar.tar.gz
echo 'Uncompressing Unet'
tar -zxf cycif-segment-tf-umap.tar.gz
echo 'Uncompressing Segmenter'
tar -zxf segmenter.tar.gz
echo 'Uncompressing Feature Extractor'
tar -zxf histoCAT.tar.gz
