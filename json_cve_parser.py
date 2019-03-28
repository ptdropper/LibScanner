#!/usr/bin/env python
#
# Copied from https://avleonov.com/2017/10/03/downloading-and-analyzing-nvd-cve-feed/
# Special thanks to Alexander V. Leonov for the code below to gather and parse the CVE dictionary
#
# this program expects a .zip file in the directory nvd/ for use as the
# NIST produced list of vulnerabilitys in json format.
#
# Execute: json_cve_parser.py
# Expect:  a data dump of all the CVE's with the three fields sent to standard output:
#             CVE-IDENTIFIER
#             Text description of the issue
#             Version strings for this issue.
# Input data file contains the triplet "vendor-product-version" with dashes.
# Must do a match on all 3 to decide to report the CVE.
# Then make an output format decision if the specific CVE is also found in the ignore list.
#
# Example microsoft-home_server-2003
# search for a match on the example "php-php-5.4.3"
#
########################################################################
from __future__ import print_function
"""
Command Line Interface for the CVE lookup.
"""
import argparse
from os import listdir
from os.path import isfile, join
import zipfile
import json

parser = argparse.ArgumentParser(description="Lookup known vulnerabilities from yocto/RPM/SWID in the CVE")
parser.add_argument("packages", help="The list of packages to run through the lookup", type=open)
parser.add_argument("-a", "--fail", help="Severity value [0-10] over which it will be a FAILURE", type=float, default=3)
parser.add_argument("-i", "--ignore_file", help="""A File containing a new-line delimited list of specific CVE's to ignore
 (e.g.  CVE-2015-7697 ) . These CVE's will show up as skipped in the report""", type=open)
# Input argument processing
args = parser.parse_args()

# create a "set" called ignore_set
# elements to ignore are stored in "ignore_set" object.
ignore_list = {}
ignored_control_lookup = {}
if args.ignore_file is not None:
    # first column is CVE, 2nd column is human readable description of control taken
    # eg: CVE-2015-7696 , Device shall never allow decompression of arbitrary zip files
    iterator = 0
    for line in args.ignore_file:
        cols = line.split(",") # split on ,
        if len(cols) > 0:
            cve_id = cols[0].strip()
            cve_control = "N/A"
            if len(cols) > 1:
                cve_control = cols[1]
            # add them to the list
            ignore_list[iterator] = cve_id  # Entries to ignore stored here
            iterator += 1
            ignored_control_lookup[cve_id] = cve_control

###################################################################
# https://www.geeksforgeeks.org/split-string-substrings-using-delimiter/
#
# This code is contributed by
# Surendra_Gangwar
#
# Python 3 implementation to split string
# into substrings on the basis of delimiter
# and return the substrings after split
#
# Input: string, delimiter
# Output: sub strings split by delimiter
#
def splitStrings(st, dl):
    word = ""

    # to count the number of split strings
    num = 0

    # adding delimiter character at
    # the end of str
    st += dl

    # length of str
    l = len(st)

    # traversing str from left to right
    substr_list = []
    for i in range(l):

        # if str[i] is not equal to the
        # delimiter character then accumulate
        # it to word
        if (st[i] != dl):
            word += st[i]

        else:

            # if word is not an empty string,
            # then add this word to the array
            # substr_list[]
            if (len(word) != 0):
                substr_list.append(word)

            # reset word
            word = ""

    # return the splitted strings
    return substr_list
    
###################################################################
# Contributed by Utkarsh Trivedi. 
# https://www.geeksforgeeks.org/compare-two-version-numbers/
# Method to compare two versions.
#
# Input: version string 1, version string 2
# Output: Return 1 if v2 is smaller, 
#         -1 if v1 is smaller,, 
#         0 if equal 
#
def versionCompare(v1, v2): 
      
    # This will split both the versions by '.' 
    arr1 = v1.split(".") 
    arr2 = v2.split(".") 
  
    # Initializer for the version arrays 
    i = 0 
      
    # We have taken into consideration that both the 
    # versions will contains equal number of delimiters 
    while(i < len(arr1)): 
          
        # Version 2 is greater than version 1 
        if int(arr2[i]) > int(arr1[i]): 
            return -1
          
        # Version 1 is greater than version 2 
        if int(arr1[i]) > int(arr2[i]): 
            return 1
  
        # We can't conclude till now 
        i += 1
          
    # Both the versions are equal 
    return 0
    
###################################################################
#
# Main
#
# will hold entry triplets from the input file called "packages"
package_set = frozenset(open(args.packages.name,'r').read().split()) 

json_cve_set = set() # will hold json cve entries for searching only
json_cve_list = []   # list of json cve entries for output
header_printed = False
my_final_set = set()
my_final_list = []

files = [f for f in listdir("nvd/") if isfile(join("nvd/", f))]
files.sort()
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

    totalcvecount = int(str(cve_dict['CVE_data_numberOfCVEs']))
    for cveiterator in range(0, totalcvecount):    
       if len(cve_dict['CVE_Items'][cveiterator]['cve']['affects']['vendor']['vendor_data']) > 0 :
           totalproductnamecount = len(cve_dict['CVE_Items'][cveiterator]['cve']['affects']['vendor']['vendor_data'][0]['product']['product_data'])
           for product_iterator in range(0,totalproductnamecount):
              my_product_name = str(cve_dict['CVE_Items'][cveiterator]['cve']['affects']['vendor']['vendor_data'][0]['product']['product_data'][0]['product_name'])

           my_vendor_name = str(cve_dict['CVE_Items'][cveiterator]['cve']['affects']['vendor']['vendor_data'][0]['vendor_name'])
           my_current_cve = str(cve_dict['CVE_Items'][cveiterator]['cve']['CVE_data_meta']['ID'])
           my_current_cve_description = str(cve_dict['CVE_Items'][cveiterator]['cve']['description']['description_data'][0]['value'])
           
           #
           # iterate over found version values to fill the set json_cve_set with 
           # data of the vendor-product-version triplet
           #
           for productnameiterator in range(0, totalproductnamecount):
                if len(cve_dict['CVE_Items'][cveiterator]['cve']['affects']['vendor']['vendor_data'][0]['product']['product_data'][productnameiterator]['version']['version_data']) > 0 :
                   totalversionrange = len(cve_dict['CVE_Items'][cveiterator]['cve']['affects']['vendor']['vendor_data'][0]['product']['product_data'][productnameiterator]['version']['version_data'])
                   
                   for version_iterator in range(0, totalversionrange):
                      my_version = str(cve_dict['CVE_Items'][cveiterator]['cve']['affects']['vendor']['vendor_data'][0]['product']['product_data'][productnameiterator]['version']['version_data'][version_iterator]['version_value'])
                      json_cve_entry = my_vendor_name + "-" + my_product_name + "-" + my_version
                      json_cve_set.add(json_cve_entry)
                      
                      json_cve_list.append(json_cve_entry + ';' + my_current_cve_description + ';' + my_current_cve)                      
    jsonfile.close()

    my_intersection_set = set()
    my_intersection_set = json_cve_set.intersection(package_set)
    my_sub_string = []
    # 
    # For each item found in my_intersection_set create a report with 
    # the CVE_ID and description.        
    #
    for my_intersection_set_iterator in range(len(my_intersection_set)):
        possible_cve_match = my_intersection_set.pop()
        # Convert each entry into a list object for output formatting.
        Output = list(filter(lambda x:possible_cve_match in x, json_cve_list))        
        for outputs_iterator in range(len(Output)):
            output_str = str(Output[outputs_iterator]).strip('[]')
            my_sub_strings = splitStrings(output_str, ';')
            #
            # Version number check since the set.intersection() returns an inexact match.
            #
            pcm_version = str(possible_cve_match).split('-')
            mss_version = my_sub_strings[0].split('-')
            if pcm_version[2] == mss_version[2]:            
                # print(my_sub_strings[2] + " " + my_sub_strings[0])
                # If the issue is not in the ignore list, then mark it with a warning
                heading = "<warning> "
                for ignored_cve_iter in range(len(ignore_list)):
                    if my_sub_strings[2] == ignore_list[ignored_cve_iter]:
                        heading = "<skipped> "                
                #
                # Store the output triplet CVE ID, package name, description in a list so 
                # the list can be sorted and then only unique entries are preserved.
                # list { 'cve id' 'package name' 'description' }
                my_final_list.append(my_sub_strings[2] + ";" + my_sub_strings[0] + ";" + heading + my_sub_strings[1])
        #
    # 
# All files processed at this point
#               
my_final_list.sort()
my_final_set = set(my_final_list)
my_final_list = sorted(my_final_set)
for x in range(len(my_final_list)):
    list_element = my_final_list[x]
    my_sub_strings = splitStrings(str(list_element), ';')
    print(my_sub_strings[0]) 
    print(my_sub_strings[1])
    print(my_sub_strings[2])
    print()
    
# EOF
