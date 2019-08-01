Welcome to the [CVE Scanner](https://github.com/ptdropper/CVE-Scanner-for-your-SW-BOM) wiki! 

This project provides a way that you can manage the risk inherited by using open source and third party source projects. This provides you with intelligent Software Composition Analysis to identify and reduce risk.

The project is a python based NIST-CVE library search engine for use with your own custom Software Bill of Materials (SBOM) input file. This is ideal for projects where you can create a text file of your SBOM as input to the tool. The output will be all CVE identifiers of potential risks. The library from NIST is tens of thousands of entries, and this tool does the work of searching for your specific packages of interest. 

HOW TO:
- Create an ascii text input file in the following format:
- Input data file contains the triplet "vendor-product-version" with dashes.
- Must match on all 3 to decide to report the CVE.

Example for a typical open source package where there is no vendor so set the vendor value to match the product name.

libssh-libssh-1.0

linux_kernel-linux_kernel-4.9

microsoft-home_server-2003

php-php-5.4.3


Next is an optional whitelist file you can create. The whitelist is referred to as the "ignore list" in the python sources. 
The ignore list content is based on your analysis of the reported CVE's affecting your project. As you review CVE descritopns and details you may find that some of the CVEs do not apply in your product. Thus copy those entries into the ignore list file and optionally provide some message to yourself to explain why the CVE does not apply. These ignored CVE's will show up with the marking < skipped > in the report so you are aware they have been analyzed.

Example ignore list file content

##CVE-2015-7697 does not apply because the product does not use feature foo which is the trigger for this issue.

CVE-2015-7697
