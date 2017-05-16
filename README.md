A simple python script called cli.py to parse your provided list of software against a database of known software
vulnerabilities.
The vulnerabilities are the NIST provided CVE issues. The script download.xml gathers an updated database from NIST
and stores it locally.
Then run the cli.py script with your software to parse through the entire database.
The output is an XML file showing the matching CVE's.

Fair warning it uses some specific python libraries so your are BEST served by creating a local directory with
a virtual python envionrment to protect your machine. Trust me.

To get this working you will need to download a copy of the NVD here: https://nvd.nist.gov/download.cfm#CVE_FEED
and put the xml files in the dbs folder.

run package-cve-lookup -h for more information on using the command line interface.
