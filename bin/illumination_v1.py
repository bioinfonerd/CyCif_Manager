#Purpose: generate illumination files using imageJ
#to run:  python illumination.py ['path to sample folder']
#example: python illumination ./example_data/image_1

#library
from __future__ import print_function
from subprocess import call
try:
    import pathlib
except ImportError:
    import pathlib2 as pathlib
import sys
import os
import datetime

def text_to_bool(text):
    return False \
        if not str(text) \
        else str(text).lower() in '1,yes,y,true,t'
def path_to_date(path):
    return os.path.getmtime(str(path))

#define all
ROI = next(os.walk(sys.argv[1]))[1]

for i in ROI:
    path_exp = pathlib.Path('/'.join([str(sys.argv[1]),i]))
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
