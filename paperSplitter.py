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
    end = paper.lower().rfind('references')
    upper = False  # to check if it is all upper, if it is all upper, we can check easier
    if not re.search(r'REFERENCES', paper) == None:
        upper = True
    #print 'flag', upper
    if start == -1 or end == -1:
        return paper.split('\n')
    paper = paper[start:end]
    #print paper
    #print '--------------------------------'
    paras = paper.split('\n')
    words = []

    for para in paras:
        #print para,'\n'
        if len(para) > 40:
            continue
        #check if it is alnum after remove all '.' and space
        alnum = para.replace('.','',1)
        alnum = alnum.replace(' ','')
        if not alnum.isalnum():
            continue
       
        wordList = re.findall(r'[A-Za-z]+', para)
        if wordList == []:
            continue
        goodToAdd = True
        for word in wordList:
            if upper:
                if (not word.isupper()) or re.search(r'[A-Z]+$', para) == None:
                    goodToAdd = False
                    break
            else:
                if (not word.istitle()) or re.search(r'[A-Z][a-z]+$', para) == None:
                    goodToAdd = False
                    break
        if goodToAdd:
            words.append(para)
            #print 'para', para

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
        if upper:
            if not word.isupper():
                continue
        indexDict[ind] = word
        heappush(indexHeap, ind)
    indexList = [heappop(indexHeap) for i in range(len(indexHeap))]
    
    indTag = 0
    for i in range(len(indexList)-1):
        if indexList[indTag+1] - indexList[indTag] < 200:
            del indexDict[indexList[indTag+1]]
            del indexList[indTag+1]
        else:
            indTag += 1
    for i in indexList:
        print indexDict[i], i
    if len(indexList) < 5:
        return True  # use to indicate to print the head of paper to check why it is < 5

a = 0
for key in papers.keys():
    print 'Number',key
    paper = papers[key]
    flag = splitSection(paper)
    if flag:
        print paper[:200]
        a += 1
    print '\n'
print 'less 5:', a
'''
splitSection(allPapers[144])
print allPapers[144][:100]

splitSection('2. RELATED WORK\n')

'''


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


'''
    for num in range(len(paras)-2):
        para = paras[num]
        para = para.strip()
        paraFollow = paras[num+1]
        paraFollow2 = paras[num+2]
        paraFollow = paraFollow.strip()
        flag = False
        if paraFollow == '':
            flag = True
        elif paraFollow[:1].isupper(): #have situation: 2. INTRODUCTION \n 2.1 Something
            flag = True
        if para == '':
            flag = False
        elif not (para[:1].isupper() or para[:1].isdigit()):
            flag = False
        elif len(paraFollow2) < 40:   #have situation: 2. INTRODUCTION \n 2.1 sm \n \n 
            flag = False
        if len(para) < 40 and flag:
            words += re.findall(r'\w+', para)
 '''
'''
    for num in range(len(paras)-2):
        para = paras[num]
        if len(para) < 40 and (para[:1].isupper() or para[:1].isdigit()):
            if upper and not re.search(r'[A-Z]+$', para) == None: # if it is upper case, have to end with an UPPER word
                words += re.findall(r'\w+', para)
                print para
            elif not re.search(r'[A-Z][a-z]+$',para) == None :  # if it is Title case, need to define whether it is end with capital first
                if not (len(paras[num+1]) <20 and len(paras[num+2]) < 20):  # check if it is in a graph
                    words += re.findall(r'\w+', para)
'''
