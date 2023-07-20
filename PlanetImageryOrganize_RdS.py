
# Planet Imagery Organizer

# Rachel de Sobrino, 2023/07/14

# This script takes PlanetScope imagery downloaded through Planet Explorer and organizes
# them in the following hierarchy: sensor -> date -> image ID -> all files.
#   e.g. ../PlanetScope/2023/2023_05_08/20230508_000_000_000/files
#
# It *should* work on any organization of files, whether it's newly downloaded from Planet
# Explorer or already in some organizational schemata on cryoshare

# TODO if you want: handle PSScene files

# python PlanetImageryOrganize_RdS.py

import os
from tkinter import filedialog as fd
import tkinter as tk
import shutil

root = tk.Tk()
root.withdraw()

# set processing folder
rootdir = fd.askdirectory()
os.chdir(rootdir)

# recursively searches folder structure and reorganizes folders
def nest(wd_path):
    for fname in os.listdir(wd_path):
        fname = fname.replace('._', '')
        f = os.path.join(wd_path, fname)

        # handles SkySat or Planet imagery only, ignores other files
        if os.path.isfile(f) and fname.startswith('20') and ('SkySat' in f or 'PlanetScope' in f or 'PSScene' in f):
            # format date
            y = fname[0:4]
            d = y + '_' + fname[4:6] + '_' + fname[6:8]

            # identify satellite type for filepaths and store filepath up to satellite type
            if 'SkySat' in f:
                sat = 'SkySat'
                rootdir = f[:f.find(sat)]
            # PLanet is handled differently based on if downloaded from PlanetExplorer or re-org on cryoshare
            elif 'PlanetScope' in f:
                sat = 'PlanetScope'
                rootdir = f[:f.find(sat)]
            elif 'PSScene' in f:
                rootdir = f[:f.find('PSScene')]
                sat = 'PlanetScope'

            # extracts image id from filepath
            id = image_id(fname, sat)

            # make directory for image id
            if not os.path.isdir(rootdir+'/'+sat+'/'+y+'/'+d+'/'+id):
                os.makedirs(rootdir+'/'+sat+'/'+y+'/'+d+'/'+id)
            # move associated file to correct directory
            if not os.path.exists(rootdir+'/'+sat+'/'+y+'/'+d+'/'+id+'/'+fname):
                shutil.move(f, rootdir+'/'+sat+'/'+y+'/'+d+'/'+id)

        # continues searching directories, unless not relevant
        elif os.path.isdir(f) and fname not in ['BlackSky', 'DESIS', 'Landsat', 'Sentinel-2', 'Worldview', 'WorldView']:
            nest(wd_path + "/" + fname)


# extracts the image id from the filename
#   NOTE: image ids not of consistent length across and within satellite systems
def image_id(fname, type):
    fname = fname.replace('.', '_')
    if type == 'SkySat':
        fname = fname.split('_')
        id = fname[0]+'_'+fname[1]+'_'+fname[2]+'_'+fname[3]
    elif type == 'PlanetScope':
        fname = fname.split('_')
        id = fname.pop(0)
        while fname[0] not in ['3B', 'json', 'metadata']:
            id += '_'+fname.pop(0)
    return id


# deletes empty folders, if remaining from previous organization scheme
def clean_up(path):
    try:
        for f in os.listdir(path):
            if os.path.isdir(path+'/'+f) and len(os.listdir(path+'/'+f)) == 0:
                print(path+'/'+f)
                shutil.rmtree(path+'/'+f)
            elif os.path.isdir(path+'/'+f):
                clean_up(path+'/'+f)
    # for handling wv imagery file confusion
    except FileNotFoundError:
        print('File Not Found, Skipping: ', path+'/'+f)


# main function
nest(rootdir)

# ... if you want to make trouble
# print('Deleting empty folders... ')
# clean_up(rootdir)
# clean_up(rootdir)
# clean_up(rootdir)
# clean_up(rootdir)
