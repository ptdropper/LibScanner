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

parser = argparse.ArgumentParser(description="Lookup known vulnerabilities from yocto/RPM/SWID in the CVE."+
                                             " Output in JUnit style XML where a CVE = failure")
parser.add_argument("packages", help="The list of packages to run through the lookup", type=open)
# for JSON the directory name is fixed. TODO. parser.add_argument("db_loc", help="The folder that holds the CVE xml database files", type=str)
# Only supporting rpm format for now. TODO. parser.add_argument("-f", "--format", help="The format of the packages", choices=["swid","rpm",'yocto'], default="rpm")
parser.add_argument("-a", "--fail", help="Severity value [0-10] over which it will be a FAILURE", type=float, default=3)
parser.add_argument("-i", "--ignore_file", help="""A File containing a new-line delimited list of specific CVE's to ignore
 (e.g.  CVE-2015-7697 ) . These CVE's will show up as skipped in the report""", type=open)

args = parser.parse_args()

from cve_lookup_json import *
#
# create a "set" called ignore_list
# elements to ignore are stored in "ignore_list" object.
ignore_list = set()
ignored_control_lookup = {}
if args.ignore_file is not None:
    # first column is CVE, 2nd column is human readable description of control taken
    # eg: CVE-2015-7696 , Device shall never allow decompression of arbitrary zip files
    for line in args.ignore_file:
        cols = line.split(",") # split on ,
        if len(cols) > 0:
            cve_id = cols[0].strip()
            cve_control = "N/A"
            if len(cols) > 1:
                cve_control = cols[1]
            # add them to the list
            ignore_list.add(cve_id)  # Entries to ignore stored here
            ignored_control_lookup[cve_id] = cve_control

# num_cves = sum(len(x) for x in cves.values())
# num_failed_cves = sum(len([e for e in x if (e['@name'] not in ignore_list and float(e['@CVSS_score']) >= args.fail)]) for x in cves.values())

# print the xml header
# print('<?xml version="1.0" encoding="UTF-8" ?>')
# print('<testsuite id="CVE TEST" name="CVE TEST" tests="{0}" failures="{1}">'.format(num_cves, num_failed_cves))
#for package_name, info in cves.iteritems():

    #for e in info:
        #print('<testcase id="{0}" name="{0}" classname="{1}" time="0">'.format(e['@name'], package_name))
        #try:
            ## always warn, but fail if we're above the failure threshold
            #sev = "failure" if float(e['@CVSS_score']) >= args.fail else "warning"

            #try:
                #description = e['desc']['descript']['#text']
            #except:
                #description = ""

            ## mark any CVEs in the ignore_list as skipped
            #if e['@name'] in ignore_list:
                #sev = "skipped"
                ## append the mitigating control
                #description += "\n\n Controlled by: " + ignored_control_lookup[e['@name']]

            ##print("<{0}> {6} ({1}) - {2} \n\n {3} {4} {5} </{0}>".format(sev, e['@CVSS_score'], description,
            ##                                                       e['@type'], "Published on: " + e['@published'],
            ##                                                       NIST_URL+e['@name'], e['@severity']))
        #except Exception as e:
            #print('<error>{0}</error>'.format(str(e)))

        #print('</testcase>')

#print("</testsuite>")

###################################################################

from os import listdir
from os.path import isfile, join
import zipfile
import json

# will hold entry triplets from the input file called "packages"
package_list = frozenset(open(args.packages.name,'r').read().split()) 

json_cve_set = set() # will hold json cve entries for searching only
json_cve_list = []   # list of json cve entries for output

files = [f for f in listdir("nvd/") if isfile(join("nvd/", f))]
files.sort()
for file in files:
    archive  = zipfile.ZipFile(join("nvd/", file), 'r')
    jsonfile = archive.open(archive.namelist()[0])
    cve_dict = json.loads(jsonfile.read())

    print("CVE_data_timestamp: "    + str(cve_dict['CVE_data_timestamp']))
    print("CVE_data_version: "      + str(cve_dict['CVE_data_version']))
    print("CVE_data_format: "       + str(cve_dict['CVE_data_format']))
    print(" ")

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
                # TODO edit the hard coded zero to a proper iteration
                if len(cve_dict['CVE_Items'][cveiterator]['cve']['affects']['vendor']['vendor_data'][0]['product']['product_data'][productnameiterator]['version']['version_data']) > 0 :
                   # TODO edit the hard coded zero to a proper iteration
                   totalversionrange = len(cve_dict['CVE_Items'][cveiterator]['cve']['affects']['vendor']['vendor_data'][0]['product']['product_data'][productnameiterator]['version']['version_data'])
                   
                   for version_iterator in range(0, totalversionrange):
                      # TODO edit the hard coded zero to a proper iteration
                      my_version = str(cve_dict['CVE_Items'][cveiterator]['cve']['affects']['vendor']['vendor_data'][0]['product']['product_data'][productnameiterator]['version']['version_data'][version_iterator]['version_value'])
                      json_cve_entry = my_vendor_name + "-" + my_product_name + "-" + my_version
                      json_cve_set.add(json_cve_entry)
                      
                      json_cve_list.append(json_cve_entry + '\n' + my_current_cve_description + '\n' + my_current_cve)
                      #print("json_cve_entry is " + json_cve_entry)
    jsonfile.close()

    my_intersection_set = set()
    my_intersection_set = json_cve_set.intersection(package_list)    
    print("my_intersection_set is " + str(my_intersection_set))
        
    for my_intersection_set_iterator in range(0,len(my_intersection_set)):
        thing = my_intersection_set.pop()
        #print("thing is " + str(thing))
        Output = list(filter(lambda x:thing in x, json_cve_list))
        output_length = len(Output)
        for outputs_iterator in range(0,output_length):
            print(Output.pop())        
            output_str = str(Output).strip('[]') 
            print(output_str)
            print('\n')
    
    # 
    # For each item found in my_intersection_set report the CVE_ID and description.
    #

