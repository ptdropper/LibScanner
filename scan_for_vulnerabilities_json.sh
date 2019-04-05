# start the process of looking for common vulnerabilities.

# step 1 download data from NIST
echo Download vulnerability data from NIST
./download_xml_json.sh
# If an error, then send a message out that the download failed

echo Setting up python environment
# Step 2 prepare a local python environment 
source bin/activate

output=D:/CVE_Results/${BUILD_NUMBER}
mkdir -p ${output}

echo Checking Space Com WiFi Lite and Space Com 2
# Step 3 check the spacecom project for CVE issues, store the results in a file in the ./spacecom directory
./check_spacecom_json.sh  >  ${output}/spacecom_`date +%F_%T`.xml

echo Checking DoseTrac and DoseLink vulnerabilities
# Step 4 check the dosetrack project for CVE issues, store the results in a file in the ./dosetraclink directory
./check_dosetrack_json.sh >  ${output}/dosetraclink_`date +%F_%T`.xml

echo Checking Space Com 3
# Step 3 check the spacecom project for CVE issues, store the results in a file in the ./spacecom directory
./check_com_3_json.sh  >  ${output}/space_com_3_`date +%F_%T`.xml


# end

exit
