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
    paperU = unicode(paper, 'utf-8')
    paper = unicodedata.normalize('NFKD', paperU)
    papers[ind] = paper

outWrite = []
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
            for data in datas:
                if data != '':
                    data = data.replace('  ',' ')
                    try:
                        data = unicode(data, 'utf-8')
                    except:
                        print 'ind:', ind
                    data = unicodedata.normalize('NFKD', data)
                    data = data.encode('ascii','ignore')
                    find = paper.find(data)
                    if find == -1:
                        print 'data:',ind, data
                        flag = False
        if flag:
            row.append('match')
        else:
            row.append('not-match')
        outWrite.append(row)

with open('sample2.csv','wb') as cf:
    wr = csv.writer(cf, delimiter=',', quotechar = '"')
    wr.writerows(outWrite)

            



