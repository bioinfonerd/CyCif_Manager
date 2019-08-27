# CyCif Manager

Purpose: Provide pipeline platform infrastructure to streamline CyCif Analysis both on a local machine and on the O2 cluster at HMS

## Assumptions

- Can be run either locally or on O2
- user must have O2 account 
	- access to 'transfer_users' and 'ImStor_sorger' groups 
	- to check:
```{bash,eval==FALSE}
groups
```
	- If lack O2 access or groups, request at "https://rc.hms.harvard.edu/" 
- data follows Folder Organization (shown below)
- file 'markers.csv' that lists on each row the name of marker in order imaged 
	- Example:
```{bash,eval==FALSE}
DNA1
AF488
AF555
AF647
DNA2
mLY6C
mCD8A
mCD68
DNA3
CD30
CPARP
CD7
```

# Pipeline Workflow
![CyCif Pipeline Plan](/images/CyCif_Pipeline_Plan.png)


## Folder Organization Example 

Project folder is at a location findable by O2

```{bash, eval==FALSE}
(base) bionerd@MTS-LSP-L06275:~/Dana_Farber/CyCif/git/CyCif_O2_Manager/example_data$ pwd
/home/bionerd/Dana_Farber/CyCif/git/CyCif_O2_Manager/example_data
```

Within your data folder there are separate folders for each imaged slide

- Can be whole tissue slide or TMA (eventually)

```{bash, eval==FALSE}
(base) bionerd@MTS-LSP-L06275:~/Dana_Farber/CyCif/git/CyCif_O2_Manager/example_data$ ll
drwxrwxrwx 1 bionerd bionerd 4096 Aug  9 08:03 image_1/
drwxrwxrwx 1 bionerd bionerd 4096 Aug  9 08:04 image_2/
```
- each folder should contain a subfolder: 'raw_files' with 
	- where for each CyCif cycle there should the raw images from the microscope
	- for example from Rare Cycte: '.rcpnl' and '.metadata '

```{bash,eval==FALSE}
(base) bionerd@MTS-LSP-L06275:~/Dana_Farber/CyCif/git/CyCif_O2_Manager/example_data$ ll image_1/
total 0
drwxrwxrwx 1 bionerd bionerd 4096 Aug  9 10:44 ./
drwxrwxrwx 1 bionerd bionerd 4096 Aug  7 12:19 ../
drwxrwxrwx 1 bionerd bionerd 4096 Aug  9 08:04 raw_files/
[ntj8@login01 image_1]$ cd raw_files/
[ntj8@login01 raw_files]$ ll
total 3326644
-rwxrwx--- 1 ntj8 ntj8      11516 Jul  9 17:30 Scan_20190612_164155_01x4x00154.metadata
-rwxrwx--- 1 ntj8 ntj8 1703221248 Jul  9 17:31 Scan_20190612_164155_01x4x00154.rcpnl
-rwxrwx--- 1 ntj8 ntj8      11524 Jul  9 17:31 Scan_20190613_125815_01x4x00154.metadata
-rwxrwx--- 1 ntj8 ntj8 1703221248 Jul  9 17:32 Scan_20190613_125815_01x4x00154.rcpnl
```
After the CyCif Pipeline is run there will be additional folders made (explained later), for each slide

# Run CyCif Pipeline

## On O2

### New User Installation

Run the following on O2 to modify your .bash_profile in order for commands to be found by path

``` {bash,eval==FALSE}
echo 'CYCIF=/n/groups/lsp/cycif/CyCif_Manager/O2:/n/groups/lsp/cycif/CyCif_Manager/bin' >> ~/.bash_profile

echo 'export PATH=$CYCIF:$PATH' >> ~/.bash_profile

source ~/.bash_profile
```
Test CyCif Pipeline Is Found. If works, should give the path to it.  If not, will be blank

```
which cycif_pipeline_activate.sh
```
### Run CyCif Pipeline on O2

Three stages:
	
- Transfer data
- Activate CyCif Pipeline: Makes all of the files unique to your dataset to submit jobs to O2
- Run CyCif Pipeline: Submits all modules to run on O2 job scheduler

*Currently, large datasets overwhelm O2 que capacity.  Next version will fix

Transfer Data to scratch disk.  Example:
	
- transfer.sbatch [from] [to]        
- Change 'ntj8' to your O2 username
- Must use previously defined folder organization  

``` {bash, eval == FALSE}

sbatch transfer.sbatch /n/files/ImStor/sorger/data/RareCyte/nathantjohnson/Data/example_data/ /home/ntj8/scratch
```
Go To Your Working Directory

- Suggestion, change location to within your dataset so all of the working and log files are within your dataset
- Change '/n/scratch2/ntj8/example_data' to your data's path

```
cd /n/scratch2/ntj8/example_data
cycif_pipeline_activate.sh /n/scratch2/ntj8/example_data
Run_CyCif_pipeline.sh
```
*If part of the pipeline has already been run, it will not re-run or overwrite the previous files


## Run On Local Machines (request analysis time: https://ppms.us/hms-lsp/login/)



# Results

Upon completion of the pipeline there will be the following folders within your project directory containing the processed information from each part of the pipeline.  The folders are: 

- cell_states  
	- Placeholder for future analysis 
- clustering  
	- Placeholder for future analysis
- dearray  
	- Contains masks
- feature_extraction  
	- The counts matrix of marker expression at a single cell level for all images (Output of HistoCAT software)
- illumination_profiles  
	- Preprocessing files required for stitching the acquired raw tiles into a single image (Ashlar)
- prob_maps
	- Probability maps predicted by the UMAP deep learning algorithm for identifying nucleus, cell borders and background
- raw_files  
	- Your original folder containing the raw images 
- registration
	- Image that has been stitched and aligned over multiple cycles (needs to be uploaded to Omero for viewing or can be viewed using Image J)  
- segmentation
	- Output for S3 

# Advertising Pros

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

# For Developers

Updated your code? Wish to add your method to pipeline? Contact Nathan 


### Local Install & Run

Assumption: Matlab Installed, Linux Environment (can use linux subsystem for windows)

``` {bash, eval==FALSE}

git clone git@github.com:bioinfonerd/CyCif_O2_Manager.git

```

Install conda environments and example data

Run within github directory
```{bash,eval==FALSE}
install.sh
install_example_dataset.sh
```


