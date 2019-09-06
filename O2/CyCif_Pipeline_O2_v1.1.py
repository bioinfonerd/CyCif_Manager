#libraries
from contextlib import redirect_stdout
import yaml
import os
import sys
import shutil
import glob

#handles path to data correctly
#master_dir = os.path.normpath(sys.argv[1])
master_dir = os.path.normpath('/home/bionerd/Dana_Farber/CyCif/git/CyCif_Manager/example_data/')
os.chdir('/home/bionerd/Dana_Farber/CyCif/git/CyCif_Manager/O2')

######################
#O2 Handling Function#
######################

#master job that controls submission, organizing, running of cycif pipeline (may want to split functions)
def master(samples):
    #create list of lists to handle organizing job ranking and submission

    #look for all scripts to include in O2 run
    files = glob.glob('*.sh')

    #Order of list is dependent on order of pipeline steps to be run
    pipeline = ['QC','illumination','stitcher','prob_mapper','segmenter','feature_extractor']

    # list length of number of samples plus one to store the QC step
    res = lst = [[] for _ in range(len(samples)+1)]

    # for QC step
    res[0] = [i for i in files if pipeline[0] in i]

    #make list of lists for each sample to be put together
    for n in range(1,len(pipeline)):

        #grab all files to be run as part of each stage
        tmp = [i for i in files if pipeline[n] in i]

        #populate the list with each file (TOFIX:list comprehension?)
        for i in range(0,len(tmp)):
            res[i+1].append(tmp[i])

    #write list to file with job id dependencies
    f = open('Run_CyCif_pipeline.sh', 'w')
    with redirect_stdout(f):
        print('#!/bin/bash')
        #QC step
        print('jid1=$(sbatch --parsable '+res[0][0]+')')

        #each step dependent on QC run, then a stack is made separated for each individual sample ID
        for i in range(1,len(res)):
            for n in range(0,len(res[i])):
                if i == 0 & n == 0:
                    current_jobID = 2

                if n == 0:
                    previous_job_id = 1
                    print('jid'+str(current_jobID)+'=$(sbatch --dependency=afterok:$jid'+str(previous_job_id)+' --parsable '+res[i][n]+')')
                    previous_job_id=previous_job_id+1
                    #current_jobID=current_jobID+1

                print('jid' + str(current_jobID) + '=$(sbatch --dependency=afterok:$jid' + str(previous_job_id) + ' --parsable ' + res[i][n] + ')')
                previous_job_id = previous_job_id + 1
                current_jobID = current_jobID + 1

    f.close()

################################
#CyCIf Method Class Definitions#
################################

#QC (at the moment just folder infrastructure checking) [TODO]
class QC(object):
    directory = master_dir
    executable_path = '../bin/check_folder_v1.py'
    environment = '/n/groups/lsp/cycif/CyCif_Manager/environments/cycif_pipeline'
    parameters = master_dir
    modules = ['conda2/4.2.13']
    run = 'python /n/groups/lsp/cycif/CyCif_Manager/bin/check_folder_v1.py'
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
        print('sleep 5') # wait for slurm to get the job status into its database
        print('sacct --format=JobID,Submit,Start,End,State,Partition,ReqTRES%30,CPUTime,MaxRSS,NodeList%30 --units=M -j $SLURM_JOBID') #resource usage

    # save the sbatch job script
    def save_sbatch_file(self):
        f = open('QC.sh', 'w')
        with redirect_stdout(f):
            self.print_sbatch_file()
        f.close()

#Illumination Profiles (pre-req for ashlar) [TODO]
class Ilumination(object):
    environment = '/n/groups/lsp/cycif/CyCif_Manager/environments/ImageJ'
    directory = master_dir
    parameters = '/n/groups/lsp/cycif/CyCif_Manager/bin/illumination_v1.py'
    modules = ['conda2/4.2.13']
    run = 'python '
    sbatch = ['-p short', '-t 0-12:00', '--mem=64G', '-J illumination',
              '-o illumination.o', '-e illumination.e']
    sample = 'NA'
    sbatchfilename = 'NA'

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
        print(self.run, self.parameters, self.directory+'/'+self.sample)
        print('conda deactivate')
        print('sleep 5') # wait for slurm to get the job status into its database
        print('sacct --format=JobID,Submit,Start,End,State,Partition,ReqTRES%30,CPUTime,MaxRSS,NodeList%30 --units=M -j $SLURM_JOBID') #resource usage

    # save the sbatch job script
    def save_sbatch_file(self):
        self.sbatchfilename = self.sample + '_illumination.sh'
        f = open(self.sbatchfilename, 'w')
        with redirect_stdout(f):
            self.print_sbatch_file()
        f.close()

#stich the multiple images together [TODO]: fix what runs
class Stitcher(object):
    method = 'Ashlar'
    run = 'No'
    environment = '/n/groups/lsp/cycif/CyCif_Manager/environments/ashlar'
    directory = master_dir
    program = '/n/groups/lsp/cycif/CyCif_Manager/bin/run_ashlar_v1.py'
    modules = ['conda2/4.2.13']
    run = 'python'
    sbatch = ['-p short','-t 0-12:00', '--mem=64G', '-J ashlar',
              '-o ashlar.o','-e ashlar.e']
    sample = 'NA'

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
        print(self.run, self.program, self.directory+'/'+self.sample)
        print('conda deactivate')
        print('sleep 5') # wait for slurm to get the job status into its database
        print('sacct --format=JobID,Submit,Start,End,State,Partition,ReqTRES%30,CPUTime,MaxRSS,NodeList%30 --units=M -j $SLURM_JOBID') #resource usage

    # save the sbatch job script
    def save_sbatch_file(self):
        self.sbatchfilename = self.sample + '_stitcher.sh'
        f = open(self.sbatchfilename, 'w')
        with redirect_stdout(f):
            self.print_sbatch_file()
        f.close()

#determine probability of cell boundary on image
class Probability_Mapper(object):
    method = 'Unet'
    run = 'No'
    environment = '/n/groups/lsp/cycif/CyCif_Manager/environments/unet'
    directory = master_dir
    executable_path = '../bin/run_batchUNet2DtCycif_V1.py'
    parameters = ['/n/groups/lsp/cycif/CyCif_Manager/bin/run_batchUNet2DtCycif_v1.py',0,1,1]
    modules = ['gcc/6.2.0','cuda/9.0','conda2/4.2.13']
    run = 'python'
    sbatch = ['-p gpu','-n 1','-c 12', '--gres=gpu:1','-t 0-12:00','--mem=64000',
              '-e probability_mapper.e','-o probability_mapper.o', '-J prob_mapper']
    sample = 'NA'

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
        print(self.run, self.parameters[0],self.directory+'/'+self.sample,self.parameters[1],self.parameters[2],self.parameters[3])
        print('conda deactivate')
        print('sleep 5') # wait for slurm to get the job status into its database
        print('sacct --format=JobID,Submit,Start,End,State,Partition,ReqTRES%30,CPUTime,MaxRSS,NodeList%30 --units=M -j $SLURM_JOBID') #resource usage

    # save the sbatch job script
    def save_sbatch_file(self):
        self.sbatchfilename = self.sample + '_prob_mapper.sh'
        f = open(self.sbatchfilename, 'w')
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
    program = '"addpath(genpath(\'/n/groups/lsp/cycif/CyCif_Manager/environments/segmenter/\'));O2batchS3segmenterWrapperR('
    parameters =  ",'HPC','true','fileNum',1,'TissueMaskChan',[2],'logSigma',[3 30],'mask'," \
                  "'tissue','segmentCytoplasm','ignoreCytoplasm')\""
    sbatch = ['-p short', '-t 0-12:00', '-c 1','--mem=100G', '-J segmenter', '-o segmenter.o', '-e segmenter.e']
    sample = 'NA'

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
        print(self.run,self.program,"'",self.directory+'/'+self.sample,"'",self.parameters,sep='')
        print('sleep 5')  # wait for slurm to get the job status into its database
        print('sacct --format=JobID,Submit,Start,End,State,Partition,ReqTRES%30,CPUTime,MaxRSS,NodeList%30 --units=M -j $SLURM_JOBID')  # resource usage

    # save the sbatch job script
    def save_sbatch_file(self):
        self.sbatchfilename = self.sample + '_segmenter.sh'
        f = open(self.sbatchfilename, 'w')
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
    program = '"addpath(genpath(\'/n/groups/lsp/cycif/CyCif_Manager/environments/histoCAT/\'));Headless_histoCAT_loading('
    parameters = ["5", "no"]
    sbatch = ['-p short', '-t 0-12:00', '-c 8','--mem=100G', '-J feature_extractor', '-o feature_extractor.o', '-e feature_extractor.e']
    sample = 'NA'

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
        #specific for histocat TODO: change to be yaml inputable
        tmp = ''
        tmp = tmp.__add__(''.join(["'",self.directory,"/",self.sample,"/registration'",","]))
        tmp = tmp.__add__(''.join(["'",self.sample,".ome.tif',"]))
        tmp = tmp.__add__(''.join(["'",self.directory,"/",self.sample,'/segmentation/',self.sample,"',"]))
        tmp = tmp.__add__(''.join(["'cellMask.tif'",",'",self.directory,"/","markers.csv'",",","'",self.parameters[0] ,"'",",","'",self.parameters[1] ,"')\""]))
        print(self.run,self.program,tmp,sep='')
        print("mv",''.join(['./output/',self.sample,'/*']),''.join([self.directory,'/',self.sample,'/segmentation']))
        print("rm -r ",''.join(['./output/',self.sample]))
        print('sleep 5') # wait for slurm to get the job status into its database
        print('sacct --format=JobID,Submit,Start,End,State,Partition,ReqTRES%30,CPUTime,MaxRSS,NodeList%30 --units=M -j $SLURM_JOBID') #resource usage

    # save the sbatch job script
    def save_sbatch_file(self):
        self.sbatchfilename = self.sample + '_feature_extractor.sh'
        f = open(self.sbatchfilename, 'w')
        with redirect_stdout(f):
            self.print_sbatch_file()
        f.close()

#run it
if __name__ == '__main__':
    #output sbatch files to run for O2 for each component in pipeline

    # grab all image folders within master directory
    samples = next(os.walk(master_dir))[1]

    #QC
    part1=QC()
    part1.save_sbatch_file()

    #for each sample create a pipeline structure for that sample
    for n in samples:

        # Illumination
        part2 = Ilumination()
        part2.sample = n
        part2.save_sbatch_file()

        # define stitcher & make sbatch file for task
        part3 = Stitcher()
        part3.sample = n
        part3.save_sbatch_file()

        # define probability mapper
        part4 = Probability_Mapper()
        part4.sample = n
        part4.save_sbatch_file()

        # define segmenter
        part5 = Segementer()
        part5.sample = n
        part5.save_sbatch_file()

        # define histocat
        part6 = feature_extractor()
        part6.sample = n
        part6.save_sbatch_file()

        #output master run file to manage running cycif pipeline

    #merge all sbatch jobs for the samples to be run into one file to be submitted to O2
    master(samples)

    # change permissions to make file runable on linux
    os.system('chmod 755 Run_CyCif_pipeline.sh')
