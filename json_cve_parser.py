#!/usr/bin/env python3

# json_nist_cve_parser <packages file name> | -i <ignore file name>
# Input: 
#   <packages file name> A file name continaing the packages of interest
#   <ignore file name> A file name continaing CVE-XYZ values to ignore
# Output:
#   The database files in ./nvd/*.db will have an additional table 
#   created continaing package name triplets. 
#
# Precondition is that json_nist_database_builder.py has created one or
# more *.db database files from the NIST JSON CVE database.
#
# For every database file created by json_nist_database_builder.py
# create an additional table to hold the pcakages of interest based on
# <packages file name>. 
#
# Post condition is to execute dbtest.py to perform the SQL join of
# the tables to get the list of which CVE affects each software package
# referenced in the input file <packages file name>.
#

from __future__ import print_function
import argparse
from os import listdir
from os.path import isfile, join
import zipfile
import json
import sqlite3

"""
Command Line Interface for the CVE lookup.
"""
parser = argparse.ArgumentParser(description="Lookup known vulnerabilities from yocto/RPM/SWID in the CVE")
parser.add_argument("packages", help="The list of packages to run through the lookup", type=argparse.FileType('r', encoding='UTF-8'))
parser.add_argument("-a", "--fail", help="Severity value [0-10] over which it will be a FAILURE", type=float, default=3)
parser.add_argument("-i", "--ignore_file", help="""A File containing a new-line delimited list of specific CVE's to ignore
 (e.g.  CVE-2015-7697 ) . These CVE's will show up as skipped in the report""", type=argparse.FileType('r', encoding='UTF-8'))
# Input argument processing
args = parser.parse_args()

###################################################################
# create a "list" called ignore_list
# elements to ignore are stored in "ignore_list" object.
###################################################################
ignore_list = {}
ignored_control_lookup = {}
if args.ignore_file is not None:
    # first column is CVE, 2nd column is human readable description of control taken
    # eg: CVE-2015-7696 , Device shall never allow decompression of arbitrary zip files
    iterator = 0
    for line in args.ignore_file:
        if line.find("#") == -1: # ignore lines beginning with a hash character
            cols = line.split(",") # split on ,
            if len(cols) > 0:
                cve_id = cols[0].strip()
                cve_control = "N/A"
                if len(cols) > 1:
                    cve_control = cols[1]
                # add them to the list
                ignore_list[iterator] = { "ignore_list" : cve_id } # Entries to ignore stored here
                iterator += 1
                ignored_control_lookup[cve_id] = cve_control


###################################################################
#
# Main
#
# will hold entry triplets from the user provided input file called "packages"
# each elemenet has a vendor-package-version format including the "-" dash
###################################################################
my_final_set = set()
my_final_list = []
#
# will hold entry triplets from the user provided input file called "packages"
# each elemenet has a vendor-package-version format including the "-" dash
package_set = set(open(str(args.packages.name),'r').read().split())
#convert to a dictionary
package_dict = dict()
for element in iter(package_set):    
    package_dict[element] = { "nist_json_cve_entry" : element }
# endfor

# Open the file containing the SQL database.
files = [f for f in listdir("dbs/") if f.endswith('.zip.db')]

for db_filename in files:
    db_filename_with_path = "./dbs/" + db_filename
    print(db_filename_with_path)
    with sqlite3.connect(db_filename_with_path) as conn:
        # Change the package_table to the value in args.packages.name
        CREATE_Statement = "" + "CREATE TABLE IF NOT EXISTS " + args.packages.name + " (nist_json_cve_entry varchar(100) );" + ""
        # print(CREATE_Statement)
        conn.execute(CREATE_Statement)

        # Insert each entry from json into the table.
        keys = ["nist_json_cve_entry"]
        for entry in package_dict:
            # This will make sure that each key will default to None
            # if the key doesn't exist in the json entry.
            values = [package_dict[entry].get(key, None) for key in keys]
            # print("insert this value into database " + str(values))
            # Execute the command and replace '?' with the each value
            # in 'values'. DO NOT build a string and replace manually.
            # the sqlite3 library will handle non safe strings by doing this.
            INSERT_Statement = "" + "INSERT INTO " + args.packages.name + " VALUES( ? );" + ""
            conn.execute(INSERT_Statement, values)
            conn.commit()
        # endfor
    conn.close()
    print("Table is built")
    
    with sqlite3.connect(db_filename_with_path) as conn:
        # Change the package_table to the value in args.packages.name
        CREATE_Statement = "" + "CREATE TABLE IF NOT EXISTS " + args.packages.name + "_ignore" +  " (ignore_list varchar(100) );" + ""
        # print(CREATE_Statement)
        conn.execute(CREATE_Statement)

        # Insert each entry from json into the table.
        keys = ["ignore_list"]
        for entry in ignore_list:
            # This will make sure that each key will default to None
            # if the key doesn't exist in the json entry.
            values = [ignore_list[entry].get(key, None) for key in keys]
            # print("insert this value into database " + str(values))
            # Execute the command and replace '?' with the each value
            # in 'values'. DO NOT build a string and replace manually.
            # the sqlite3 library will handle non safe strings by doing this.
            INSERT_Statement = "" + "INSERT INTO " + args.packages.name + "_ignore" + " VALUES( ? );" + ""
            conn.execute(INSERT_Statement, values)
            conn.commit()
        # endfor
    conn.close()
    print("Ignore table is built")

print("All done")        
exit
