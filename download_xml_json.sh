#!/usr/bin/env bash

mkdir -p nvd
cd nvd

year=`date +"%Y"`
for i in $(seq -f "%04g" 2002 $year)
do    
    wget  https://nvd.nist.gov/feeds/json/cve/1.0/nvdcve-1.0-$i.json.zip -outfile nvdcve-1.0-$i.json.zip

done
# no idea what utfile is, remove it.
rm utfile
cd ..
