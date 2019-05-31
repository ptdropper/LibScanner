NIST CVE library search engine.

Input: 	YOUR list of your software packages 
	YOUR list of CVE identifiers to ignore
	NIST provided CVE JSON files 

This tool will use your list of project packages to search thousands 
of current NIST CVE entries to find known issues.
Knowledge is half the battle, so use this to automate the search for 
software items that could have outstanding issues. 

How does it work? It is a python script to search a set of JSON input files from NIST.
Your list of software modules is the search criteria for parsing the content from NIST.

Python data structures including "sets" and "lists" manage creating a 
database if issues, a database of your packages, and performing a set-intersection of 
the two data sets. The resulting output is a set of CVE issues that apply to your 
specific project packages.
 
The script download_json.xml gathers an updated database from NIST
and stores it in ./nvd/. These are zip files that are expanded by the scripts.

to manage the data. Here is an example:
   ./json_cve_parser.py ./my_input_sbom_list -i ./my_ignore_list

The script that does the work is json_cve_parser.py.
The input file of project packages is my_input_sbom_list
The input file of CVE entries to ignore is my_ignore_list

The results are sent to standard output so a front end script is helpful, for
example see scan_for_vulnerabilities_json.sh


