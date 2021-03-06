[ -d dbs ] || mkdir dbs

[ -d nvd ] || mkdir nvd

echo "Created dbs and nvd directories"

rm -rf ./dbs/*
rm -rf ./nvd/*

echo "Cleaned existing data from nvd and dbs"

cd nvd
year=`date +"%Y"`
for i in $(seq -f "%04g" 2002 $year)
do    
    echo "wget for $i"
    wget https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-$i.json.zip -outfile nvdcve-1.1-$i.json.zip

done

# no idea what utfile is, remove it.
rm utfile
cd ..
