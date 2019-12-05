
"""
python3 crop2aoi.py
"""

import os



inFolder="/eos/jeodpp/home/users/leomarg/Sentinel1_scaled_images"
outFolder="/eos/jeodpp/home/users/leomarg/S1_cropped"
aoi="/eos/jeodpp/home/users/leomarg/aoi_bialo/aoi_bialo.shp"


filelist=os.listdir(inFolder)

for filename in filelist:
    cmd='gdalwarp -t_srs "EPSG:32634" -cutline %s -crop_to_cutline %s/%s %s/%s' %(aoi,inFolder,filename,outFolder,filename)
    os.system(cmd)
    
