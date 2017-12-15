#1. take an input file witch should have the Description column.
#2. extract all words that is not in stopwords list starting with capital letter
#3. outwrite the words list to a file
#4. should take two parameters, the first one is the input csv file, the second one
#   is the output file name
#Example: python catchwords.py muweiprove.csv dataNames.txt

from nltk.corpus import stopwords
import csv, sys

#initial stopwords, outputlist
stopWords = set(stopwords.words('english'))
out = set()

#Read the input file
with open(sys.argv[1], 'rU') as cf:
    rd = csv.reader(cf, delimiter=',', quotechar='"')
    header = rd.next()
    #find the column of description
    ind = header.index('Description')
    #extract target words
    for r in rd:
        words = r[ind].split()
        for word in words:
            if word.lower() not in stopWords and word[:1].isupper():
                out.add(word)

#outWrite output list
out = [x for x in out]

f = open(sys.argv[2], 'wb')
f.write('\n'.join(out))
f.close()
