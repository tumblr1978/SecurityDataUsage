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
#Example: python grouping.py papers.csv downloadTest.csv 1.5


import csv, unicodedata, os, sys

#open the plain text paper file
fileName = sys.argv[1]
if not fileName.endswith('csv'):
    print 'A valid file should be in .csv format.'
    sys.exit()

papers = []
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
paperMap = {} #to store the mapping between text and its pdf name
for i in range(len(papers)):
    paper = papers[i][1]
    start = paper.lower().find('abstract')
    end = paper.lower().rfind('references')
    if start != -1 and end != -1:
        paper = paper[start:end]
    paperU = unicode(paper, 'utf-8')
    paper = unicodedata.normalize('NFKD', paperU).encode('ascii','ignore')
    #paperMap[papers[i][0]] = paper.encode('utf-8')
    paperMap[papers[i][0]] = paper


#split the data paper only around its data described sentences, and split the non-data 
#paper into grouped sentence, only from abstract to reference 
nonData = []  #to store all non-data paper samples [text, categorization, name]
dataSample = []     #to store all data paper samples  [text, categorization, name]
for row in data_info:
    datas = ''
    if row[5] != '\\':
        datas += row[5]
        datas += '|'
    if row[7] != '\\':
        datas += row[7]
    paperName = row[-1]
    if datas != '':
        paper = paperMap[paperName]
        datas = datas.split('|')
        text = ''
        for data in datas:
            if data != '':
                data = data.replace('  ',' ')
                try:
                    data = unicode(data, 'utf-8')
                except:
                    print 'paper name', paperName
                data = unicodedata.normalize('NFKD', data).encode('ascii','ignore')
                #data = data.encode('utf-8')
                find = paper.find(data)
                #find the previous 1 sentence and the following 2 sentences
                if find != -1:
                    cutStart = paper.rfind('.',0, find)
                    cutStart = paper.rfind('.',0, cutStart-1)
                    cutEnd = paper.find('.', find)
                    cutEnd = paper.find('.', cutEnd)
                    cutEnd = paper.find('.', cutEnd)
                    text = paper[cutStart+1:cutEnd]
                    dataSample.append([text, 'Data', paperName])
                else:
                    print 'data finding error', paperName,':', data
    else:
        sentences = paper.split('.')
        for i in range(len(sentences)/4):
            nonData.append(['.'.join(sentences[i*4:i*4+4]), 'Non-data', paperName])

print 'data entry (not copied):',len(dataSample)
#outWrite = outWrite*57
#print 'data entry (copied):', len(outWrite)
print 'Non-data entry #:', len(nonData)


#Mix them with different ratios
ratio = 1.0
try:
    ratio = float(sys.argv[3])
except:
    print 'ratio entered is not a valid number. System abort.'
    print sys.argv[3]
    sys.exit()    

#create a folder to store all grouping csv files
if 'grouping' not in os.listdir('./'):
    os.mkdir('grouping')

#write to a new csv file with header ['sample', 'category','paper_name']
nonData_num = int(len(dataSample)*ratio)
nonData_group = len(nonData)/nonData_num
for i in range(nonData_group-1):
    out = dataSample[:]
    out += nonData[i*nonData_num:i*nonData_num + nonData_num]
    with open('./grouping/group'+str(i)+'.csv', 'wr') as cf:
        try:
            wt = csv.writer(cf, delimiter = ',', quotechar = '|')
            wt.writerows(out)
        except:
            print 'Error!'
            print out
            break


