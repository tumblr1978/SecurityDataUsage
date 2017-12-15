#Muwei Zheng
#Some helper methods might be useful in other scripts


import csv, re, unicodedata
from nltk.corpus import stopwords
from textblob import TextBlob

#method to read from a csv file
def readCSV(name, header, quo='"', sep=','):
    content= []
    with open(name, 'r') as cf:
        rd = csv.reader(cf, delimiter=sep, quotechar=quo)
        header = rd.next()
        for r in rd:
            content.append(r)
    return content


#method to write to a csv file
def writeCSV(name, out, quo='"', sep=',', aw='w'):
    with open(name, aw) as cf:
        wr = csv.writer(cf, delimiter=sep, quotechar=quo)
        wr.writerows(out)


#method to clean up the text: clean all non-alphadigit chars; remove multiple spaces; turn to lower case
def cleanStr(string):
    string = re.sub('[^0-9a-zA-Z]+', ' ', string)
    string = re.sub(' +', ' ', string)
    return string.strip().lower()


#Helper method to convert the strange characters into normal character. like "fi" to fi
def normalizeChar(string):
    stringU = unicode(string, 'utf-8', errors='ignore')
    string = unicodedata.normalize('NFKD', stringU)
    return string.encode('utf-8')

#Turn ever word in the string to base form and then clean up stopwords.
#Return: a list of words.
def cleanStopWords(string):
    string = cleanStr()
    words = TextBlob(string).words
    stopWords = set(stopwords.words('english'))
    wordsRaw = [word.lemma for word in words]
    wordOut = []
    for word in wordsRaw:
        if len(word) == 1:
            continue
        if word in stopWords:
            continue
        wordOut.append(word)
    return wordOut
