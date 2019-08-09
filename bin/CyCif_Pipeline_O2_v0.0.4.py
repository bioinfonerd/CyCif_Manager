
#libraries
from contextlib import redirect_stdout
import yaml
import os

#[TODO]
#define current CyCif module classes & set things that need to be update from user to NA
#read in yaml file [TODO: update class info based on user input, not implemented
#update class use from yaml file
#Print what was parsed from yaml file, what was modified, and what modules are to run
#define function that checks all user defined criteria




###########################
#Generic Function Handling#
###########################

#read in yaml file
file='input.yaml'
def yaml_handler(file):
    with open(file, 'r') as ymlfile:
        try:
            input = yaml.safe_load(ymlfile)
        except yaml.YAMLError as exc:
            print(exc)
    return(input)

##########################################################################
#O2 Specific Functions (not including class functions that are O2 related#
##########################################################################

#bash script that controls slurm submission, organizing, running of cycif pipeline
#[TODO]: update to run each image as a separate string of jobs
#each subsequent job runs only if previous runs to completion and does not have an exit code of zero)
def master(stich,prob,seg,feature):
    f = open('cycif_master.sh', 'w')
    with redirect_stdout(f):
        print('#!/bin/bash')
        print('jid1=$(sbatch --parsable sticher.sh)')
        print('jid2=$(sbatch --dependency=afterok:$jid1 --parsable prob_mapper.sh)')
        print('jid3=$(sbatch --dependency=afterok:$jid2 --parsable segmenter.sh)')
        print('jid4=$(sbatch --dependency=afterok:$jid3 --parsable feature_extractor.sh)')
    f.close()

################################
#CyCIf Method Class Definitions#
################################

#good idea?
#class to handle global parameters that get passed to entir
class General(object):
    def __init__(self):

#stich the multiple images together
#class needs to be modified for use with other stichers (assumption no plan)
class Sticher(object):
    #set class variables to be updated by user to null or No not to run
    self.directory = '/n/groups/lsp/cycif/example_data/ashlar_dirs.csv'
    self.run = 'No'
    self.parameters = '/n/groups/lsp/cycif/ashlar/lib/run_ashlar_csv_batch_v1.7.0.py ashlar_dirs.csv'


    #initilizing method standard class and printing when initialized done
    def __init__(self):
        print ("Initialize Stitcher Definition")
        self.method = 'Ashlar'
        self.environment = '/n/groups/lsp/cycif/ashlar'
        self.executable_path = '/n/groups/lsp/cycif/example_data/run_ashlar_csv_batch.py'
        self.modules = ['conda2/4.2.13']
        self.run = 'python'
        self.sbatch = ['-p short', '-t 0-2:00', '--mem=64G', '-J ashlar', '-o ashlar.o', '-e ashlar.e']

    # use this function to update from yaml input
    def yaml_updater(self):
        print(self.method)

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
        f =  open('sticher.sh', 'w')
        with redirect_stdout(f):
            self.print_sbatch_file()
        f.close()

#determine probability of cell boundary on image
class Probability_Mapper(object):
    method = 'Unet'
    run = 'No'
    environment = '/n/groups/lsp/cycif/unet_segmenter/unet'
    directory = '/n/groups/lsp/cycif/example_data/'
    executable_path = '/n/groups/lsp/cycif/example_data/run_batchUNet2DtCycif_ajit.py'
    parameters = 'run_batchUNet2DtCycif_ajit.py'
    modules = ['gcc/6.2.0','cuda/9.0','conda2/4.2.13']
    run = 'python'
    sbatch = ['-p gpu','-n 1','-c 12', '--gres=gpu:1','-t 0-5:00','--mem=64000',
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
        print(self.run, self.parameters,self.directory)
        print('conda deactivate')

    #save the sbatch job script
    def save_sbatch_file(self):
        f =  open('prob_mapper.sh', 'w')
        with redirect_stdout(f):
            self.print_sbatch_file()
        f.close()

#segment fluroscence probes
class Segementer(object):
    method = 'matlab_jerry'
    run = 'No'
    #directory = '/n/groups/lsp/cycif/example_data/'
    directory = '/c/Users/Nathan/Documents/@Dana_Farber/CyCif'
    modules = ['matlab/2018b']
    run = 'matlab -nodesktop -r'
    program = '"addpath(genpath(\'/n/groups/lsp/cycif/unet_segmenter/segmenter/\'));O2batchS3segmenterWrapper('
    files = []
    parameters =  ",1,'/n/groups/lsp/cycif/example_data','TissueMaskChan',[2],'logSigma',[3 30],'mask'," \
                  "'tissue','segmentCytoplasm','ignoreCytoplasm')\""
    sbatch = ['-p short', '-t 0-5:00', '-c 8','--mem=100G', '-J segmenter', '-o segmenter.o', '-e segmenter.e']

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
                print(self.run,self.program,i+1,self.parameters)

    #save the sbatch job script
    def save_sbatch_file(self):
        f =  open('segmenter.sh', 'w')
        with redirect_stdout(f):
            self.print_sbatch_file()
        f.close()

#extra features from image
class feature_extractor(object):
    method = 'histocat'
    run = 'No'
   #directory = '/n/groups/lsp/cycif/example_data/'
    directory = '/c/Users/Nathan/Documents/@Dana_Farber/CyCif'
    modules = ['matlab/2018b']
    run = 'matlab -nodesktop -r'
    program = '"addpath(genpath(\'/n/groups/lsp/cycif/histoCAT/\'));Headless_histoCAT_loading('
    files = []
    # [TODO] fix use of parameter input (right now its hard coded)
    #parameters = ["/registration',",".ome.tif','/n/groups/lsp/cycif/example_data/","image_2/segmentation/","'cellMask.tif','/n/groups/lsp/cycif/cycif_pipeline_testing_space/markers.csv','5')"]
    parameters = ["5"]
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
                tmp = tmp.__add__(''.join(["'cellMask.tif'",",'",part4.directory,"markers.csv'",",","'",part4.parameters[0] ,"')\""]))
                print(part4.run,part4.program,tmp)

    #save the sbatch job script
    def save_sbatch_file(self):
        f =  open('feature_extractor.sh', 'w')
        with redirect_stdout(f):
            self.print_sbatch_file()
        f.close()

#run it
if __name__ == '__main__':
    #output sbatch files for each component in pipeline
    #define sticher & make sbatch file for task
    part1=Sticher()
    part1.save_sbatch_file()

    #define probability mapper
    part2=Probability_Mapper()
    part2.save_sbatch_file()

    #define segmenter
    part3=Segementer()
    part3.file_finder() #update file names from directory path
    part3.save_sbatch_file()

    #define histocat
    part4=feature_extractor()
    part4.file_finder()#update file names from directory path
    part4.save_sbatch_file()

    #output master run file to manage running cycif pipeline
    master(part1,part2,part3,part4)
    os.system('chmod 755 cycif_master.sh') #change permissions to make file runable on linux
