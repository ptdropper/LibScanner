%time%

rm dbs/*.db
rm spa*_output*.txt

echo Building the database from NIST. This takes time.
python ./nist_cve_1.1.py

echo Checking Space Space Com 2
python ./json_cve_parser.py spacecom2_input -i spacecom2_ignore_list

echo Checking Space Com WiFi Lite
python ./json_cve_parser.py spacecom_input  -i spacecom_ignore_list

echo Checking Space Com 3
python ./json_cve_parser.py space_com_3_input -i space_com_3_ignore_list


echo Building output files
python ./dbtest.py
python sort_output.py spacecom2_input_output.txt
python sort_output.py spacecom_input_output.txt
python sort_output.py space_com_3_input_output.txt

%time%

exit