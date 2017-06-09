import re
from heapq import heappush, heappop

out = []

f = open('rawPapers.txt','r')

out = f.readlines()
f.close()

whole = ''.join(out).split('|||')
whole = whole[1:]
papers = {}


for i in range(len(whole)/2):
    ind = whole[i*2]
    paper = whole[i*2+1]
    papers[ind] = paper

allPapers = papers.values()
'''
papersCap = []

for paper in allPapers:
    start = paper.lower().index('abstract')
    paper = paper[start:]
    words = re.findall(r'\w+', paper)
    wordsCap = [x for x in words if (x.istitle() or x.isupper()) and len(x) > 3]
    papersCap.append(list(set(wordsCap)))

print [x for x in papersCap[0] if x.isupper()]
'''

def splitSection(paper):
    start = paper.lower().find('abstract')
    end = paper.lower().find('references')
    if start == -1 or end == -1:
        return paper.split('\n')
    paper = paper[start:end]
    paras = paper.split('\n')
    words = []
    for num in range(len(paras)-2):
        para = paras[num]
        para = para.strip()
        paraFollow = paras[num+1]
        paraFollow2 = paras[num+2]
        paraFollow = paraFollow.strip()
        flag = False
        if paraFollow == '':
            flag = True
        elif paraFollow[:1].isupper():
            flag = True
        if para == '':
            flag = False
        elif not (para[:1].isupper() or para[:1].isdigit()):
            flag = False
        elif len(paraFollow2) < 40:
            flag = False
        if len(para) < 40 and flag:
            words += re.findall(r'\w+', para)
    wordsCap = [x for x in words if (x.istitle() or x.isupper()) and len(x) > 3]
    wordsCapUnique = []
    wordsCapRepeat = set()
    for word in wordsCap:
        if word not in wordsCapUnique:
            wordsCapUnique.append(word)
        else:
            wordsCapRepeat.add(word)
    for word in wordsCapRepeat:
        wordsCapUnique.remove(word)

    indexHeap = []
    indexDict = {}
    for word in wordsCapUnique:
        ind = paper.index(word)
        if ind in indexDict:
            continue
        indexDict[ind] = word
        heappush(indexHeap, ind)
    indexList = [heappop(indexHeap) for i in range(len(indexHeap))]

    
    indTag = 0
    for i in range(len(indexList)-1):
        if indexList[indTag+1] - indexList[indTag] < 40:
            try:
                del indexDict[indexList[indTag+1]]
            except:
                print indexList[indTag+1]
            del indexList[indTag+1]
        else:
            indTag += 1
    for i in indexList:
        print indexDict[i], i 

for i in range(len(allPapers)):
    print 'Number',i
    splitSection(allPapers[i])
    print '\n'


#print allPapers[0][:100]




'''
allPapers = [x.split('\n\n') for x in allPapers]

#print type(allPapers[0]), len(allPapers)
#print allPapers[0]

count = {}
elsewhere = []

for paper in allPapers:
    for para in paper:
        if len(para) < 20:
            if para.lower() not in count:
                count[para.lower()] = 1
            else:
                count[para.lower()] +=1
        elif 'Reference' in para or 'REFERENCE' in para:
            elsewhere.append(para)

print 'elsewhere:', len(elsewhere)

incount = 0
for key in count.keys():
    if 'reference' in key:
        #print key, ':', count[key]
        incount += count[key]

print 'incount:',incount
'''
