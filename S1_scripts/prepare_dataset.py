import os



inFileVV="/eos/jeodpp/home/users/leomarg/Projects/S1_change_detection/S1_VV_bands_bialo.txt"
inFileVH="/eos/jeodpp/home/users/leomarg/Projects/S1_change_detection/S1_VH_bands_bialo.txt"
outFolder="/eos/jeodpp/home/users/leomarg/S1_cropped"
aoi="/eos/jeodpp/home/users/leomarg/aoi_bialo/aoi_bialo.shp"

with open(inFileVV) as f:
    filelist = f.read().splitlines()
    
with open(inFileVH) as f:
    filelist1 = f.read().splitlines()
    
filelist = filelist+filelist1
    


for filename in filelist:
    basename=filename.split("/")[-1]
    cmd='gdalwarp -t_srs "EPSG:32634" -cutline %s -crop_to_cutline %s %s/%s' %(aoi,filename,outFolder,basename)
    #print(cmd)
    os.system(cmd)
