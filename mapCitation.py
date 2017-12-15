#Muwei Zheng
# two parameters: csv file name, citationInfo file name

import csv, sys, re

# Create parameters
# papersInfo: list store the papersInfo
# header
# cites: dict store the citationInfo
papersInfo = []
header = []
citesInfo = []
cites = {}
error = []


#helper method to clean up the text
def clean(string):
    string = re.sub('[^0-9a-zA-Z]+', ' ', string)
    string = re.sub(' +', ' ', string)
    return string.strip().lower()


#Open the csv file and the citation file
with open(sys.argv[1], 'rU') as cf:
    rd = csv.reader(cf, delimiter=',', quotechar='"')
    header = rd.next()
    for r in rd:
        papersInfo.append(r)

f = open(sys.argv[2], 'r')
citesInfo = f.readlines()
f.close()

#Mapping citations
for cite in citesInfo:
    if not ' was cited by ' in cite:
        continue
    parts = cite.split(' was cited by ')
    title = parts[0]
    title = clean(title)
    citeNum = parts[1].split()[0]
    cites[title] = citeNum


ind = header.index('citeNum')
for i in range(len(papersInfo)):
    paper = papersInfo[i]
    title = clean(paper[1])
    citeNum = paper[ind]
    if citeNum != 'NA' and citeNum != '':
        continue

    try:
        num = cites[title]
        if num == 'this':
            num = 0
        papersInfo[i][ind] = num
    except:
        papersInfo[i][ind] = 'NA'

#WriteOut output
out = [header]
out += papersInfo
with open('hannahprove2.csv', 'w') as cf:
    wr = csv.writer(cf)
    wr.writerows(out)
