# CyCif O2 Cluster Manager

*Purpose: Provide platform infrastructure to streamline CyCif Analysis
Stitching -> Probability Maps -> Segmentation -> Feature Extraction 
*Organization:  Matlab scripts or conda environments

## Advertising Pros

- Anyone at LSP can run it by themselves
	- one location, ease of use
	- user supplies .yaml file with parameters requested for analysis
	- data is required to be on scratch disk (we will write to automatically pull/push from ImStor)
- Current Method Implementation:
	- Ashlar (Jeremy), Unet & Segmenter (Clarence), Feature Extraction (HistoCat-Denise) 
- any new analysis method can be added as a module for CyCif analysis
	- modules can be packaged using a conda environment 
- program keeps track of usage statistics 
- ability to scale (pipeline manager organizes at both method and image)
	- possible limitation is user job submission limit 
- merges every component of cycif pipeline to be runnable and scalable on O2
	- when switch happens to cloud computing or external use as a package framework is still useable with minor modifications

## Whats Next?

- depending on future usage, we may need our own personal GPU node on O2
- adding other methods  
- push stiched images to Omero?

## Whats Next Next?

- GUI/webpage interface for non-command line users to provide information
- backend: submit the information to program to run on O2
- possibly update to singularity/docker containers for methods
