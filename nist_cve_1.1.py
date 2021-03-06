from __future__ import print_function
from os import listdir
from os.path import isfile, join
import json
import sqlite3
import zipfile
from timeit import default_timer as timer
import time # to check which parts are time consumers



def writeToSQLDB(file, cve_nist_dict ):
    # Open the file containing the SQL database.
    db_filename = "./dbs/nistfile"+ file + ".db"
    print(db_filename)
    time_103 = time.process_time()
    with sqlite3.connect(db_filename) as conn:
        # conn.text_factory = str     
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
            #conn.execute(cmd, [TextValue, TextValue, sqlite3.Binary(current_cve_description)])
            conn.execute(cmd, values)

    conn.commit()
    time_134 = time.process_time()
    #print("134-103 took this amount of time " + str(time_134-time_103))
# end of writeToSQLDB


# The databasae contains the labels true and false which needs a numeric value.
true=True
false=False

#
# --------------------------------------------------------------------
# Process the NIST database files into the following format.
#
# Output is: nist_json_cve_list[]
# Each element of nist_json_cve_list contains:
#
#     [0] vendor-product-version many values for on cve value
#     [1] cve text description   one value for this cve value
#     [2] cve value              one value for this cve value
#
# --------------------------------------------------------------------
#
# A single CVE-ID will have N descriptions
#   It will have X nodes
#      Each node will have Y cpe_match values
#


header_printed = False
nist_json_cve_list = []     # NIST provided json cve entries for output
FIELD_SPLIT_CHARACTER = '|'

files = [f for f in listdir("nvd/") if f.endswith('.zip') and isfile(join("nvd/", f))]
files.sort()
nist_json_matched_list = list()
########################################################################
# For each json file
########################################################################
for file in files:
    archive  = zipfile.ZipFile(join("nvd/", file), 'r')
    jsonfile = archive.open(archive.namelist()[0])
    issue_dict = json.loads(jsonfile.read().decode('utf-8'))
    print("Processing file " + file)

    if header_printed == False:
        print("CVE_data_timestamp: "    + str(issue_dict['CVE_data_timestamp']))
        print("CVE_data_version: "      + str(issue_dict['CVE_data_version']))
        print("CVE_data_format: "       + str(issue_dict['CVE_data_format']))
        print(" ")
        header_printed = True

    # Check that the CVE_data_version is 4.0  TODO
    # cvedataversion = str(cve_dict['CVE_data_version'])
    # cvedataversion = '4.0'
    #if ( cvedataversion.find("4.0") == 0 ) :
    #   print("CVE Schema version is unknown, exiting")
    #   exit

    cve_nist_dict = dict()
    cve_nist_dict_iter=0
    nist_json_cve_entry_list = list()
    totalcvecount = int(str(issue_dict['CVE_data_numberOfCVEs']))
    print("totalcvecount is " + str(totalcvecount))

    ########################################################################
    # For each CVE in this JSON file
    ########################################################################
    for CVE_ItemsIter in range (0, totalcvecount):
        time_52 =  timer() # performance check tool

        # TODO gather any operator such as OR AND
        # TODO gather cpe matches looking at value of versionEndIncluding
        # and cpe23Uri parsed out into the manufacturer:productName
        cveIssueDict    = issue_dict['CVE_Items'][CVE_ItemsIter]        
        # Only need the initial description for the summary report so use index value 0 (zero)
        descriptionIndex=0
        theDescription = cveIssueDict['cve']['description']['description_data'][descriptionIndex]['value']                        
        cveId           = cveIssueDict['cve']['CVE_data_meta']['ID']
        # DEBUG print(theDescription)
        # DEBUG print ("CVE ID: " + cveId)
        
        #########################################################################        
        # surprise that some entries contain zero data so special handling below.
        # if there are no nodes then we skip processing the invalid data.    
        if (len(cveIssueDict['configurations']['nodes']) != 0) :
            
            configurationNodeLen = len(cveIssueDict['configurations']['nodes'])            
            for configurationNode in range(0, configurationNodeLen):    
            
                if ( 'children' in cveIssueDict['configurations']['nodes'][configurationNode].keys() ):
                    # TODO set the array index to a non-zero value
                    cve_version     = cveIssueDict['configurations']['nodes'][configurationNode]['children'][0]['cpe_match'][0]['cpe23Uri']
                else :
                    # TODO set the array index to a non-zero value
                    try:
                        # CVE-2018-10511 does not have the entity cpe_match as of July 2 2020. I think this is wrong so here
                        # we have special handling for this error.
                        if ( 'cpe_match' in cveIssueDict['configurations']['nodes'][configurationNode].keys() ):
                            cve_version     = cveIssueDict['configurations']['nodes'][configurationNode]['cpe_match'][0]['cpe23Uri']
                    except: 
                        print ("Error with " + str(cveId) + str(cveIssueDict['configurations']['nodes'][configurationNode]))
                        cve_version = "unknown:unknown:unknown:unknown:unknown:unknown"

                split_cpe23uri = cve_version.split(':')
                nist_json_cve_entry = split_cpe23uri[3] + "-" + split_cpe23uri[4] + "-" + split_cpe23uri[5]
                # DEBUG print(split_cpe23uri[3] + "-" + split_cpe23uri[4] + "-" + split_cpe23uri[5])                
                    
                cve_nist_dict[cve_nist_dict_iter] = {\
                    "current_cve_id"          : cveId,\
                    "nist_json_cve_entry"     : nist_json_cve_entry,\
                    "current_cve_description" : theDescription\
                }
                #print(cve_nist_dict[cve_nist_dict_iter]['current_cve_id'] + " " + cve_nist_dict[cve_nist_dict_iter]['nist_json_cve_entry'] + " " + str(cve_nist_dict_iter))
                cve_nist_dict_iter+=1
            # End for(nist_json_cve_entry_iter)
        # endif len(cveIssueDict)
        
    # DEBUG print(cve_nist_dict[0]['current_cve_id'] + " " + cve_nist_dict[0]['nist_json_cve_entry'] + " " + cve_nist_dict[0]['current_cve_description'])
    # DEBUG lastcveindex = len(cve_nist_dict)-1
    # DEBUG print(cve_nist_dict[lastcveindex]['current_cve_id'] + " " + cve_nist_dict[lastcveindex]['nist_json_cve_entry'] + " " + cve_nist_dict[lastcveindex]['current_cve_description'])
    
    #end for(nist_json_cve_entry_iter)
    # print("Reject count = " + str(rejectCount))
    writeToSQLDB(file, cve_nist_dict)
    cve_nist_dict.clear()
    print("Count of entries added to db " + str(cve_nist_dict_iter))

# End of this NVD file

time_97 =  timer()
# print(time_97 - time_52)

