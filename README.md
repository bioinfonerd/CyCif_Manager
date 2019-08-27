# CyCif Manager

Purpose: Provide pipeline platform infrastructure to streamline CyCif Analysis both on a local machine and on the O2 cluster at HMS

## Assumptions

- Can be run either locally or on O2
- user must have O2 account & access to transfer node
- data is stored on ImStor under a project name
	- each folder under the project folder will be for one imaged slide 
	- under each imaged slide's folder, a separate folder labeled 'raw files' will contain all .rcpnl and .metadata
- data follows Folder Organization Example
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


## Run On Local Machines ()


#Results

- cell_states  
- clustering  
- dearray  
- feature_extraction  
- illumination_profiles  
- prob_maps  
- raw_files  
- registration  
- segmentation

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


