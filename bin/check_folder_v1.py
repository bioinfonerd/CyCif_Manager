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
sys.argv[1]='./example_data'

#base folder system
samples = os.listdir(sys.argv[1])

# Create/check the desired folder structure for future pipeline steps
folders_to_make = ['dearray/masks','prob_maps','segmentation','feature_extraction',
                   'clustering/consensus', 'clustering/drclust', 'clustering/pamsig','cell_states']
for d in samples:
    for f in folders_to_make:
        try:
            os.makedirs(str(sys.argv[1])+'/'+d+'/'+f)
        except:
            print('Folder '+f+' already exists for '+d)