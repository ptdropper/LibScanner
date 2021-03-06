from __future__ import print_function

from os import listdir
import os
import argparse
from itertools import islice

parser = argparse.ArgumentParser(description='Sort CVE file.')
parser.add_argument('input_file', help='input file name')
args = parser.parse_args()

outputfile = open("spacecom_cve_output.txt",'w')
with open(str(args.input_file),'r') as filehandle:
	for line in islice(filehandle,0,None):
		cveid = line.split('-')
		# 2009 1234    convert to 2,009,001,234   2009*1,000,000 + id
		cveidnum = (int(cveid[1]) * 1000000) + int(cveid[2])		
		mythreelines = str(cveidnum) + '~' + str(filehandle.readline().replace('\n', '~')) + str(filehandle.readline().replace('\n', '~'))
		outputfile.write(mythreelines)
		outputfile.write('\n')
filehandle.close()
outputfile.close()

outputfile = open("spacecom_output_1.txt",'w')
with open('spacecom_cve_output.txt', 'r') as r:
	for line in sorted(r):
		#print(line, end='')        
		outputfile.write(line)        
outputfile.close()        

outputfilename = str(args.input_file) + "_sorted.txt"
outputfile = open(outputfilename,'w')
with open('spacecom_output_1.txt', 'r') as r:
	for line in r:        
		outputlines = line.split('~')
		#Restore the formatted CVE identifier structure
		yearval = int(outputlines[0])//1000000
		idval =  int(outputlines[0]) - ((int(outputlines[0])//1000000 ) * 1000000)
		
		outputfile.write("CVE-" + str(yearval) + '-' + str("%04d"%(idval)) + '\n')
		outputfile.write(outputlines[1] + '\n')
		outputfile.write(outputlines[2] + '\n')
		
outputfile.close()
os.remove('spacecom_output_1.txt')
os.remove('spacecom_cve_output.txt')
