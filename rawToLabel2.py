import csv, unicodedata

#open the plain text paper file
fileName = sys.argv[1]
if not fileName.endswith('csv'):
    print 'A valid file should be in .csv format.'
    sys.exit()

papers = []
with open(fileName, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter='|', quotechar='"')
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
    paper = unicodedata.normalize('NFKD', paperU)
    paperMap[papers[i][0]] = paper.encode('utf-8')


#split the data paper only around its data described sentences, and split the non-data 
#paper into grouped sentence, only from abstract to reference 
nonData = []  #to store all non-data paper names
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
                data = unicodedata.normalize('NFKD', data)
                data = data.encode('utf-8')
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
        nonData.append(paperName)



#write to a new csv file with header ['sample', 'category']



out = []

f = open('rawPapers2.txt','r')

out = f.readlines()
f.close()

whole = ''.join(out).split('|||')
whole = whole[1:]
papers = {}

for i in range(len(whole)/2):
    ind = whole[i*2]
    paper = whole[i*2+1]
    start = paper.lower().find('abstract')
    end = paper.lower().rfind('references')
    if start != -1 and end != -1:
        paper = paper[start:end]
    paperU = unicode(paper, 'utf-8')
    paper = unicodedata.normalize('NFKD', paperU)
    papers[ind] = paper.encode('utf-8')

outWrite = []
nonData = []
with open('sample.csv', 'rb') as cf:
    rd = csv.reader(cf, delimiter = ',', quotechar='"')
    for row in rd:
        ind = str(row[-1])
        flag = True
        datas = ''
        if row[5] != '\\':
            datas += row[5]
            datas += '|'
        if row[7] != '\\':
            datas += row[7]
        if datas != '':
            paper = papers[ind]
            datas = datas.split('|')
            text = ''
            for data in datas:
                if data != '':
                    data = data.replace('  ',' ')
                    try:
                        data = unicode(data, 'utf-8')
                    except:
                        print 'ind:', ind
                    data = unicodedata.normalize('NFKD', data)
                    data = data.encode('utf-8')
                    find = paper.find(data)
                    #find the previous 1 sentence and the following 2 sentences
                    if find != -1:
                        cutStart = paper.rfind('.',0, find)
                        cutStart = paper.rfind('.',0, cutStart)
                        cutEnd = paper.find('.', find)
                        cutEnd = paper.find('.', cutEnd)
                        cutEnd = paper.find('.', cutEnd)
                        text = paper[cutStart+1:cutEnd]
                        outWrite.append([text, 'Data', ind])
                    else:
                        print 'data:',ind, data
                        flag = False
        else:
            nonData.append(ind)
print 'data entry (not copied):',len(outWrite)
outWrite = outWrite*57
print 'data entry (copied):', len(outWrite)
print 'Non-data papers #:', len(nonData)

for ind in nonData:
    paper = papers[ind]
    sentences = paper.split('.')
    for i in range(len(sentences)/4):
        outWrite.append([''.join(sentences[i*4:i*4+4]), 'Non-data', ind])
print 'num of all entries:',len(outWrite)

with open('rawSentencesLabelCopy.csv', 'wb') as cf:
    wt = csv.writer(cf, delimiter = ',', quotechar = '|')
    wt.writerows(outWrite)

'''
for i in range(len(whole)/2):
    ind = whole[i*2]
    paper = whole[i*2+1].lower()
    #add only abstract
    start = paper.find('abstract')
    end = paper.find('introduction', start)
    if start != -1 and end != -1:
        papers[ind] = paper[start:end]

#    papers[ind] = paper.replace('|',' ')
#    if papers[ind].find('|') != -1:
#        print 'Error'

label = []
with open('sample.csv','rb') as cf:
    reader = csv.reader(cf, delimiter=',', quotechar='"')
    for row in reader:
        label.append(row[8])

out = []
for i in range(len(label)):
    if str(i) in papers:
        out.append([label[i], papers[str(i)]])

#print 'here:', out[7][0], 'there:', out[7][1][:200], 'another:', out[7][1][-200:]
#print out[7][1][out[7][1].find('Matrixk')-100:out[7][1].find('Matrixk')+100]

fh = open('rawPaperLabel.txt', 'w')
for row in out:
    row = '|'+'|,|'.join(row)+'|'
    fh.write(row)
fh.close()


with open('rawPaperLabelabstract.csv', 'wb') as cf:
    writer = csv.writer(cf, delimiter=',', quotechar='|')
    writer.writerows(out)


#print out[7]
'''
