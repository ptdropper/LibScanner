
from __future__ import print_function
import sqlite3    
from os import listdir
import os
import argparse
from os.path import isfile, join
import zipfile
import json

  
print("Searching database software package names with CVE issues")

files = [f for f in listdir("./dbs") if f.endswith('.zip.db')]
files.sort()
file_index=1
package_table_list = ["spacecom2_wb45_input","spacecom2_input","space_com_3_input","spacecom_input"]


for package_table in package_table_list:
    outputfile = open(package_table + "_output.txt", 'w')
    print()
    print("CVE Issues for the product: " + package_table)
    print("----------------------------------------------------------------")
    for fi in files:
        db_filename_with_path = "./dbs/" + fi
        print(db_filename_with_path)
        with sqlite3.connect(db_filename_with_path) as conn:        
            cmd = "" + "SELECT nist.current_cve_id,nist.nist_json_cve_entry,nist.current_cve_description FROM nist INNER JOIN " + package_table + " ON nist.nist_json_cve_entry LIKE '%' || " + package_table + ".nist_json_cve_entry || '%' ORDER BY nist.nist_json_cve_entry ;" + ""
            cur = conn.execute(cmd)
            res = cur.fetchall()
            conn.commit()            
            my_final_set = set(res)    # unique
            # my_final_list = list(sorted(set(filter(None,res))))
            # my_final_list = res
            my_final_list = list(my_final_set)
            # TypeError '<' not supported between NoneType and str, my_final_list = sorted(my_final_set) # sorted again due to undefined sort in the set()            
            #
            # If there is a table called <product>_ignore then process 
            # the ignored CVE's by prefixing the output with the phrase <skipped>
            #       
            ########################################################################
			# PERFORMANCE tuning by removing the inner for loop. Unwind this somehow.
			########################################################################
            for x in range(len(my_final_list)):
                print(my_final_list[x][0], file=outputfile)
                print(my_final_list[x][1], file=outputfile)
                str2 = str(my_final_list[x][2])
                print("warning " + str(str2.encode(encoding="ascii",errors="ignore")), file=outputfile)

                ## Look for ignored entries and add a prefix if needed
                #cmd2 = "" + "SELECT nist.current_cve_id FROM nist INNER JOIN " + package_table + "_ignore" + " ON nist.current_cve_id = " + package_table +  "_ignore.ignore_list " + " ORDER BY nist.nist_json_cve_entry  ;" + ""
                #cur2 = conn.execute(cmd2)
                #res2 = cur2.fetchall()
                #conn.commit()
                
                #if ( res2 ): 
                    ## ignore CVE matched therefore results are not emtpy                    
                    #print("<skipped> " + str(my_final_list[x][2]), file=outputfile)
                #else :
                    #print("<warning> " + str(my_final_list[x][2]), file=outputfile)
            #file_index+=1

    #endfor
    outputfile.close()
#endfor
