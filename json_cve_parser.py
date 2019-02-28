from os import listdir
from os.path import isfile, join
import zipfile
import json

files = [f for f in listdir("nvd/") if isfile(join("nvd/", f))]
files.sort()
for file in files:
    archive = zipfile.ZipFile(join("nvd/", file), 'r')
    jsonfile = archive.open(archive.namelist()[0])
    cve_dict = json.loads(jsonfile.read())
    
    print("CVE_data_timestamp: " + str(cve_dict['CVE_data_timestamp']))
    print("CVE_data_version: " + str(cve_dict['CVE_data_version']))
    print("CVE_data_format: " + str(cve_dict['CVE_data_format']))
    print("CVE_data_numberOfCVEs: " + str(cve_dict['CVE_data_numberOfCVEs']))
    print("CVE_data_type: " + str(cve_dict['CVE_data_type']))
    
    totalcvecount = int(str(cve_dict['CVE_data_numberOfCVEs']))
    
    for cveiterator in range(0, totalcvecount):
        #cve:CVE_data_meta:ID is the cve number     
        print(json.dumps(cve_dict['CVE_Items'][cveiterator]['cve']['CVE_data_meta']['ID'], sort_keys=True, indent=4, separators=(',', ': ')))
        print(json.dumps(cve_dict['CVE_Items'][cveiterator]['cve']['description']['description_data'][0]['value'], sort_keys=True, indent=4, separators=(',', ': ')))
        #
        # determine the length of the field affects:vendor:vendor_data array 
        # display each entry contianing "product_name"
        #        
        if len(cve_dict['CVE_Items'][cveiterator]['cve']['affects']['vendor']['vendor_data']) > 0 :
           totalproductnamecount = len(cve_dict['CVE_Items'][cveiterator]['cve']['affects']['vendor']['vendor_data'][0]['product']['product_data'])
           for productnameiterator in range(0, totalproductnamecount):
                print(json.dumps(cve_dict['CVE_Items'][cveiterator]['cve']['affects']['vendor']['vendor_data'][0]['product']['product_data'][productnameiterator]['product_name'], sort_keys=True, indent=4, separators=(',', ': ')))
                #
                # iterate over found version values
                #
                if len(cve_dict['CVE_Items'][cveiterator]['cve']['affects']['vendor']['vendor_data'][0]['product']['product_data'][productnameiterator]['version']['version_data']) > 0 :
                   totalversionrange = len(cve_dict['CVE_Items'][cveiterator]['cve']['affects']['vendor']['vendor_data'][0]['product']['product_data'][productnameiterator]['version']['version_data'])
                   for version_iterator in range(0, totalversionrange):
                      print(json.dumps(cve_dict['CVE_Items'][cveiterator]['cve']['affects']['vendor']['vendor_data'][0]['product']['product_data'][productnameiterator]['version']['version_data'][version_iterator]['version_value'], sort_keys=True, indent=4, separators=(',', ': ')))
        
        print("")

    # prints out just the first entry for use as an example
    #print(json.dumps(cve_dict['CVE_Items'][0], sort_keys=True, indent=4, separators=(',', ': ')))
    jsonfile.close()
