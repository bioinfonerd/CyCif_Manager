# Image Stitching and Registration {#stitch}

<script src="./libs/ext/highlight.pack.js"></script>
<script>hljs.initHighlightingOnLoad();</script>

Raw CyCIF images must be stitched together and aligned across cycles before
further processing. The tool we use to do this is
[Ashlar](https://github.com/labsyspharm/ashlar).

## Input

  * Image files for one or more cycles, in a
    [BioFormats](https://www.openmicroscopy.org/bio-formats/) compatible format
    where metadata for pixel physical size and image stage positions are
    available. The RareCyte, InCell 6000, and DeltaVision microscopes are fully
    supported, and IXM support is currently in progress.
    * RareCyte: Each cycle is fully contained in one `.rcnpl` file.
    * InCell 6000: Each cycle is stored as many `.tif` files and one `.xdce`
      file. Use the `.xdce` file as the input for Ashlar.
    * DeltaVision: Each cycle is fully contained in one `.dv` file.
  * Shading correction profiles for all channels in each cycle. These profiles
    can be computed using the
    [BaSiC](https://www.helmholtz-muenchen.de/icb/research/groups/quantitative-single-cell-dynamics/software/basic/index.html)
    plugin for ImageJ. Eventually this functionality will be built into Ashlar,
    but for now use this ImageJ Python macro:
    [imagej_basic_ashlar.py](https://gist.githubusercontent.com/jmuhlich/96417108a2cf7d95ba9258a96904ba5a/raw/5bd41fc651ab6cfcfce872374f23161f4223920b/imagej_basic_ashlar.py)
    (see instructions in comments at the beginning of the script). The macro
    will take one CyCIF cycle and generate two `.tif` files, the multi-channel
    flat-field and dark-field profiles. You will need to run the macro on each
    cycle separately.

## Output

  * A single many-channel `.ome.tif` image covering the entire sample across all
    cycles. This image file can be used for further processing in this pipeline
    or imported into OMERO for visualization and sharing.

## Installation

  * For most users, the Docker container is the simplest option: `docker pull
    labsyspharm/ashlar:latest`
  * Experienced Python users can install natively: `pip install ashlar`

## Usage

### Docker container

If you are using Ashlar via the Docker container, you must first launch the
container with the interactive (`-i`) and TTY (`-t`) options, as well as a
volume (`-v`) argument that maps the directory containing your data to the
`/data` directory inside the container. Here is an example command line,
assuming your images live in `/Volumes/ImStor/images`:

```{bash, eval=FALSE}
docker run labsyspharm/ashlar:latest -i -t -v /Volumes/ImStor/images:/data
```

At this point you will be at a Bash prompt inside the container, with `/data` as
your working directory. Continue with the [instructions for native Python
users](#instructions-python) below.

### Native Python {#instructions-python}

Below is the general format of the command line you should start with, filling
in all of the arguments like filenames and channel numbers to match your own
data. Ashlar has many command line options, but in the context of this pipeline
only a limited subset are relevant. Other options may be helpful to correct
certain stitching problems, but they will not be covered here. Note that in this
command, `...` just means "more of the same" and should not be typed literally.

```{bash, eval=FALSE}
ashlar \
  cycle-1.ext cycle-2.ext ...   \ # List of image files, one per cycle (.rcpnl, .xdce, etc.)
  --ffp ffp-1.tif ffp-2.tif ... \ # List of flat-field profile images, one per cycle
  --dfp dfp-1.tif dfp-2.tif ... \ # List of dark-field profile images, one per cycle
  -c dna_channel                \ # 0-based index of channel with DNA stain (often 0)
  -o output_directory           \ # Output image destination location
  -f sample_name.ome.tif        \ # Filename for output image
  --pyramid                     \ # Required to produce OME-TIFF output
```

To manage this long command line it may be helpful to copy the above sample
command into a Bash script file, edit the file to suit your data, and run the
script with `bash script.sh`. However in the example below we will type the
command directly.

## Example

```{bash, eval=FALSE}
$ ashlar \
>   input/BP40/cycle1.rcpnl input/BP40/cycle2.rcpnl \
>   --ffp shading/BP40-cycle1-ffp.tif shading/BP40-cycle2-ffp.tif \
>   --dfp shading/BP40-cycle1-dfp.tif shading/BP40-cycle2-dfp.tif \
>   -c 0 \
>   -o output \
>   -f BP40.ome.tif \
>   --pyramid
Cycle 0:
    reading input/BP40/cycle-1.rcpnl
    quantifying alignment error 1000/1000
    aligning edge 38/38
    Channel 0:
        merging tile 24/24
        writing to output/BP40.ome.tif
    Channel 1:
        merging tile 24/24
        writing to output/BP40.ome.tif
    Channel 2:
        merging tile 24/24
        writing to output/BP40.ome.tif
    Channel 3:
        merging tile 24/24
        writing to output/BP40.ome.tif
Cycle 1:
    reading input/BP40/cycle-2.rcpnl
    aligning tile 24/24
    Channel 0:
        merging tile 24/24
        writing to output/BP40.ome.tif
    Channel 1:
        merging tile 24/24
        writing to output/BP40.ome.tif
    Channel 2:
        merging tile 24/24
        writing to output/BP40.ome.tif
    Channel 3:
        merging tile 24/24
        writing to output/BP40.ome.tif
Building pyramid
    Level 1:
        processing channel 8/8
    Level 2:
        processing channel 8/8
    Level 3:
        processing channel 8/8
```

## More details

https://github.com/labsyspharm/ashlar

## References

(In progress)
