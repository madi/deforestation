
"""
python3 create_vrt.py
"""

import os
from create_datefile import writeOutFile

def tellPol (listname_vv, listname_vh, itemlist):
    for item in itemlist:
        #tokens=item.split("-")
        tokens=item.split("_")
        pol=tokens[-6]
        if pol == "vv":
            listname_vv.append(item)
        elif pol == "vh":
            listname_vh.append(item)
        else:
            return ValueError("Wrong value for polarization %s " %(item))
    return listname_vv, listname_vh



    

datafolder="/media/madi/TOSHIBA EXT/S1/S1_db"
destfilelist_vv="/media/madi/TOSHIBA EXT/S1/S1_files/S1_db_vv.images"
destfilelist_vh="/media/madi/TOSHIBA EXT/S1/S1_files/S1_db_vh.images"
# Needed by gdal to manage space in the path
destfilelist1_vv="/media/madi/TOSHIBA\ EXT/S1/S1_files/S1_db_vv.images"
destfilelist1_vh="/media/madi/TOSHIBA\ EXT/S1/S1_files/S1_db_vh.images"
destvrt_vv="/media/madi/TOSHIBA\ EXT/S1/S1_db/s1_db_stack_vv.vrt"
destvrt_vh="/media/madi/TOSHIBA\ EXT/S1/S1_db/s1_db_stack_vh.vrt"


filelist=os.listdir(datafolder)

filelistvv1=[]
filelistvh1=[]
filelistvv, filelistvh = tellPol(filelistvv1, filelistvh1, filelist)

writeOutFile(destfilelist_vv, filelistvv)
writeOutFile(destfilelist_vh, filelistvh)

os.chdir(datafolder)

cmd_vv="gdalbuildvrt -separate -input_file_list %s %s " %(destfilelist1_vv,destvrt_vv)
cmd_vh="gdalbuildvrt -separate -input_file_list %s %s " %(destfilelist1_vh,destvrt_vh)

# print(cmd_vv)
# print(cmd_vh)

os.system(cmd_vv)
os.system(cmd_vh)

