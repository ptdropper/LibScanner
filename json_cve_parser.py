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
#
from __future__ import print_function
"""
Command Line Interface for the CVE lookup.
"""
import argparse

parser = argparse.ArgumentParser(description="Lookup known vulnerabilities from yocto/RPM/SWID in the CVE."+
                                             " Output in JUnit style XML where a CVE = failure")
parser.add_argument("packages", help="The list of packages to run through the lookup", type=open)
# parser.add_argument("db_loc", help="The folder that holds the CVE xml database files", type=str)
# parser.add_argument("-f", "--format", help="The format of the packages", choices=["swid","rpm",'yocto'], default="rpm")
parser.add_argument("-a", "--fail", help="Severity value [0-10] over which it will be a FAILURE", type=float, default=3)
parser.add_argument("-i", "--ignore_file", help="""A File containing a new-line delimited list of specific CVE's to ignore
 (e.g.  CVE-2015-7697 ) . These CVE's will show up as skipped in the report""", type=open)

args = parser.parse_args()

from cve_lookup import *
root = parse_dbs(args.db_loc)

errors, packages = get_package_dict(args.packages.read())
cves = get_vulns(packages, root)

# get the ignore list
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
            ignore_list.add(cve_id)
            ignored_control_lookup[cve_id] = cve_control


num_cves = sum(len(x) for x in cves.values())
num_failed_cves = sum(len([e for e in x if (e['@name'] not in ignore_list and float(e['@CVSS_score']) >= args.fail)]) for x in cves.values())

# print the xml header
print('<?xml version="1.0" encoding="UTF-8" ?>')
print('<testsuite id="CVE TEST" name="CVE TEST" tests="{0}" failures="{1}">'.format(num_cves, num_failed_cves))
for package_name, info in cves.iteritems():

    for e in info:
        print('<testcase id="{0}" name="{0}" classname="{1}" time="0">'.format(e['@name'], package_name))
        try:
            # always warn, but fail if we're above the failure threshold
            sev = "failure" if float(e['@CVSS_score']) >= args.fail else "warning"

            try:
                description = e['desc']['descript']['#text']
            except:
                description = ""

            # mark any CVEs in the ignore_list as skipped
            if e['@name'] in ignore_list:
                sev = "skipped"
                # append the mitigating control
                description += "\n\n Controlled by: " + ignored_control_lookup[e['@name']]

            #print("<{0}> {6} ({1}) - {2} \n\n {3} {4} {5} </{0}>".format(sev, e['@CVSS_score'], description,
            #                                                       e['@type'], "Published on: " + e['@published'],
            #                                                       NIST_URL+e['@name'], e['@severity']))
        except Exception as e:
            print('<error>{0}</error>'.format(str(e)))

        print('</testcase>')

print("</testsuite>")

###################################################################

from os import listdir
from os.path import isfile, join
import zipfile
import json

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

    # Input data file 1 contains the triplet "vendor-product-version" with dashes.
    # Must do a match on all 3 to decide to report the CVE.
    # Then make an output format decision if the specific CVE is also found in teh ignore list.
    #
    # Example microsoft-home_server-2003
    # search for a match on the example "php-php-5.4.3"

    totalcvecount = int(str(cve_dict['CVE_data_numberOfCVEs']))
    #for cveiterator in range(0, totalcvecount):
    #
    # TODO restore to the full range of totatlcvecount
    #
    for cveiterator in range(0, 1):
        # if we get a triplet match set match_found to non zero
        match_prodname_found = 0
        match_vendorname_found = 0
        match_version_found = 0

        # cve:CVE_data_meta:ID is the cve number
        my_current_cve = str(cve_dict['CVE_Items'][cveiterator]['cve']['CVE_data_meta']['ID'])
        #print("My current cve is " + str(my_current_cve) )

        # TODO edit the hard coded zero to a proper iteration
        my_current_cve_description = str(cve_dict['CVE_Items'][cveiterator]['cve']['description']['description_data'][0]['value'])
        #print("my_current_cve_description is " + my_current_cve_description)

        # determine the length of the field affects:vendor:vendor_data array
        # display each entry containing "product_name"
        #
        if len(cve_dict['CVE_Items'][cveiterator]['cve']['affects']['vendor']['vendor_data']) > 0 :
           # TODO edit the hard coded zero to a proper iteration
           totalproductnamecount = len(cve_dict['CVE_Items'][cveiterator]['cve']['affects']['vendor']['vendor_data'][0]['product']['product_data'])
           for product_iterator in range(0,totalproductnamecount):
              my_product_name = str(cve_dict['CVE_Items'][cveiterator]['cve']['affects']['vendor']['vendor_data'][0]['product']['product_data'][0]['product_name'])
              print("my_product_name is " + my_product_name)
           if my_product_name == "home_server" :
              match_prodname_found = 1

           my_vendor_name = str(cve_dict['CVE_Items'][cveiterator]['cve']['affects']['vendor']['vendor_data'][0]['vendor_name'])
           if my_vendor_name == "microsoft":
               match_vendorname_found = 1
               print("my_vendor_name is " + my_vendor_name)
               print("My current cve is " + my_current_cve)

           #
           # iterate over found version values
           #
           for productnameiterator in range(0, totalproductnamecount):
                # TODO edit the hard coded zero to a proper iteration
                if len(cve_dict['CVE_Items'][cveiterator]['cve']['affects']['vendor']['vendor_data'][0]['product']['product_data'][productnameiterator]['version']['version_data']) > 0 :
                   # TODO edit the hard coded zero to a proper iteration
                   totalversionrange = len(cve_dict['CVE_Items'][cveiterator]['cve']['affects']['vendor']['vendor_data'][0]['product']['product_data'][productnameiterator]['version']['version_data'])
                   for version_iterator in range(0, totalversionrange):
                      # TODO edit the hard coded zero to a proper iteration
                      my_version = str(cve_dict['CVE_Items'][cveiterator]['cve']['affects']['vendor']['vendor_data'][0]['product']['product_data'][productnameiterator]['version']['version_data'][version_iterator]['version_value'])

                      if my_version == "2003":
                         print("my_version = " + my_version)
                         match_version_found = 1
           if (match_prodname_found == 1 and match_vendorname_found == 1 and match_version_found == 1) :
              print("")
              print("Match found CVE is " + my_current_cve)
              print( my_current_cve_description)
              print("")

        print("")

    # prints out just the first entry for use as an example
    # print(json.dumps(cve_dict['CVE_Items'][0], sort_keys=True, indent=4, separators=(',', ': ')))
    jsonfile.close()
