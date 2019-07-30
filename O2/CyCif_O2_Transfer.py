#libraries
from contextlib import redirect_stdout
import yaml
import os
import sys
import shutil

#handles path to data correctly
master_dir = os.path.normpath(sys.argv[1])
run_type = sys.argv[2]

#
def master():
    f = open('Run_CyCif.sh', 'w')
    with redirect_stdout(f):
        print('#!/bin/bash')
        print('jid2=$(sbatch --dependency=afterok:$jid1 --parsable QC.sh)')
        print('jid3=$(sbatch --dependency=afterok:$jid2 --parsable illumination.sh)')
        print('jid4=$(sbatch --dependency=afterok:$jid3 --parsable stitcher.sh)')
        print('jid5=$(sbatch --dependency=afterok:$jid4 --parsable prob_mapper.sh)')
        print('jid6=$(sbatch --dependency=afterok:$jid5 --parsable segmenter.sh)')
        print('jid7=$(sbatch --dependency=afterok:$jid6 --parsable feature_extractor.sh)')
    f.close()

#copy data from ImStor or to local
class Transfer(object):
    starting_point = master_dir
    scratch = '/n/scratch2/${USER}'
    direction = 'NA'
    directory = master_dir
    command = 'NA'
    sbatch = ['-p transfer','-t 0-2:00', '-J copy','-o copy.o','-e copy.e']

    def __init__(self):
        print ("Initialize Copy Definition")

    # what sbatch parameters to load in O2
    def sbatch_def(self):
        self.sbatch = sbatch_submission()

    # export the sbatch parameters saved
    def sbatch_exporter(self):
        for i in self.sbatch:
            print('#SBATCH ',i)

    # copy data to and from
    def copy_data(self,direction):
        if direction=='from':
            print('Initialize Copying Data to Scratch from ImStor')
            self.direction = direction
            self.command = ''.join(['rsync -arP ',self.directory,' ',self.scratch,'/'])
        if direction=='to':
            print('Initialize Copying Data to ImStor from Scratch')
            self.direction = direction
            self.command = ''.join(['rsync -arP ',self.scratch,self.directory.split('/')[-1],' ', self.directory,'/'])

    #print the sbatch job script
    def print_sbatch_file(self):
        print('#!/bin/bash')
        self.sbatch_exporter()
        print(self.command)

    #save the sbatch job script
    def save_sbatch_file(self):
        if self.direction == 'to':
            f =  open('transfer_to.sh', 'w')
            with redirect_stdout(f):
                self.print_sbatch_file()
            f.close()
        if self.direction == 'from':
            f =  open('transfer_from.sh', 'w')
            with redirect_stdout(f):
                self.print_sbatch_file()
            f.close()

#run it
if __name__ == '__main__':

    if run_type == 'yes-both':
        T1=Transfer()
        T1.copy_data(direction='from')
        T1.save_sbatch_file()

        # transfer data from ImStor
        T2 = Transfer()
        T2.copy_data(direction='to')
        T2.save_sbatch_file()

    if run_type == 'yes-from':
        T1 = Transfer()
        T1.copy_data(direction='from')
        T1.save_sbatch_file()

    if run_type == 'yes-to':
        T1 = Transfer()
        T1.copy_data(direction='to')
        T1.save_sbatch_file()



