#!/bin/bash

# Creates command line to import bands 4 and 8 into GRASS 
## Usage example
# chmod u+x create_cmd.sh
# ./create_cmd.sh  lista_S2_clean.txt > cmd.sh
# chmod u+x cmd.sh
## from GRASS:
# ./cmd.sh


while IFS='' read -r line || [[ -n "$line" ]]; do
    echo "i.sentinel.import --o -c -r input=$line pattern='B0(4|8)_10m'"
done < "$1"
