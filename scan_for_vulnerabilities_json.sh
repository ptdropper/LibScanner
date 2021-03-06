# start the process of looking for common vulnerabilities.

# step 1 download data from NIST
echo Download vulnerability data from NIST
./download_xml_json.sh
# If an error, then send a message out that the download failed

output=D:/CVE_Results/${BUILD_NUMBER}
mkdir -p ${output}

echo clean up existing database files
rm ./nvd/*.db

echo Building the database from NIST. This takes time.
C:/Python38/python.exe ./nist_cve_1.1.py

echo Checking Space Space Com 2 WB45
C:/Python38/python.exe ./json_cve_parser.py spacecom2_wb45_input -i spacecom2_wb45_ignore_list

echo Checking Space Space Com 2
C:/Python38/python.exe ./json_cve_parser.py spacecom2_input -i spacecom2_ignore_list

echo Checking Space Com WiFi Lite
C:/Python38/python.exe ./json_cve_parser.py spacecom_input  -i spacecom_ignore_list

echo Checking Space Com 3
C:/Python38/python.exe ./json_cve_parser.py space_com_3_input -i space_com_3_ignore_list

echo Checking Space Plus
C:/Python38/python.exe ./json_cve_parser.py space_plus_input

#echo Checking DoseTrac and DoseLink vulnerabilities
#python3 ./json_cve_parser.py dosetracklink.input -i ignorecvelist

echo Building output files
C:/Python38/python.exe ./dbtest.py
C:/Python38/python.exe sort_output.py spacecom2_wb45_input_output.txt
C:/Python38/python.exe sort_output.py spacecom2_input_output.txt
C:/Python38/python.exe sort_output.py spacecom_input_output.txt
C:/Python38/python.exe sort_output.py space_com_3_input_output.txt
C:/Python38/python.exe ./sort_output.py space_plus_input_output.txt

# cp C:/cve_scan/nvd/*.db $output
cp c:/cve_scan/*_sorted.txt $output

exit
