Welcome to the [CVE Scanner](https://github.com/ptdropper/CVE-Scanner-for-your-SW-BOM) wiki! 

What is CVE-scanner?
====================
This project provides a way that you can manage the risk inherited by using open source and third party source projects. This provides you with intelligent Software Composition Analysis to identify and reduce risk.

Inputs from your project
========================
The project is a python based NIST-CVE library search engine for use with your own custom Software Bill of Materials (SBOM) input file. This is ideal for projects where you can create a text file of your SBOM as input to the tool. The output will be all CVE identifiers of potential risks. The library from NIST is tens of thousands of entries, and this tool does the work of searching for your specific packages of interest. 

HOW TO:
=======
- Create an ascii text input file holding package names and versions of interest.
- Input data file contains the triplet "vendor-product-version" with dashes.
- Must match on all 3 to decide to report the CVE.
- Lines with a leading hash/pound symbol are ignored.

Example for typical open source packages where there is no vendor so set the vendor value to match the product name.
```sh
libssh-libssh-1.0
linux_kernel-linux_kernel-4.9
microsoft-home_server-2003
php-php-5.4.3
```
Whitelist to ignore specific CVEs
=================================
Next is an optional whitelist file you can create. The whitelist is referred to as the "ignore list" in the python sources. 
The ignore list content is based on your analysis of the reported CVE's affecting your project. As you review CVE descriptions and details you may find that some of the CVEs do not apply in your product. Then copy those entries into the ignore list file and optionally provide some message to yourself to explain why the CVE does not apply. These ignored CVE's will show up with the marking < skipped > in the report so you are aware they have been analyzed.

Example ignore list file content
================================
```sh
##CVE-2015-7697 does not apply because the product does not use feature foo which is the trigger for this issue.
CVE-2015-7697
```

Usage: ./json_cve_parser.py ./my_input_input -i ./my_ignore_list
Example: the shell script "check_spacecom_json.sh" calls 

./json_cve_parser.py ./spacecom_input -i ./spacecom_ignore_list

The parser is json_cve_parser.py, accepts input file, reads each line, searches the database for that triplet, and if that product tripet is related to a CVE number write the CVE number and summary text to the output file. If that CVE is in the ignore list, then indicate that the CVE is marked with the prefix < skipped >.

So there is more to the process as is captured in the script scan_for_vulnerabilities_json.sh. This script is the real entry point for the process which can be run on the command line, in a cron job, or hooked into Jenkins. THe file performs the required database download from NIST, starts a local python environment using the "activate" command, creates a new directory that has a unique incremental build number, and finally calls the shell script "check_spacecom_json.sh" to execute the process.

Jenkins
=======
For a daily build process use the script scan_for_vulnerabilities_json.bat as the hook into your Jenkins build machine. It will call the "scan_for_vulnerablities_json.sh" script in a bash session.

Finally the output directories will continue to grow in number and daily changes to the NIST database will be reflected in the output files in those output directories. One tool to use to verify you can observe changes is to use the Git SCM tool to track every one of the output files. Each day copy the latest over the top of the previous iteration and let the Git diff feature show you what changed. Managing vulnerabilities then means managing these changes.

