#Purpose: check and create folder directory system for CyCif Pipeline if not available
#to run: python check_folder.py ['Base folder']
#example:  python check_folder.py ./example_data/

#libraries
from __future__ import print_function
try:
    import pathlib
except ImportError:
    import pathlib2 as pathlib
import os
import sys
#sys.argv[1]='./example_data'

#grab all folders within systems argument
samples = next(os.walk(sys.argv[1]))[1]

# Create/check the desired folder structure for future pipeline steps
folders_to_make = ['dearray/masks','prob_maps','segmentation','feature_extraction',
                   'clustering/consensus', 'clustering/drclust', 'clustering/pamsig','cell_states']
for d in samples:
    for f in folders_to_make:
        print('Making folder structure for sample:',f)
        try:
            os.makedirs(str(sys.argv[1])+'/'+d+'/'+f)
        except:
            print('Folder '+f+' already exists for '+d)