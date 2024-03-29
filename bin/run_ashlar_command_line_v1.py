#library
from __future__ import print_function
import csv
from subprocess import call
try:
    import pathlib
except ImportError:
    import pathlib2 as pathlib
import argparse
import os
import datetime

#function
def text_to_bool(text):
    return False \
        if not str(text) \
        else str(text).lower() in '1,yes,y,true,t'
def path_to_date(path):
    return os.path.getmtime(str(path))

#argument parser
parser = argparse.ArgumentParser(
    description='Read a csv config file and run ashlar'
)
parser.add_argument(
    'csv_filepath', metavar='CSVFILE',
    help='a csv file with header row: Directory, Correction, Pyramid'
)
parser.add_argument(
    '-f', '--from-dir', dest='from_dir', default=0, type=int, metavar='FROM',
    help=('starting directory; numbering starts at 0')
)
parser.add_argument(
    '-t', '--to-dir', dest='to_dir', default=None, type=int, metavar='TO',
    help=('ending directory; numbering starts at 0')
)
args = parser.parse_args()

csv_path = pathlib.Path(args.csv_filepath)
if not csv_path.is_file() or csv_path.suffix != '.csv':
    print('A csv file is required to proceed.')
    parser.print_usage()
    parser.exit()

with open(str(csv_path)) as exp_config:
    exp_config_reader = csv.DictReader(exp_config)
    exps = [dict(row) for row in exp_config_reader]

    # Check the raw_files subfolder for either rcpnl or xdce files
    for exp in exps[args.from_dir: args.to_dir]:
        path_exp = pathlib.Path(exp['Directory'])
        raw_dir = path_exp / 'raw_files'
        files_exp = sorted(raw_dir.glob('*rcpnl'))
        file_type = 'rcpnl'
        if len(files_exp) == 0:
            files_exp = sorted(raw_dir.glob('*xdce'))
            file_type = 'xdce'
        files_exp.sort(key=path_to_date)

        if len(files_exp) == 0:
            print('No rcpnl or xdce files found in', str(raw_dir))
            continue

        print('Processing files in', str(raw_dir))
        print(datetime.datetime.now())
        print()
        if text_to_bool(exp['Correction']):
            lambda_flat = '0.1'
            lambda_dark = '0.01'
            ffp_list = []
            dfp_list = []
            for j in files_exp:
                print('\r    ' + 'Generating ffp and dfp for ' + j.name)
                ffp_file_name = j.name.replace('.' + file_type, '-ffp.tif')
                dfp_file_name = j.name.replace('.' + file_type, '-dfp.tif')
                illumination_dir = path_exp / 'illumination_profiles'
                if (path_exp / 'illumination_profiles' / ffp_file_name).exists() and (
                        path_exp / 'illumination_profiles' / dfp_file_name).exists():
                    print('\r        ' + ffp_file_name + ' already exists')
                    print('\r        ' + dfp_file_name + ' already exists')
                else:
                    if not illumination_dir.exists():
                        illumination_dir.mkdir()
                    call(
                        "/home/ajn16/softwares/Fiji.app/ImageJ-linux64 --ij2 --headless --run /home/ajn16/softwares/Fiji.app/plugins/imagej_basic_ashlar.py \"filename='%s', output_dir='%s', experiment_name='%s', lambda_flat=%s, lambda_dark=%s\"" % (
                        str(j), str(illumination_dir), j.name.replace('.' + file_type, ''), lambda_flat, lambda_dark),
                        shell=True)
                    print('\r        ' + ffp_file_name + ' generated')
                    print('\r        ' + dfp_file_name + ' generated')
                ffp_list.append(str(illumination_dir / ffp_file_name))
                dfp_list.append(str(illumination_dir / dfp_file_name))

    print('Run ashlar')
    print(datetime.datetime.now())
    print()
    out_dir = path_exp / 'registration'
    if not out_dir.exists():
        out_dir.mkdir()
    # Create the desired folder structure for the future steps
    folders_to_make = ['dearray/masks','prob_maps','segmentation','feature_extraction', 'clustering/consensus', 'clustering/drclust', 'clustering/pamsig','cell_states']
    for f in folders_to_make:
        try:
            os.makedirs(str(path_exp)+'/'+f)
        except:
            print('Folder '+f+' already exists')


    input_files = ' '.join([str(f) for f in files_exp])
    command = 'ashlar ' + input_files + ' -m 30 -o ' + str(out_dir)

    if text_to_bool(exp['Pyramid']):
        command += ' --pyramid -f ' + path_exp.name + '_v2.ome.tif'

    if text_to_bool(exp['Correction']):
        ffps = ' '.join(ffp_list)
        dfps = ' '.join(dfp_list)
        command += ' --ffp ' + ffps + ' --dfp ' + dfps

    # print(command)
    call(command, shell=True)
    print(datetime.datetime.now())
