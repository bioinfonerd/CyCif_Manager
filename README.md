# CyCif Manager

Purpose: Provide pipeline platform infrastructure to streamline CyCif Analysis both on a local machine and on the O2 cluster at HMS

## Assumptions

- Can be run either locally or on O2
- user must have O2 account & 'access to transfer node?'
- data is stored on ImStor under a project name
	- each folder under the project folder will be for one ROI 
	- under each ROI's folder, a separate folder labeled 'raw files' will contain all .rcpnl and .metadata

### Folder Organization Example 

Project folder is at this location

```{bash, eval==FALSE}
(base) bionerd@MTS-LSP-L06275:~/Dana_Farber/CyCif/git/CyCif_O2_Manager/example_data$ pwd
/home/bionerd/Dana_Farber/CyCif/git/CyCif_O2_Manager/example_data
```

Within 'example_data' are ROI folders

```{bash, eval==FALSE}
(base) bionerd@MTS-LSP-L06275:~/Dana_Farber/CyCif/git/CyCif_O2_Manager/example_data$ ll
drwxrwxrwx 1 bionerd bionerd 4096 Aug  9 08:03 image_1/
drwxrwxrwx 1 bionerd bionerd 4096 Aug  9 08:04 image_2/
```
- each folder should contain a subfolder: raw_files
	- where for each CyCif cycle there should be a .rcpnl and .metadata 
```{bash,eval==FALSE}
(base) bionerd@MTS-LSP-L06275:~/Dana_Farber/CyCif/git/CyCif_O2_Manager/example_data$ ll image_1/
total 0
drwxrwxrwx 1 bionerd bionerd 4096 Aug  9 10:44 ./
drwxrwxrwx 1 bionerd bionerd 4096 Aug  7 12:19 ../
drwxrwxrwx 1 bionerd bionerd 4096 Aug  9 08:04 raw_files/
```
After the CyCif Pipeline is run there will be additional folders made (explained later), for each ROI

## Workflow
Stitching -> Probability Maps -> Segmentation -> Feature Extraction
Ashlar -> Unet -> Clarence Matlab Code -> HistoCat

## Local Install & Run

!Assumption: Matlab Installed, Linux Environment (can use linux subsystem for windows)

git lfs 
``` {bash, eval==FALSE}
git clone git@github.com:bioinfonerd/CyCif_O2_Manager.git
```

python CyCif_Pipeline_v#.py [path to folder base on ImStor]
- assumption is each folder within this folder is a single sample to be processed



### O2 Install & run

git clone git@github.com:bioinfonerd/CyCif_O2_Manager.git

Python program: CyCif_Pipeline_v#.py [path to folder base on ImStor]

## Advertising Pros

- Anyone familiar with command line can run:
	- transferable
	- automatic
	- straightforward to run
	- one location, ease of use
	- user supplies location for data
- any new analysis methods can be added/switched as a module for CyCif analysis
- ability to scale (pipeline manager organizes at both method and image)
- merges every component of cycif pipeline to be runnable and scalable on O2
- With minor modification can switch to AWS (or any cloud computing) 

## Whats Next? (By Priority)

- add analysis parameters
- manage moving image data from ImStor and Scratch
- move to nextflow pipeline management system
- improve useability 
- benchmark scalibility
- add QC metrics/prompting for user 
- track usage
- test for scalability limitations
- GUI/webpage interface for non-command line users to provide information
- update to singularity/docker containers for methods transferability

### How Does it Work

1) Download Data
	- If on O2, will copy data defined by all folders to scratch for processing (can be long process)
2) Check Folder Structure and correct if needed
	- /bin/check_folder_v1.py
3) Run Illumination 
	- /bin/illumination_v1.py
4) Run Ashlar
	- /bin/run_ashlar_command_line_v1.py
5) Run Probability Mapper (Unet)
6) Run Segmenter (Clarence)
7) Run Feature Extractor (Histocat) 
8) Copy results to ImStor (If on O2)


