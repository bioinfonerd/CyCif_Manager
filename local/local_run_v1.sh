#Author: Nathan T. Johnson
#Email: johnsonnathant@gmail.com, nathan_johnson@hms.harvard.edu
#Purpose: Provide script that will automate running through entire CyCif Pipeline
#Use:
#


#!/usr/bin/env bash

#read in base folder
folder = ${1}
echo "${folder}"

folder_name = ${basename ${folder}}
echo "${folder_name}"

#copy data locally
echo "rsync -aRP ${folder} $HOME"

# run folder check
echo "python ../bin/check_folder_v1.py $HOME/${folder_name}"

#process illumination
echo "conda activate ImageJ"
for i in `ls -d $HOME/${folder_name}`;
  do echo "python ../bin/illumination_v1.py $HOME/${folder_name}/${i}";
done
echo "conda deactivate"

#run ashlar
echo "conda activate ashlar"
for i in `ls -d $HOME/${folder_name}`;
  do echo "python run_ashlar_command_line_v1.py $HOME/${folder_name}/${i}";
done
echo "conda deactivate"

#run unet
echo "conda activate unet"
for i in `ls -d $HOME/${folder_name}`;
echo "python run_batchUNet2DtCycif_ajit.py $HOME/${folder_name}/${i}";
done
echo "conda deactivate"

#run segmenter
for i in `ls -d $HOME/${folder_name}`;
  do echo "matlab -nodesktop -r "addpath(genpath('../local/segmenter/'));O2batchS3segmenterWrapper( 1 ,1,'/n/groups/lsp/cycif/example_data','TissueMaskChan',[2],'logSigma',[3 30],'mask','tissue','segmentCytoplasm','ignoreCytoplasm')"";
done

#run feature extractor
for i in `ls -d $HOME/${folder_name}`;
  do echo "matlab -nodesktop -r "addpath(genpath('../local/histoCAT/'));Headless_histoCAT_loading( '/n/groups/lsp/cycif/example_data/image_1/registration','image_1.ome.tif','/n/groups/lsp/cycif/example_data/image_1/segmentation/image_1','cellMask.tif','/n/groups/lsp/cycif/example_data/markers.csv','5')""
done

#copy data back to ImStor
echo "rsync -aRP $HOME/${folder_name} ${folder}"
