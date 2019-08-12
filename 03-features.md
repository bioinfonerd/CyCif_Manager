# Extract spatial single cell features {#features}

Once the image is [segmented](#segment) label masks for nuclei, cytoplasm and full cell outline can be used to extract spatial single cell features.

**Expected input:**

  * `.tif` (16/32 bit) label mask for nuclei, cytoplasm or full cell outline (only one mask can be used per run)
  * `.ome.tif` [stitched](#stitch) image
  * `.csv` including all channels corresponding to the `ome.tif`

  **Expected output:**

  * `.csv` including all quantified spatial single cell features

**How to install:**

  * Clone histoCAT headless version from `https://github.com/DenisSch/histoCAT`
    * Command line: `git clone https://github.com/DenisSch/histoCAT`

**How to run:**

``` {octave, eval=FALSE}
% Run locally or remotly
Headless_histoCAT_loading...
(samplefolders_str,... % Path to OME.TIF image
tiff_name,... % OME.TIF image name		
segmentationfolder_str,... % Path to .TIF mask
mask_name,... % .TIF mask name
Marker_CSV,... % .CSV including all channels corresponding to the OME.TIF
expansionpixels,... % How many pixels should be used for extraction of spatial features
neighbors)` % Should neighborhood / neighbors be calculates (e.g. for neighborhood analysis)
```

**Example:**
```{octave, eval=FALSE}
Headless_histoCAT_loading...
    ('headless_Test/',...
    'Example.tif',...
    'headless_Test/',...
    'Mask.tif',...
    'headless_Test/Triplet_40_markers.csv','30','yes')
```

**More details:**

https://github.com/DenisSch/histoCAT

**References:**

https://www.nature.com/articles/nmeth.4391

