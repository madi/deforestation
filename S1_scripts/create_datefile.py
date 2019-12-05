
'''
python3 create_datefile.py
'''

import os


def populateList (listname_vv, listname_vh, itemlist):
    for item in itemlist:
        #tokens=item.split("-")
        tokens=item.split("_")
        #print(tokens)
        pol=tokens[-6]
        date=tokens[-5].split("t")[0]
        if pol == "vv":
            listname_vv.append(date)
        elif pol == "vh":
            listname_vh.append(date)
        else:
            return ValueError("Wrong value for polarization %s " %(item))
    return listname_vv, listname_vh
    
def writeOutFile (outFileName, itemlist):
    data = open(outFileName, "w")
    for item in itemlist:
        data.write("%s\n" % (item))
    data.close()
    return 0
    

datafolder="/media/madi/TOSHIBA EXT/S1/S1_db"
outdatefilevv="/media/madi/TOSHIBA EXT/S1/S1_files/S1_db_vv.dates"
outdatefilevh="/media/madi/TOSHIBA EXT/S1/S1_files/S1_db_vh.dates"

filelist=os.listdir(datafolder)

datelistvv1=[]
datelistvh1=[]
datelistvv, datelistvh = populateList(datelistvv1, datelistvh1, filelist)
writeOutFile(outdatefilevv, datelistvv)
writeOutFile(outdatefilevh, datelistvh)






