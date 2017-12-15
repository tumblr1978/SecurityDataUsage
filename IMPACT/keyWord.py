#Muwei Zheng
#
#1. Takes one parameter, the folder of files that we need to extract
#   keywords from files inside it
#2. The out put will be a csv file list all filenames and their key words.

import sys, helper
import rake, operator

#read file
files, header = helper.readCSV('./request/requestApproved.csv')

reqIndex = header.index('reason')
userIndex = header.index('idUser')
orgIndex = header.index('orgType')

if reqIndex == -1:
    print "can't find column 'reason"
    sys.exit(1)


#method to extract keyword:
def extractKeyWords(string):
    rake_object = rake.Rake("SmartStoplist.txt", 3,3,1)
    #rake_object = rake.Rake("SmartStoplist.txt")
    keywords = rake_object.run(string)
    return keywords


#Process files, extract key words
processed = set()
out = []

orgMap = {'Academia':'',
          'Commercial':'',
          'Foreign':'',
          'Governmental':'',
          'Private Sector':''}
for f in files:
    text = f[reqIndex]
    if not text.endswith('.'):
        text += '.'
    user = f[userIndex]
    org = f[orgIndex]
    unique = (text, user)
    if unique not in processed:
        orgMap[org] += text

for org in orgMap.keys():
    text = orgMap[org]
    keywords = extractKeyWords(text)
    keywords = ','.join([x[0] for x in keywords])
    out.append([org, keywords])


#write file
helper.writeCSV('./keyWordExtraction/testoutCombined.csv', out)
