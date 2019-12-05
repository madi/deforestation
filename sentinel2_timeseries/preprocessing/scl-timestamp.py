#!/usr/bin/env python

'''
Author: Martin Landa
Modified by Margherita Di Leo

Script to timestamp scene classification cloud masks from current mapset

Usage example:
scl-timestamp.py output=scl-timestamps.txt
'''

#%module
#% description: Timestamps scene classification cloud masks from current mapset.
#%end
#%option G_OPT_F_OUTPUT
#%end

import sys
import os
from datetime import datetime, timedelta

import grass.script as gs

from grass.pygrass.gis import Mapset

def main():
    mapset = Mapset()
    mapset.current()

    with open(options['output'], 'w') as fd:
        for rast in mapset.glist('raster'):
            items = rast.split('_')
            if rast.startswith('T34UFD_') and rast.endswith('_MSK'):
                d = datetime.strptime(items[1], '%Y%m%dT%H%M%S')
            else:
                continue
            #fd.write("{0}|{1}{2}".format(rast, iso_date, os.linesep))
            ## workaround
            dd = d + timedelta(seconds=1)
            fd.write("{0}|{1}|{2}{3}".format(
                rast,
                d.strftime('%Y-%m-%d %H:%M:%S'),
                dd.strftime('%Y-%m-%d %H:%M:%S'),
                os.linesep))
        
    return 0

if __name__ == "__main__":
    options, flags = gs.parser()
    
    sys.exit(main())
