#Muwei Zheng
#
#This script is to split text paper into sentences,
#label them with catorization, and mapping the data position.
#It takes three inputs:
#1. csv file which contains raw txt files
#2. csv file which contains data information for each paper
#3. The ratio we want in our machine-learning test sample, should 
#   be float point if it is not integer, and should be non-data/data
#
#Example: python groupingAbstract.py MLpapers_pdf.csv MLpapers.csv


import csv, unicodedata, os, sys

#open the plain text paper file
fileName = sys.argv[1]
if not fileName.endswith('csv'):
    print 'A valid file should be in .csv format.'
    sys.exit()

papers = []
csv.field_size_limit(sys.maxsize) #set size limit to maximum
with open(fileName, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    header = reader.next() 
    for row in reader:
        papers.append(row)


#label each paper whether it is data or not
fileName = sys.argv[2]
if not fileName.endswith('csv'):
    print 'A valid file should be in .csv format.'
    sys.exit()

data_info = []
with open(fileName, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    header = reader.next() 
    for row in reader:
        data_info.append(row)


#try to normalize all strange characters like 'ff'
paperMap = {} #to store the mapping between label and its pdf name
for data in data_info:
    paperMap[data[-1]] = data[-2]

out = []    #['pdfName','pdfAbs_Mod', 'label']
count = 0
for i in range(len(papers)):
    paper = papers[i][1]
    pdfName = papers[i][0]
    start = paper.lower().find('abstract')
    end = paper.lower().find('introduction', start)
    if start != -1 and end != -1:
        paper = paper[start+8:end]
    else:
        print papers[i][0]
        count += 1
        continue
    paperU = unicode(paper, 'utf-8')
    paper = unicodedata.normalize('NFKD', paperU).encode('ascii','ignore')
    out.append([papers[i][0],paper,paperMap[pdfName]])

print 'skip count:', count
print 'len out:', len(out)
print '-------'
#print out[0]
print '-------'


with open('MLpapers_abstracts.csv', 'wb') as cf:
    wr = csv.writer(cf, delimiter = ',', quotechar = '|')
    wr.writerows(out)

