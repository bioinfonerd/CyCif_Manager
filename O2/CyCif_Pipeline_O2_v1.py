
#libraries
from contextlib import redirect_stdout
import yaml
import os
import sys
import shutil

#handles path to data correctly
master_dir = os.path.normpath(sys.argv[1])

######################
#O2 Handling Function#
######################

#master job that controls submission, organizing, running of cycif pipeline
#each subsequent job runs only if previous runs to completion and does not have an exit code of zero)
def master():
    f = open('Run_CyCif.sh', 'w')
    with redirect_stdout(f):
        print('#!/bin/bash')
        print('jid1=$(sbatch --parsable transfer_from.sh)')
        print('jid2=$(sbatch --dependency=afterok:$jid1 --parsable QC.sh)')
        print('jid3=$(sbatch --dependency=afterok:$jid2 --parsable illumination.sh)')
        print('jid4=$(sbatch --dependency=afterok:$jid3 --parsable stitcher.sh)')
        print('jid5=$(sbatch --dependency=afterok:$jid4 --parsable prob_mapper.sh)')
        print('jid6=$(sbatch --dependency=afterok:$jid5 --parsable segmenter.sh)')
        print('jid7=$(sbatch --dependency=afterok:$jid6 --parsable feature_extractor.sh)')
        print('jid8=$(sbatch --dependency=afterok:$jid7 --parsable transfer_to.sh)')
    f.close()

################################
#CyCIf Method Class Definitions#
################################

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

#QC (at the moment just folder infrastructure checking) [TODO]
class QC(object):
    directory = master_dir
    executable_path = '../bin/check_folder_v1.py'
    environment = '../environments/cycif_pipeline'
    parameters = ''
    modules = ['conda2/4.2.13']
    run = 'python'
    sbatch = ['-p short', '-t 0-1:00', '-J QC', '-o QC.o', '-e QC.e']

    # initilizing class and printing when done
    def __init__(self):
        print("Initialize QC Definition")

    # what sbatch parameters to load in O2
    def sbatch_def(self):
        self.sbatch = sbatch_submission()

    # export the sbatch parameters saved
    def sbatch_exporter(self):
        for i in self.sbatch:
            print('#SBATCH ', i)

    # export the module parameters
    def module_exporter(self):
        for i in self.modules:
            print('module load', i)

    # print the sbatch job script
    def print_sbatch_file(self):
        print('#!/bin/bash')
        self.sbatch_exporter()
        self.module_exporter()
        print('source activate ', self.environment)
        print(self.run, self.parameters)
        print('conda deactivate')

    # save the sbatch job script
    def save_sbatch_file(self):
        f = open('QC.sh', 'w')
        with redirect_stdout(f):
            self.print_sbatch_file()
        f.close()

#Illumination Profiles (pre-req for ashlar) [TODO]
class Ilumination(object):
    environment = '../environments/ImageJ'
    directory = master_dir
    executable_path = '../bin/illumination_v1.py'
    parameters = ''
    modules = ['conda2/4.2.13']
    run = 'python'
    sbatch = ['-p short', '-t 0-2:00', '--mem=64G', '-J ashlar', '-o ashlar.o', '-e ashlar.e']

    # initilizing class and printing when done
    def __init__(self):
        print("Initialize Illumination Definition")

    # what sbatch parameters to load in O2
    def sbatch_def(self):
        self.sbatch = sbatch_submission()

    # export the sbatch parameters saved
    def sbatch_exporter(self):
        for i in self.sbatch:
            print('#SBATCH ', i)

    # export the module parameters
    def module_exporter(self):
        for i in self.modules:
            print('module load', i)

    # print the sbatch job script
    def print_sbatch_file(self):
        print('#!/bin/bash')
        self.sbatch_exporter()
        self.module_exporter()
        print('source activate ', self.environment)
        print(self.run, self.parameters)
        print('conda deactivate')

    # save the sbatch job script
    def save_sbatch_file(self):
        f = open('illumination.sh', 'w')
        with redirect_stdout(f):
            self.print_sbatch_file()
        f.close()

#stich the multiple images together [TODO]: fix what runs
class Stitcher(object):
    method = 'Ashlar'
    run = 'No'
    environment = '../environments/ashlar'
    directory = master_dir
    program = '../bin/run_ashlar_csv_batch.py'
    parameters = '/n/groups/lsp/cycif/ashlar/lib/run_ashlar_csv_batch_v1.7.0.py ashlar_dirs.csv'
    modules = ['conda2/4.2.13']
    run = 'python'
    sbatch = ['-p short','-t 0-2:00', '--mem=64G', '-J ashlar','-o ashlar.o','-e ashlar.e']

    #initilizing class and printing when done
    def __init__(self):
        print ("Initialize Stitcher Definition")

    # what sbatch parameters to load in O2
    def sbatch_def(self):
        self.sbatch = sbatch_submission()

    # export the sbatch parameters saved
    def sbatch_exporter(self):
        for i in self.sbatch:
            print('#SBATCH ',i)

    # export the module parameters
    def module_exporter(self):
        for i in self.modules:
            print('module load',i)

    #print the sbatch job script
    def print_sbatch_file(self):
        print('#!/bin/bash')
        self.sbatch_exporter()
        self.module_exporter()
        print('source activate ', self.environment)
        print(self.run, self.parameters)
        print('conda deactivate')

    #save the sbatch job script
    def save_sbatch_file(self):
        f =  open('stitcher.sh', 'w')
        with redirect_stdout(f):
            self.print_sbatch_file()
        f.close()

#determine probability of cell boundary on image
class Probability_Mapper(object):
    method = 'Unet'
    run = 'No'
    environment = '../environments/unet'
    directory = master_dir
    executable_path = '../bin/run_batchUNet2DtCycif_V1.py'
    parameters = ['run_batchUNet2DtCycif_V1.py',0,1,1]
    modules = ['gcc/6.2.0','cuda/9.0','conda2/4.2.13']
    run = 'python'
    sbatch = ['-p gpu','-n 1','-c 12', '--gres=gpu:1','-t 0-1:00','--mem=64000',
              '-e probability_mapper.e','-o probability_mapper.o', '-J prob_mapper']

    #initilizing class and printing when done
    def __init__(self):
        print ("Initialize Probability Mapper Definition")

    # what sbatch parameters to load in O2
    def sbatch_def(self):
        self.sbatch = sbatch_submission()

    # export the sbatch parameters saved
    def sbatch_exporter(self):
        for i in self.sbatch:
            print('#SBATCH ',i)

    # export the module parameters
    def module_exporter(self):
        for i in self.modules:
            print('module load',i)

    #print the sbatch job script
    def print_sbatch_file(self):
        print('#!/bin/bash')
        self.sbatch_exporter()
        self.module_exporter()
        print('source activate ', self.environment)
        print(self.run, self.parameters[0],self.directory,self.parameters[1],self.parameters[1],self.parameters[3])
        print('conda deactivate')

    #save the sbatch job script
    def save_sbatch_file(self):
        f =  open('prob_mapper.sh', 'w')
        with redirect_stdout(f):
            self.print_sbatch_file()
        f.close()

#segment fluroscence probes
class Segementer(object):
    method = 'S3'
    run = 'No'
    directory = master_dir
    modules = ['matlab/2018b']
    run = 'matlab -nodesktop -r '
    program = '"addpath(genpath(\'../environments/segmenter/\'));O2batchS3segmenterWrapperR('
    files = []
    parameters =  ",'HPC','true','fileNum',1,'TissueMaskChan',[2],'logSigma',[3 30],'mask'," \
                  "'tissue','segmentCytoplasm','ignoreCytoplasm')\""
    sbatch = ['-p short', '-t 0-5:00', '-c 1','--mem=100G', '-J segmenter', '-o segmenter.o', '-e segmenter.e']

    #initilizing class and printing when done
    def __init__(self):
        print ("Initialize Segmenter Definition")

    # what sbatch parameters to load in O2
    def sbatch_def(self):
        self.sbatch = sbatch_submission()

    # export the sbatch parameters saved
    def sbatch_exporter(self):
        for i in self.sbatch:
            print('#SBATCH ',i)

    # export the module parameters
    def module_exporter(self):
        for i in self.modules:
            print('module load',i)

    #find all folder names from the directory path position
    def file_finder(self):
        self.files=next(os.walk(self.directory))[1]

    #print the sbatch job script
    def print_sbatch_file(self):
        print('#!/bin/bash')
        self.sbatch_exporter()
        self.module_exporter()
        if not self.files: #if files have not been updated, throw error
            print('No Files Found')
        #else: #for each file print out separate run command
        #    for i in self.files:
        #        print(self.run,self.program,i,self.parameters)
        else: #for each file print out separate run command
            for i in range(len(next(os.walk(self.directory))[1])):
                print(self.run,self.program,"'",self.directory,"'",self.parameters,sep='')

    #save the sbatch job script
    def save_sbatch_file(self):
        f =  open('segmenter.sh', 'w')
        with redirect_stdout(f):
            self.print_sbatch_file()
        f.close()

#extra features from image
class feature_extractor(object):
    method = 'histoCat'
    run = 'No'
    directory = master_dir
    modules = ['matlab/2018b']
    run = 'matlab -nodesktop -r '
    program = '"addpath(genpath(\'../environments/histoCAT/\'));Headless_histoCAT_loading('
    files = []
    # [TODO] fix use of parameter input (right now its hard coded)
    #parameters = ["/registration',",".ome.tif','/n/groups/lsp/cycif/example_data/","image_2/segmentation/","'cellMask.tif','/n/groups/lsp/cycif/cycif_pipeline_testing_space/markers.csv','5')"]
    parameters = ["5", "no"]
    sbatch = ['-p short', '-t 0-5:00', '-c 8','--mem=100G', '-J feature_extractor', '-o feature_extractor.o', '-e feature_extractor.e']

    #initilizing class and printing when done
    def __init__(self):
        print ("Initialize Feature Extractor Definition")

    # what sbatch parameters to load in O2
    def sbatch_def(self):
        self.sbatch = sbatch_submission()

    # export the sbatch parameters saved
    def sbatch_exporter(self):
        for i in self.sbatch:
            print('#SBATCH ',i)

    # export the module parameters
    def module_exporter(self):
        for i in self.modules:
            print('module load',i)

    #find all folder names from the directory path position
    def file_finder(self):
        self.files=next(os.walk(self.directory))[1]

    #print the sbatch job script
    def print_sbatch_file(self):
        print('#!/bin/bash')
        self.sbatch_exporter()
        self.module_exporter()
        if not self.files: #if files have not been updated, throw error
            print('No Files Found')
        else: #for each file print out separate run command
            for i in self.files:
                #specific for histocat TODO: change to be yaml inputable
                tmp = ''
                tmp = tmp.__add__(''.join(["'",part4.directory,i,"/registration'",","]))
                tmp = tmp.__add__(''.join(["'",i,".ome.tif',"]))
                tmp = tmp.__add__(''.join(["'",part4.directory,i,'/segmentation/',i,"',"]))
                tmp = tmp.__add__(''.join(["'cellMask.tif'",",'",part4.directory,"markers.csv'",",","'",part4.parameters[0] ,"'",",","'",part4.parameters[1] ,"')\""]))
                print(part4.run,part4.program,tmp,sep='')
        print("mv ./output",self.directory)

    #save the sbatch job script
    def save_sbatch_file(self):
        f =  open('feature_extractor.sh', 'w')
        with redirect_stdout(f):
            self.print_sbatch_file()
        f.close()

#run it
if __name__ == '__main__':
    #output sbatch files for each component in pipeline

    #transfer data from ImStor
    part1=Transfer()
    part1.copy_data(direction='from')
    part1.save_sbatch_file()

    #QC
    part2=QC()
    part2.save_sbatch_file()

    #Illumination
    part3=Ilumination()
    part3.save_sbatch_file()

    #define stitcher & make sbatch file for task
    part4=Stitcher()
    part4.save_sbatch_file()

    #define probability mapper
    part5=Probability_Mapper()
    part5.save_sbatch_file()

    #define segmenter
    part6=Segementer()
    part6.file_finder() #update file names from directory path
    part6.save_sbatch_file()

    #define histocat
    part7=feature_extractor()
    part7.file_finder()#update file names from directory path
    part7.save_sbatch_file()

    #transfer data from ImStor
    part8=Transfer()
    part8.copy_data(direction='to')
    part8.save_sbatch_file()

    #output master run file to manage running cycif pipeline
    master()
    os.system('chmod 755 Run_CyCif.sh') #change permissions to make file runable on linux
