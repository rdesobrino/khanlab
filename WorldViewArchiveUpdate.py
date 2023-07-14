# This script was written to archive imagery data from CryoShare into
# the format used in the Khan lab's archive spreadsheets

# written by Rachel de Sobrino (desob003@umn.edu), last edited 2023/07/14
# set up modified from Planet Downloads Organizer written by Colby Rand 2023/06/29

import os
from tkinter import filedialog as fd
import tkinter as tk

# Get rid of tkinter root window
root = tk.Tk()
root.withdraw()

# Ask which folder needs to be processed
wd_path = fd.askdirectory()
os.chdir(wd_path)

# dictionaries to store image attributes, by region
wv = {}  # add worldview processing later
FNF = []  # tracks hidden files

# recursively loops through file structure to catalog existing images
# takes a while to run, best to do on region folders and leave running

def prowl(wd_path, wv):
    try:
        for fname in os.listdir(wd_path):
            f = os.path.join(wd_path, fname)
            f = f.replace('._', '').replace('/', '\\').upper()  # reformats filepath

            if os.path.isfile(f):
                # create metadata
                if fname.endswith('.NTF') and ('WV' in f):
                    fpath = f.split("\\")
                    date = fpath[10].replace('_', '/')
                    region = fpath[7]
                    id = fpath[11]
                    sensor = fpath[12][0:3]

                    if region not in wv:
                        wv[region] = [region + '\t' + date + '\t' + sensor + '\t' + id]
                    elif region + '\t' + date + '\t' + sensor + '\t' + id not in wv[region]:
                        wv[region].append(region + '\t' + date + '\t' + sensor + '\t' + id)

            # continue searching relevant directories only
            elif os.path.isdir(f) and fname not in ['BlackSky', 'DESIS', 'Landsat', 'Sentinel-2', 'SkySat', 'PlanetScope']:
                prowl(wd_path+"/" + fname, wv)

        return wv

    except NotADirectoryError:
        wd_path = wd_path.replace('._', '')
        prowl(wd_path, wv)
    except FileNotFoundError:
        FNF.append(wd_path)


wv = prowl(wd_path, wv)

# printed content is tab-delimited and can be copy and pasted into google sheet archive

print('WorldView')
for region in wv:
    print(region)
    for img in wv[region]:
        print(img)

