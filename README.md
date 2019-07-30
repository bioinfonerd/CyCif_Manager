# CyCIF Manager

Purpose: Provide pipeline platform infrastructure to streamline CyCIF Analysis both on a local machine and on the O2 cluster at HMS

# Pipeline Workflow
![CyCIF Pipeline Plan](/images/CyCif_Pipeline_Plan.png)


# Quick Start: How to Run the CyCIF Pipeline

## On O2

### New User Installation

Step 1: O2 needs to know where to find the pipeline

``` {bash, eval == FALSE}
bash O2_install.sh
```

Did it work?

```{bash, eval == FALSE}
which cycif_pipeline_activate.sh
```

Step 2: Transfer the example data to your scratch space

sbatch transfer.sbatch **[from]** **[to]**

``` {bash, eval == FALSE}
sbatch transfer.sbatch /n/files/ImStor/sorger/data/RareCyte/nathantjohnson/Data/example_data_raw/ /n/scratch2/ntj8/example_data
```

Step 3: Change directories to where the example data is

change *"ntj8"* to your username

```{bash, eval == FALSE}
cd /n/scratch2/ntj8/example_data
```
Step 4: Activate CyCif Pipeline

change *"/n/scratch2/ntj8/example_data"* to your data path

```{bash, eval == FALSE}
cycif_pipeline_activate.sh /n/scratch2/ntj8/example_data
```
Step 5: Run CyCif Pipeline

```{bash, eval == FALSE}
bash Run_CyCif_pipeline.sh
```  
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
        - Provides the location for the nuclei and a cell within an image

# Visualize Images on Omero 

Step 1: Transfer data to ImStor

Step 2: Transfer data to Omero

# Using your own Data?

https://github.com/bioinfonerd/CyCif_Manager/documentation/own_data.md

# Developer?

Wish to add your own module? Updated your code? Talk to Nathan
 
https://github.com/bioinfonerd/CyCif_Manager/documentation/developers.md 

# FAQ?

https://github.com/bioinfonerd/CyCif_Manager/documentation/FAQ.md
```
