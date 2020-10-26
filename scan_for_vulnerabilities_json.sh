# start the process of looking for common vulnerabilities.

# step 1 download data from NIST
echo Download vulnerability data from NIST
./download_xml_json.sh

# The python executable differs based on build environment.
# MS Windows python executable name
PythonExecutableName=C:/Python38/python.exe
# Linux python executable name
#PythonExecutableName=python3

output=D:/CVE_Results/${BUILD_NUMBER}
mkdir -p ${output}

echo clean up existing database files
rm ./nvd/*.db

echo Building the database from NIST. This takes time.
${PythonExecutableName} ./nist_cve_1.1.py

echo Checking Space Com WiFi Lite
${PythonExecutableName} ./json_cve_parser.py spacecom_input  -i spacecom_input_ignore_list

echo Checking Space Space Com 2 WB45
${PythonExecutableName} ./json_cve_parser.py spacecom2_wb45_input -i spacecom2_wb45_input_ignore_list

echo Checking Space Space Com 2
${PythonExecutableName} ./json_cve_parser.py spacecom2_input -i spacecom2_input_ignore_list

echo Checking Space Com 3
${PythonExecutableName} ./json_cve_parser.py space_com_3_input -i space_com_3_input_ignore_list

echo Checking Space Plus
${PythonExecutableName} ./json_cve_parser.py space_plus_input

#echo Checking DoseTrac and DoseLink vulnerabilities
# ${PythonExecutableName} ./json_cve_parser.py dosetracklink.input -i ignorecvelist

echo Building output files
${PythonExecutableName} ./dbtest.py
echo Sorting spacecom 2
${PythonExecutableName} sort_output.py spacecom2_input_output.txt
echo Sorting spacecom
${PythonExecutableName} sort_output.py spacecom_input_output.txt
echo Sorting space com 3
${PythonExecutableName} sort_output.py space_com_3_input_output.txt
echo Soring space plus
${PythonExecutableName} sort_output.py space_plus_input_output.txt
echo Sorting spacecom2 wb45
${PythonExecutableName} sort_output.py spacecom2_wb45_input_output.txt

cp C:/cve_scan/nvd/*.db     $output
cp c:/cve_scan/*_sorted.txt $output

exit
