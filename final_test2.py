import csv, sys, re
from nltk.corpus import stopwords
from textblob import TextBlob

csv.field_size_limit(sys.maxsize)

#open file that contains all papers and labels
papers = {}
with open('papers400_lemma.csv','rb') as cf:
    rd = csv.reader(cf, delimiter=',', quotechar='"')
    header = rd.next()
    for r in rd:
        words_set = set(r[1].split(' '))
        name = r[0]
        label = r[2]
        papers[name] = (words_set, label)

print 'tot paper #:', len(papers.keys())

'''
out = [['name','text','lable']]
for paper in papers.keys():
    entry = [paper, ' '.join(papers[paper][0]), papers[paper][1]]
    out.append(entry)
print 'len(out)', len(out)

with open('papers400_lemma.csv','wb') as cf:
    wr = csv.writer(cf, delimiter=',', quotechar='"')
    wr.writerows(out)
'''


#open checkWords file
'''
fh = open('checkWords1.txt','rb')
checkWords1 = set(fh.readline().split(' '))
fh.close()
print '# of checkWords1',len(checkWords1)

fh = open('checkWords2.txt','rb')
checkWords2 = set(fh.readline().split(' '))
fh.close()
print '# of checkWords1',len(checkWords1)
'''
fh = open('checkWords.txt','rb')
checkWords = set(fh.readline().split(' '))
fh.close()
print '# of checkWords',len(checkWords)


falls_p = []
falls_n = []

phrase = []
for paper in papers.keys():
    predict1 = 'Non-data'
    word_set = papers[paper][0]
    label = papers[paper][1]
    for w in phrase:
        if w in word_set:
            predict1 = 'Data'
            break
    for word in checkWords:
        if word in word_set:
            predict1 = 'Data'
            break
    if predict1 != label:
        if label == 'Data':
            falls_n.append((paper,label))
        else:
            falls_p.append((paper,label))





print 'falls_n',len(falls_n)
print 'falls_p',len(falls_p)
#print [x[0] for x in falls_p]

'''
papers_pdf = {}
with open('papers400_whole.csv','rb') as cf:
    rd = csv.reader(cf, delimiter=',', quotechar='|')
    header = rd.next()
    for r in rd:
        text = r[1]
        name = r[0]
        label = r[2]
        papers_pdf[name] = (text, label)
'''
