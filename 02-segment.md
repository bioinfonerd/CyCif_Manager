# Image Segmentation {#segment}

Segmentation consists of two distinct steps:

1. [Pre-processing of images](#preprocess) to generate probability maps for background, nuclei contours and nuclei centers.
2. [Binarizing the resulting probability maps](#binarize) to identify pixel regions corresponding to individual cells.

## Image Preprocessing {#preprocess}

The current tool for image preprocessing is UnMicst (UNet Model for Identifying Cells and Segmenting Tissue).

Images can be preprocessed by inferring nuclei contours via a pretrained UNet model. The model is trained on 3 classes : background, nuclei contours and nuclei centers. The resulting probability maps can then be loaded into any modular segmentation pipeline that may use (but not limited to) a marker controlled watershed algorithm. 

The only **input** file is:
an .ome.tif or .tif  (preferably flat field corrected, minimal saturated pixels, and in focus. The model is trained on images acquired at 20x with binning 2x2 or a pixel size of 0.65 microns/px. If your settings differ, you can upsample/downsample to some extent.

**How to install:**
1. Copy the python script, UNet model, and ImageScience toolbox to your computer. Clone from https://github.com/HMS-IDAC/UnMicst.git
2. Pip install tensorflow (or tensorflow_gpu with CUDA drivers and CuDNN libraries), matplotlib, scikit-image, Pillow, tifffile, Image, scipy

**How to run:**<br/>
3. Open the python script batchUNet2DtCycif.py in an editor.<br/>
4. Make the following changes to the code to reflect the locations of your data and supporting files:<br/>
-line 10 update the path to the ImageScience toolbox folder `sys.path.insert(0, 'path//to//UNet code//ImageScience')`<br/>
-line 509 update the path to the model <br/>
`modelPath = 'modelPath = 'path//to//UNet code//TFModel - 3class 16 kernels 5ks 2 layers'`<br/>
-line 515 update the path to the top level experiment folder of the data <br/>
`imagePath = 'path//to//parent//folder//of//data'` <br/>
your files should be stored in a subfolder called `registration` <br/>
-line 516 : if you have multiple samples and they have a similar prefix, add the prefix/suffix here: <br/>`sampleList = glob.glob(imagePath + '//105*')`<br/>
-line 520 : if your files have a different extension from **tif**, you can change the extension here:<br/>
`fileList = glob.glob(iSample + '//registration//*.tif')`<br/>

**some helpful tips:**<br/>
5. -line 517 - specify the channel to infer nuclei contours and centers. If you want to run UNet on the 1st channel (sometimes DAPI/Hoechst), put 0.<br/>
-line 518 - if you acquired your images at a higher magnification (ie. 40x), you may want to downsample your image so that it is more similar to the trained model (ie. 20x binning 2x2, pixel size 0.65 microns).<br/>

6. in your terminal, activate your virtual environment and run this python script:
`python batchUNet2DtCycif.py`

7. If using tensorflow-gpu, your GPU card should be found. If not, prepare to hear your CPU fan fly! 
8. The probabilty map for the contours will be saved as a 3D tif file (concatenated with the original channel) and saved in a subfolder called `probmaps. The channel index you specified for inference is saved in the filename.

**References:** <br/>
S Saka, Y Wang, J Kishi, A Zhu, Y Zeng, W Xie, K Kirli, C Yapp, M Cicconet, BJ Beliveau, SW Lapan, S Yin, M Lin, E Boyde, PS Kaeser, G Pihan, GM Church, P Yin, Highly multiplexed in situ protein imaging with signal amplification by Immuno-SABER, Nat Biotechnology (accepted)

## Probability map binarization {#binarize}

 S3segmenter is a Matlab-based set of functions that generates single cell (nuclei and cytoplasm) label masks. Inputs are:

1. an .ome.tif (preferably flat field corrected)
2. a 3-class probability maps derived from a deep learning model such as UNet. Classes include background, nuclei contours, and nuclei foreground.

The centers of each nuclei are obtained by finding local maxima from the nuclei foreground. These are used for marker-controlled watershed constrained by the nuclei contours.

To segment cytoplasm, the nuclei are in turn used for a marker-controlled watershed segmentation constrained by a cytoplasmic marker such as B-catenin. The channel number of this marker must be specified. A 3-pixel annulus around each nucleus will also be used to segment cytoplasm.

**How to run:** In Matlab, set path to the folder of the cloned repo. Type: `O2batchS3segmenterWrapperR('/path/to/files/')`

Use the following name-value pairs arguments to customize the code to your experiment: 
``` {octave, eval=FALSE}
ip.addParamValue('HPC','false',@(x)(ismember(x,{'true','false'}))); 

% if using a cluster, this specifies which file index to work on 
ip.addParamValue('fileNum',1,@(x)(numel(x) > 0 & all(x > 0 )));

% select any number of channels for cytoplasm
ip.addParamValue('CytoMaskChan',[2],@(x)(numel(x) > 0 & all(x > 0 )));

% select any number of channels for tissue mask
ip.addParamValue('TissueMaskChan',[3],@(x)(numel(x) > 0 & all(x > 0 )));

% constrict the tissue mask to eliminate high autofluorescent regions
ip.addParamValue('RefineTissueMask',[0],@(x)(numel(x) > 0 & all(x > 0 ))); 

% set to true if sample is TMA cores
ip.addParamValue('mask','tissue',@(x)(ismember(x,{'TMA','tissue','none'}))); 

% interactiveCrop - a GUI-based crop selector, 
%   'autoCrop' - takes the middle third region,
%   'dearray', set to true if using TMA cores, 
%   'noCrop', no cropping
ip.addParamValue('crop','noCrop',@(x)(ismember(x,{'interactiveCrop','autoCrop','dearray','noCrop'})));
ip.addParamValue('cytoMethod','distanceTransform',@(x)(ismember(x,{'RF','distanceTransform','bwdistanceTransform','ring'})));

% feature to threshold nuclei. 
%   'IntPM' - intensity of probability map, 
%   'Int' - intensity of DAPI channel, 
%   'LoG', intensity of LoG filter response, 
%   'none', accept all nuclei
ip.addParamValue('nucleiFilter','IntPM',@(x)(ismember(x,{'LoG','Int','IntPM','none'}))); 

% extracts intensity features from mask
ip.addParamValue('measureFeatures','false',@(x)(ismember(x,{'true','false'})));
ip.addParamValue('nucleiRegion','watershedContourInt',@(x)(ismember(x,{'watershedContourDist','watershedContourInt','watershedBWDist','dilation'})));
ip.addParamValue('resizeFactor',1,@(x)(numel(x) == 1 & all(x > 0 )));

% specify range of nuclei diameters in pixels ie [3 30]. 
ip.addParamValue('logSigma',[2.5],@(x)(numel(x) >0 & all(x > 0 ))); 

% channels for measuring features. If 0, assume all channels. 
ip.addParamValue('chanRange',[0],@(x)(numel(x) >0 & all(x > 0 ))); 
ip.addParamValue('upSample',2,@(x)(numel(x) == 1 & all(x > 0 )));
ip.addParamValue('Docker','false',@(x)(ismember(x,{'true','false'}))); 
ip.addParamValue('dockerParams',0,@(x)(numel(x)==1));
```

Segmentation label masks for nuclei, cytoplasm, and cell will be saved to a subfolder under each parent image folder as a .tif file. Also saved are a 2-channel tif file with the DAPI and nuclei outlines for quality control.

**References:**
S Saka, Y Wang, J Kishi, A Zhu, Y Zeng, W Xie, K Kirli, C Yapp, M Cicconet, BJ Beliveau, SW Lapan, S Yin, M Lin, E Boyde, PS Kaeser, G Pihan, GM Church, P Yin, Highly multiplexed in situ protein imaging with signal amplification by Immuno-SABER, Nat Biotechnology (accepted)
