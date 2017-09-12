import csv, sys, re
from nltk.corpus import stopwords
from textblob import TextBlob

csv.field_size_limit(sys.maxsize)

#open file that contains all papers and labels
def split_into_lemmas(message):
    try:
        message = message.encode('utf-8').lower()
    except:
        print type(message)
        sys.exit()
    words = TextBlob(message).words
    # for each word, take its "base form" = lemma
    stopWords = set(stopwords.words('english'))
    wordsRaw = [word.lemma for word in words]
    wordsOut = []
    for word in wordsRaw:
        if len(word) == 1:
            continue
        if word in stopWords:
            continue
        p = re.compile(r'\W')
        check_digit = p.split(word)
        digit = True
        for i in check_digit:
            if not i.isdigit():
                digit = False
        if digit:
            continue
        wordsOut.append(word)
    return wordsOut



papers = {}
with open('MLpapers_lemma.csv','rb') as cf:
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

with open('MLpapers_lemma.csv','wb') as cf:
    wr = csv.writer(cf, delimiter=',', quotechar='"')
    wr.writerows(out)
'''

'''
fh = open('checkWords.txt','rb')
checkWords0 = set(fh.readline().split(' '))
fh.close()
print '# of checkWords0',len(checkWords0)

fh = open('checkWords1.txt','rb')
checkWords1 = set(fh.readline().split(' '))
fh.close()
print '# of checkWords1',len(checkWords1)

fh = open('checkWords2.txt','rb')
checkWords2 = set(fh.readline().split(' '))
fh.close()
print '# of checkWords2',len(checkWords2)
'''

fh = open('checkWords.txt','rb')
checkWords3 = set(fh.readline().split(' '))
fh.close()
print '# of checkWords3',len(checkWords3)

'''
falls_p = []
falls_n = []


for paper in papers.keys():
    predict3 = 'Non-data'
    word_set = papers[paper][0]
    label = papers[paper][1]
    count = 0
    for word in checkWords3:
        if word in word_set:
            count += 1
    if count > 0:
        if label != 'Data':
            falls_p.append((paper,label))
    else:
        if label == 'Data':
            falls_n.append((paper,label))
'''

paper_un = []
for paper in papers.keys():
    word_set = papers[paper][0]
    label = papers[paper][1]
    data = False
    for word in checkWords3:
        if word in word_set:
            data = True
            break
    if not data:
        paper_un.append((paper, label))

#print len(paper_un)



#print 'falls_n',len(falls_n)
#print 'falls_p',len(falls_p)
#print [x[0] for x in falls_p]


papers_pdf = {}
with open('MLpapers_whole.csv','rb') as cf:
    rd = csv.reader(cf, delimiter=',', quotechar='|')
    header = rd.next()
    for r in rd:
        text = r[1]
        name = r[0]
        label = r[2]
        papers_pdf[name] = (text, label)

print len(papers_pdf.keys())

phrase = [' Alexa', 'WHOIS','wallet','geolocation','Rockyou', 'yelp']

falls_p = []
falls_n = []
for paper, label in paper_un:
    data = False
    for word in phrase:
        if word in papers_pdf[paper][0]:
            data = True
            break
    if data:
        if label != 'Data':
            falls_p.append(paper)
    else:
        if label == 'Data':
            falls_n.append(paper)

print 'falls_n',len(falls_n)
print 'falls_p',len(falls_p)
