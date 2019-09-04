---
title: "Image Processing Pipeline"
author: |
  | Laboratory of Systems Pharmacology
date: "Last Updated: `r Sys.Date()`"
site: bookdown::bookdown_site
output: bookdown::gitbook
github-repo: labsyspharm/mcmicro
---

# Quick Start {-}

One-time installation command:
``` {bash, eval=FALSE}
bash /n/groups/lsp/cycif/CyCif_Manager/O2_install.sh
```

Run this once per dataset:
``` {bash, eval=FALSE}
sbatch --wait transfer.sbatch /n/data/ImStor/sorger/... /n/scratch2/abc123/PROJECT
cd /n/scratch2/abc123/PROJECT
cycif_pipeline_activate.sh /n/scratch2/abc123/PROJECT
bash Run_CyCif_pipeline.sh
```

For more detailed instructions, see the chapter on [end-to-end pipeline
execution](#pipeline).

# Individual module documentation {-}

1. [Stitch and register your images](#stitch)
1. [Segment your images to locate individual cells](#segment)
1. [Extract spatial single cell features](#features)
1. [Assign cell type identities](#celltype)

The instructions are under development as the LSP image processing pipeline
matures. If you have a module that you would like to see included, please view
the vignette on [how to contribute](#howto) to this guide.

