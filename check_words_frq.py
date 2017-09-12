import csv, sys, re
from nltk.corpus import stopwords
from textblob import TextBlob

csv.field_size_limit(sys.maxsize)



#use the same helper method to split papers
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


#open file that contains all papers and labels
names = set()
data_papers = []
nonD_papers = []
with open('MLpapers_whole.csv','rb') as cf:
    rd = csv.reader(cf, delimiter=',', quotechar='|')
    header = rd.next()
    for r in rd:
        text = r[1]
        words_set = set(split_into_lemmas(text))
        if r[-1] == 'Data':
            data_papers.append(words_set)
            names.add(r[0])
        elif r[-1] == 'Non-data':
            nonD_papers.append(words_set)
            names.add(r[0])
        else:
            print 'error:', r[-1]

print 'len data:', len(data_papers)
print 'len non-data:', len(nonD_papers)



# open file that contains tfidf words:
word_list = []
with open('tfidf2.csv','rb') as cf:
    rd = csv.reader(cf, delimiter=',', quotechar='"')
    header = rd.next()
    stopWords = set(stopwords.words('english'))
    for r in rd:
        words = r[1]
        p = re.compile(r'\W')
        words = p.split(words)
        for word in words:
            if word in stopWords:
                continue
            word_list.append(word)

print 'total words:', len(word_list)


qualify0 = []
qualify1 = []
qualify2 = []
qualify3 = []
qualify4 = []
qualify5 = []

for word in word_list:
    count = 0
    for paper in nonD_papers:
        if word in paper:
            count += 1
    if count <= 0:
        qualify0.append(word)

print 'qualify0:', len(qualify0)

count = len(data_papers)
for paper in data_papers:
    appear = False
    for word in qualify0:
        if word in paper:
            appear = True
            break
    if appear:
        count -=1
print 'not cover by qualify0:', count

fh = open('checkWords.txt', 'wb')
fh.write(' '.join(qualify0))
fh.close()


word_list = word_list[:len(word_list)/2]
print 'total words:', len(word_list)
#check appearance of these words in Non-data papers. If it is < 18, marked down
for word in word_list:
    count = 0
    for paper in nonD_papers:
        if word in paper:
            count += 1
    if count <= 1:
        qualify1.append(word)
    if count <= 2:
        qualify2.append(word)
    if count <= 3:
        qualify3.append(word)
    if count <= 4:
        qualify4.append(word)
    if count <= 5:
        qualify5.append(word)

print '1',len(qualify1)
print '2',len(qualify2)
print '3',len(qualify3)
print '4',len(qualify4)
print '5',len(qualify5)

count = len(data_papers)
for paper in data_papers:
    appear = False
    for word in qualify1:
        if word in paper:
            appear = True
            break
    if appear:
        count -=1
print 'not cover by qualify1:', count

count = len(data_papers)
for paper in data_papers:
    appear = False
    for word in qualify2:
        if word in paper:
            appear = True
            break
    if appear:
        count -=1
print 'not cover by qualify2:', count

count = len(data_papers)
for paper in data_papers:
    appear = False
    for word in qualify3:
        if word in paper:
            appear = True
            break
    if appear:
        count -=1
print 'not cover by qualify3:', count


count = len(data_papers)
for paper in data_papers:
    appear = False
    for word in qualify4:
        if word in paper:
            appear = True
            break
    if appear:
        count -=1
print 'not cover by qualify4:', count



count = len(data_papers)
for paper in data_papers:
    appear = False
    for word in qualify5:
        if word in paper:
            appear = True
            break
    if appear:
        count -=1
print 'not cover by qualify5:', count

fh = open('checkWords1.txt', 'wb')
fh.write(' '.join(qualify1))
fh.close()

fh = open('checkWords2.txt', 'wb')
fh.write(' '.join(qualify2))
fh.close()


fh = open('checkWords3.txt', 'wb')
fh.write(' '.join(qualify3))
fh.close()

fh = open('checkWords4.txt', 'wb')
fh.write(' '.join(qualify4))
fh.close()



