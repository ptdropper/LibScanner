NIST CVE library search engine.
Provide your project's list of software packages, libraries, and any module used to create your product.
This tool will use your list to search tousands of NIST CVE entries to find any known issues.
Knowledge is half the battle, so use this to automate the search for software items that could have outstanding 
issues needed a patch.

How does it wor? It is a simple python script used to parse your provided list of software modules (packages, libraries and so on) 
against a database of known software vulnerabilities.
The vulnerabilities are the NIST provided CVE issues. The script download.xml gathers an updated database from NIST
and stores it locally.
Then run the cli.py script with your software to parse through the entire database.
The output is an XML file showing the matching CVE's.

Fair warning it uses some specific python libraries so your are BEST served by creating a local directory with
a virtual python envionrment to protect your machine. Trust me.

To get this working you will need to download a copy of the NVD here: https://nvd.nist.gov/download.cfm#CVE_FEED
and put the xml files in the dbs folder.

run cve-lookup -h for more information on using the command line interface.

https://askubuntu.com/questions/244641/how-to-set-up-and-use-a-virtual-python-environment-in-ubuntu

Virtual environments offer a way for managing and isolating dependencies on a per-project basis. Moreover, they also avoid the whole sudo pip install situation, which is a security risk as I have explained in https://askubuntu.com/a/802594/15003. The official Python documentation also encourages the use of virtual environments.

The easiest way to create and use virtual environments for both Python 2 and Python 3 is to install virtualenv using apt or apt-get. For each Python project, create a virtualenv and then activate it. Note that the virtualenv is specific for a particular Python version. After activation, use pip to install Python packages as usual regardless of whether you are using Python 2 or 3; there is no need to use pip3 for Python 3. sudo is only used to install virtualenv and is not used with pip, therefore avoiding the aforementioned security risk. The commands to do so are:

sudo apt update
sudo apt install virtualenv
cd ~/desired_directory  # cd to desired_directory
virtualenv venv  # create virtualenv named venv for default system Python, which is Python 2 for Ubuntu
source venv/bin/activate  # activate virtualenv
pip install -U pip  # upgrade pip in case it is outdated
pip install desired_package  # install desired_package

If you would like to create a virtualenv for Python 3, replace virtualenv venv with:

virtualenv venv -p python3

Read more about various bells and whistles for virtualenv at https://virtualenv.pypa.io/en/stable/.

