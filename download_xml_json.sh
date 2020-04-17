#!/usr/bin/env bash

[ -d dbs ] || mkdir dbs

[ -d nvd ] || mkdir nvd

rm -rf ./dbs/*
rm -rf ./nvd/*

cd nvd
year=`date +"%Y"`
for i in $(seq -f "%04g" 2002 $year)
do    
    wget https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.0-$i.json.zip -outfile nvdcve-1.0-$i.json.zip

done
# no idea what utfile is, remove it.
rm utfile
cd ..
