# !/usr/bin/python

'''
Create GRASS command to import scene classification maps associated to
the sentinel 2 scenes.

Usage:

python list_cloud_cover_files.py

Generates the import_sen2cor_cloud_mask.sh script

from GRASS (mapset cloudcover_sen2cor_v2):

./import_sen2cor_cloud_mask.sh
'''


import os
import re

in_file='/storage/leomarg/Documents/v5/lista_S2_clean.txt'
out_file='/home/leomarg/import_sen2cor_cloud_mask.sh'

out_list = []

with open(in_file, 'r') as f:
    content = f.readlines()
 
content = [x.strip() for x in content] 

for x in content:
    basename = x.strip('.SAFE').split('_')[5]+'_'+x.strip('.SAFE').split('_')[6]
    for root, dirs, files in os.walk(x, topdown=False):
        for name in files:
            #if re.match(name, 'MSK_CLDPRB_20m.jp2'):
            if name.endswith('_SCL_20m.jp2'):
                filename = os.path.join(root, name)
                out_list.append([basename, filename])

with open(out_file, 'w') as f:
    for basename, filename in out_list:
        f.write("r.in.gdal --o input=%s output=%s_SCL_20m  memory=296\n" % (filename,basename))
