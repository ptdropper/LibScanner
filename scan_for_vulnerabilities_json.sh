# start the process of looking for common vulnerabilities.

# step 1 download data from NIST
# TEMPORARY: echo Download vulnerability data from NIST
# TEMPORARY: ./download_xml_json.sh
./download_xml_json.sh
# If an error, then send a message out that the download failed

#echo Setting up python environment
# Step 2 prepare a local python environment 
# TEMPORARY: source bin/activate

echo Building the database from NIST. This takes time.
python3 ./nist_cve_1.1.py

echo Checking Space Space Com 2
python3 ./json_cve_parser.py spacecom2_input -i spacecom2_ignore_list

echo Checking Space Com WiFi Lite
python3 ./json_cve_parser.py spacecom_input  -i spacecom_ignore_list

echo Checking Space Com 3
python3 ./json_cve_parser.py space_com_3_input -i space_com_3_ignore_list

#echo Checking DoseTrac and DoseLink vulnerabilities
#python3 ./json_cve_parser.py dosetracklink.input -i ignorecvelist

echo Building output files
python3 ./dbtest.py
python sort_output.py spacecom2_input_output.txt
python sort_output.py spacecom_input_output.txt
python sort_output.py space_com_3_input_output.txt

exit
