#!/usr/bin/env python

'''
Script to parse the pattern given from jhub and cut it to the ".SAFE" extension

## Usage example

```
python parse_sentinel_pattern.py lista_S2.txt
```

generates the new list in the terminal.
'''

import sys
with open( sys.argv[1]  ) as file:
    for line in file:
        print line.split(".SAFE")[0] + ".SAFE"
