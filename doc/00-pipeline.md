# End-to-end pipeline execution {#pipeline}

Here we will walk you through running the default end-to-end processing pipeline
comprising [stitching and registration](#stitch), [segmentation](#segment), and
[single-cell feature extration](#features).

## Installation

Run the following command to install the pipeline execution tools:
``` {bash, eval=FALSE}
bash /n/groups/lsp/cycif/CyCif_Manager/O2_install.sh
```

Run this command to check for success:
```{bash, eval=FALSE}
which cycif_pipeline_activate.sh
```
* If you see `/n/groups/lsp/cycif/CyCif_Manager/bin/cycif_pipeline_activate.sh`, the
  installation succeeded.
* If you see `no cycif_pipeline_activate.sh in ...` then the installation
  failed.

## Usage

The commands below use the username `abc123`, so in the typed commands you must
substitute your own username (or the username of whomever you’re working on
behalf of).

### Data transfer

First you will need to transfer your data to the scratch2 volume:

```{bash, eval=FALSE}
sbatch transfer.sbatch FROM /n/scratch2/abc123/PROJECT
```

Replace `FROM` with the path to your data, and `PROJECT` with a short name for
this project or experiment. We will refer to `/n/scratch2/abc123/PROJECT` as the
"working directory".

### Go to the working directory

```{bash, eval=FALSE}
cd /n/scratch2/abc123/PROJECT
```

### Generate the pipeline execution script

```{bash, eval=FALSE}
cycif_pipeline_activate.sh /n/scratch2/abc123/PROJECT
```

### Launch the pipeline

```{bash, eval=FALSE}
bash Run_CyCif_pipeline.sh
```

## Worked example using a sample dataset

```{bash, eval=FALSE}
sbatch --wait transfer.sbatch /n/groups/lsp/cycif/CyCif_Manager/example_data/ /n/scratch2/abc123/example_data
cd /n/scratch2/abc123/example_data
cycif_pipeline_activate.sh /n/scratch2/abc123/example_data
bash Run_CyCif_pipeline.sh
```

Note that we have added the `--wait` option to the `sbatch` command which will
pause until the data has finished transferring before continuing with the
remaining steps. This is only practical if the dataset is small (less than about
50 GB). If your data is larger, see the Tips and Tricks section below.

## Results

Upon completion of the pipeline, the following folders will appear within your
project directory containing the processed information from each part of the
pipeline. The folders are:

* `cell_states`: Placeholder for future analysis
* `clustering`: Placeholder for future analysis
* `dearray`: Contains masks
* `feature_extraction`: The counts matrix of marker expression at a single cell
  level for all images (Output of HistoCAT software)
* `illumination_profiles`: Preprocessing files required for stitching the
  acquired raw tiles into a single image (Ashlar)
* `prob_maps`: Probability maps predicted by the UMAP deep learning algorithm
  for identifying nucleus, cell borders and background
* `raw_files`: Your original folder containing the raw images
* `registration`: Image that has been stitched and aligned over multiple cycles
  (needs to be uploaded to Omero for viewing or can be viewed using Image J)
* `segmentation`: Provides the location for the nuclei and a cell within an
  image

## Visualize Images on Omero

1. Transfer data to ImStor
1. Import data to Omero

## Tips and Tricks

### Processing your own data

#### Folder Organization Example
Project folder must be at a location findable by O2.

```{bash, eval=FALSE}
(base) bionerd@MTS-LSP-L06275:~/Dana_Farber/CyCif/git/CyCif_O2_Manager/example_data$ pwd
/home/bionerd/Dana_Farber/CyCif/git/CyCif_O2_Manager/example_data
```

Within your data folder there are separate folders for each imaged slide.
Can be whole tissue slide or TMA (eventually).

```{bash, eval=FALSE}
(base) bionerd@MTS-LSP-L06275:~/Dana_Farber/CyCif/git/CyCif_O2_Manager/example_data$ ll
drwxrwxrwx 1 bionerd bionerd 4096 Aug  9 08:03 image_1/
drwxrwxrwx 1 bionerd bionerd 4096 Aug  9 08:04 image_2/
```

Each folder should contain a subfolder: 'raw_files' with
where for each CyCIF cycle there should the raw images from the microscope
for example from Rare Cycte: '.rcpnl' and '.metadata '

```{bash, eval=FALSE}
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

After the CyCIF Pipeline is run there will be additional folders created for
each slide (explained in [Results]).

#### Requirements
* Can be run either locally or on O2.
* For O2, user must have an O2 account and be a member of the `transfer_users`
  and `ImStor_sorger` groups. Run `groups` on O2 to check.
  * Request O2 account and group access at https://rc.hms.harvard.edu/.
* Data follows Folder Organization (shown above).
* File 'markers.csv' containing one marker per row, in the order imaged. Example:
```{bash, eval=FALSE}
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

## Frequently Asked Questions

### Help my O2 environment changed!
O2 loads in `.bash_profile` then `.bashrc` by default unless `.bash_profile`
does not exist. If your O2 environment has changed, it is likely that the
installation instructions created `.bash_profile`. Solution is to replace the
installation instructions from `.bash_profile` to `.bashrc`

## Instructions for pipeline module developers

Updated your code? Wish to add your method to pipeline? Contact Nathan.

### Install & Run
Assumption: Matlab Installed, Linux Environment (can use linux subsystem for
windows)

```
git clone git@github.com:bioinfonerd/CyCif_O2_Manager.git
```

Install conda environments and example data by running within github directory

```
install.sh
install_example_dataset.sh
```

### Local Install
Talk to Nathan.
