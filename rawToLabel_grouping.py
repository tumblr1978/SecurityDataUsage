import csv, unicodedata

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
        else:
            nonData.append(ind)

print 'data entry:',len(outWrite)
print 'Non-data papers #:', len(nonData)

nonDataEntries = []
for ind in nonData:
    paper = papers[ind]
    start = paper.lower().find('abstract')
    end = paper.lower().find('references')
    if start != -1 and end != -1:
        paper = paper[start:end]
    sentences = paper.split('.')
    for i in range(len(sentences)/4):
        nonDataEntries.append([''.join(sentences[i*4:i*4+4]), 'Non-data', ind])
print 'num of nonData entries:',len(nonDataEntries)

'''
outWrite += nonDataEntries
with open('wholesample_sentences.csv', 'wb') as cf:
    wr = csv.writer(cf, delimiter=',', quotechar = '|')
    wr.writerows(outWrite)
'''
numEntries = len(outWrite)*5/4
group_num = len(nonDataEntries)/numEntries

print 'numEntries:', numEntries
print 'group_num:', group_num

for i in range(group_num):
    outFile = []
    outFile += outWrite
    for t in range(numEntries):
       outFile.append(nonDataEntries[i*numEntries + t])
    #for t in range(numEntries):
    #    outFile.append(nonDataEntries[t*group_num+i])
    with open('./grouping/group'+str(i)+'.csv', 'wb') as cf:
        wt = csv.writer(cf, delimiter = ',', quotechar = '|')
        wt.writerows(outFile)
