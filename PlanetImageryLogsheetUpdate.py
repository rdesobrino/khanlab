# This script was written to archive imagery data from CryoShare into
# the format used in the Khan lab's archive spreadsheets

# written by Rachel de Sobrino (desob003@umn.edu), last edited 2023/07/09
# modified from Planet Downloads Organizer written by Colby Rand 2023/06/29

import os
from tkinter import filedialog as fd
import tkinter as tk
import json

# Get rid of tkinter root window
root = tk.Tk()
root.withdraw()

# Ask which folder needs to be processed
wd_path = fd.askdirectory()
os.chdir(wd_path)

# dictionaries to store image attributes, by region
skysat = {}
planet = {}
wv = {}
FNF = []  # hidden files

# recursively loops through file structure to catalog existing images
# takes a while to run, best to do on region folders and leave running

def prowl(wd_path, skysat, planet):
    try:
        for fname in os.listdir(wd_path):
            f = os.path.join(wd_path, fname)
            f = f.replace('._', '')  # removes hidden mac pathnames
            if os.path.isfile(f):
                # PlanetExplorer
                if fname.endswith('metadata.json') and ('SkySat' in f or 'PlanetScope' in f):
                    with open(f, 'r') as _json:
                        text = json.load(_json)
                        image_id = text['id']
                        date = text['properties']['acquired'][:10]
                        if text['properties']['item_type'] == 'SkySatCollect':  # add skysat imagery to dictionary
                            if f[71:f.find('SkySat') + 6] not in skysat:  # creates dictionary key for region if does not exist
                                skysat[f[71:f.find('SkySat') + 6]] = [image_id + '\t' + date]
                            else:
                                skysat[f[71:f.find('SkySat') + 6]].append(image_id + '\t' + date)
                        elif 'PS' in text['properties']['item_type']:  # add planet imagery to dictionary
                            if f[71:f.find('PlanetScope') + 11] not in planet:  # creates dictionary key for region if does not exist
                                planet[f[71:f.find('PlanetScope') + 11]] = [image_id + '\t' + date]
                            else:
                                planet[f[71:f.find('PlanetScope') + 11]].append(image_id + '\t' + date)
            else:  # continues searching directories
                prowl(wd_path+"/" + fname, skysat, planet)
        return skysat, planet
    except NotADirectoryError:
        wd_path = wd_path.replace('._', '')
        prowl(wd_path, skysat, planet)
    except FileNotFoundError:
        FNF.append(wd_path)


skysat, planet = prowl(wd_path, skysat, planet)

# printed content is tab-delimited and can be copy and pasted into google sheet archive
'''
print('SkySat')
for region in skysat:
    print(region)
    for img in skysat[region]:
        print(img)
'''
print('Planet')
for region in planet:
    print(region)
    for img in planet[region]:
        print(img)


