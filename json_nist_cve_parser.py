#!/usr/bin/env python3

# json_nist_cve_parser

from __future__ import print_function
"""
Command Line Interface for the CVE lookup.
"""
import argparse
from os import listdir
from os.path import isfile, join
import zipfile
import json
import sqlite3


###################################################################
#
# Main
#
# will hold entry triplets from the user provided input file called "packages"
# each elemenet has a vendor-package-version format including the "-" dash

nist_json_cve_list = []     # NIST provided json cve entries for output
header_printed = False
my_final_set = set()
my_final_list = []
FIELD_SPLIT_CHARACTER = '|'

# --------------------------------------------------------------------
# Process the NIST database zip files.
#
# Output is: nist_json_cve_list[]
# Each element of nist_json_cve_list contains:
#
#     [0] vendor-product-version split character
#     [1] cve text description   split character
#     [2] cve value              
#     
# --------------------------------------------------------------------
files = [f for f in listdir("nvd/") if f.endswith('.zip') and isfile(join("nvd/", f))]
files.sort()
nist_json_matched_list = list()


for file in files:
    archive  = zipfile.ZipFile(join("nvd/", file), 'r')
    jsonfile = archive.open(archive.namelist()[0])
    cve_dict = json.loads(jsonfile.read())

    if header_printed == False:
        print("CVE_data_timestamp: "    + str(cve_dict['CVE_data_timestamp']))
        print("CVE_data_version: "      + str(cve_dict['CVE_data_version']))
        print("CVE_data_format: "       + str(cve_dict['CVE_data_format']))
        print(" ")
        header_printed = True

    cve_nist_dict = dict()
    nist_json_cve_entry_list = list()
    totalcvecount = int(str(cve_dict['CVE_data_numberOfCVEs']))
    print("totalcvecount is " + str(totalcvecount))
    for cveiterator in range(0, totalcvecount):
        #print("cveiterator = " + str(cveiterator) + " of " + str(totalcvecount))    
        if len(cve_dict['CVE_Items'][cveiterator]['cve']['affects']['vendor']['vendor_data']) > 0 :
            totalproductnamecount = len(cve_dict['CVE_Items'][cveiterator]['cve']['affects']['vendor']['vendor_data'][0]['product']['product_data'])
            for product_iterator in range(0,totalproductnamecount):
                product_name = str(cve_dict['CVE_Items'][cveiterator]['cve']['affects']['vendor']['vendor_data'][0]['product']['product_data'][0]['product_name'])

            vendor_name = str(cve_dict['CVE_Items'][cveiterator]['cve']['affects']['vendor']['vendor_data'][0]['vendor_name'])
            current_cve_id = str(cve_dict['CVE_Items'][cveiterator]['cve']['CVE_data_meta']['ID'])
            current_cve_description = str(cve_dict['CVE_Items'][cveiterator]['cve']['description']['description_data'][0]['value'].encode("utf-8"))
            
             # iterate over found version values with 
            # data of the vendor-product-version triplet
            for product_name_iterator in range(0, totalproductnamecount):
                if len(cve_dict['CVE_Items'][cveiterator]['cve']['affects']['vendor']['vendor_data'][0]['product']['product_data'][product_name_iterator]['version']['version_data']) > 0 :
                    total_version_range = len(cve_dict['CVE_Items'][cveiterator]['cve']['affects']['vendor']['vendor_data'][0]['product']['product_data'][product_name_iterator]['version']['version_data'])
                   
                    for version_iterator in range(0, total_version_range):
                        the_version = str(cve_dict['CVE_Items'][cveiterator]['cve']['affects']['vendor']['vendor_data'][0]['product']['product_data'][product_name_iterator]['version']['version_data'][version_iterator]['version_value'])
                        nist_json_cve_entry = vendor_name + "-" + product_name + "-" + the_version                      
                        # append only unique data 
                        if nist_json_cve_entry not in nist_json_cve_entry_list :
                            nist_json_cve_entry_list.append(nist_json_cve_entry)
                            nist_json_cve_list.append(nist_json_cve_entry + FIELD_SPLIT_CHARACTER + current_cve_description + FIELD_SPLIT_CHARACTER + current_cve_id)                      
                            # debug
                            #print ("Add this json cve entry " + nist_json_cve_entry )
                            # add this triplet to the cve_nist_dict
                            cve_nist_dict[cveiterator] = {\
                                "current_cve_id"          : current_cve_id,\
                                "nist_json_cve_entry"     : nist_json_cve_entry,\
                                "current_cve_description" : current_cve_description\
                                }
                    # endfor version_iterator
                    #print("Next product")
                # endif
            # endfor product_name 
            #print(cve_nist_dict[cveiterator])            
    # endfor this nvd file is completed.
            
    # Open the file containing the SQL database.
    db_filename = "nistfile"+ file + ".db"
    with sqlite3.connect(db_filename) as conn:
        # Create the nist table if it doesn't exist.
        conn.execute(
            """CREATE TABLE IF NOT EXISTS nist(
                    current_cve_id          varchar(20),
                    nist_json_cve_entry     varchar(100),
                    current_cve_description varchar(100)                    
                );"""
            )
            
        print("Build the table with data")
        # Insert each entry from json into the table.
        keys = ["current_cve_id", "nist_json_cve_entry", "current_cve_description"]
        for entry in cve_nist_dict:
            # This will make sure that each key will default to None
            # if the key doesn't exist in the json entry.
            values = [ cve_nist_dict[entry].get(key, None) for key in keys]
        
            # Execute the command and replace '?' with the each value
            # in 'values'. DO NOT build a string and replace manually.
            # the sqlite3 library will handle non safe strings by doing this.
            cmd = """INSERT INTO nist VALUES(
                        ?,
                        ?,
                        ?
                    );"""
            conn.execute(cmd, values)

    conn.commit()
    #
    # will hold entry triplets from the user provided input file called "packages"
    # each elemenet has a vendor-package-version format including the "-" dash
    package_set = set(open("comsystem3_input",'r').read().split())
    #convert to a dictionary
    package_dict = dict()
    for element in iter(package_set):
        package_dict[element] = { "nist_json_cve_entry" : element }

        conn.execute(
            """CREATE TABLE IF NOT EXISTS packtab(
                    nist_json_cve_entry     varchar(100)
                );"""
            )

        # Insert each entry from json into the table.
        keys = ["nist_json_cve_entry"]
        for entry in package_dict:

            # This will make sure that each key will default to None
            # if the key doesn't exist in the json entry.
            values = [package_dict[entry].get(key, None) for key in keys]

            # Execute the command and replace '?' with the each value
            # in 'values'. DO NOT build a string and replace manually.
            # the sqlite3 library will handle non safe strings by doing this.
            cmd = """INSERT INTO packtab VALUES(
                        ?
                    );"""
            conn.execute(cmd, values)
    # endfor
    conn.commit()
    conn.close()
    print("Tables are built")

    # reset cve_nist_dict
    cve_nist_dict.clear()
    
# endfor - all nvd files complete    


print("All done")        
exit
