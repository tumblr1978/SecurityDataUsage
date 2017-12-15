#Muwei Zheng
#
#This script takes 3 arguments
#1. The name of input csv file
#2. The column name in the csv file when to process
#3. The out put file name.

import csv, sys
import helper

#handle parameters
inFile = sys.argv[1]
outFile = sys.argv[3]
colName = sys.argv[2]

#input file data
data , header= helper.readCSV(inFile)
#print header

#extract the column we want
ind = header.index(colName)
content = set([(x[ind], x[ind+7]) for x in data])  #need to modify
print 'len set:', len(content)

#clean up each description with stopwords and combine them back to string and output to a txt file
out = []
for entry in content:
    string = entry[0]
    string = set(helper.cleanStopWords(string))
    string = [x for x in string]
    out += string

out =' '.join(out)+'\n'
f = open(outFile, 'w')
f.write(out)
f.close()
