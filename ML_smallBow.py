import matplotlib.pyplot as plt
import csv, unicodedata, sys
from textblob import TextBlob
import pandas
import sklearn
import cPickle
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.svm import SVC, LinearSVC
from sklearn.metrics import classification_report, f1_score, accuracy_score, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import learning_curve
from sklearn.linear_model import SGDClassifier
import sys,csv

csv.field_size_limit(sys.maxsize) #set size limit to maximum

papers = pandas.read_csv('./MLpapers_sentences.csv', delimiter=',', quotechar='|',
                           names=["paper", "label","paperName"])

#papers_origin = pandas.read_csv('./rawSentencesLabelCopy.csv', delimiter=',', quotechar='|',
#                           names=["paper", "label","paperName"])

def split_into_tokens(message):
    message = unicode(message, 'utf8')  # convert bytes into proper unicode
    return TextBlob(message).words

def split_into_lemmas(message):
    try:
        message = message.encode('utf-8').lower()
    except:
        print type(message)
        sys.exit()
    words = TextBlob(message).words
    # for each word, take its "base form" = lemma 
    return [word.lemma for word in words]

dataStc = []
for i in range(len(papers['paper'])):
    if papers['label'][i] == 'Data':
        dataStc.append(papers['paper'][i])

#######
count = 0
wordset = set()
tokens = set()
for sample in dataStc:
    sample = split_into_lemmas(sample)
    for word in sample:
        if word.isdigit():
            count += 1
        elif len(word) <= 2:
            wordset.add(word)
        else:
            tokens.add(word)
#print 'numbers: ', count
#print 'len 1 & 2:',len(wordset)
print 'len tokens', len(tokens)
#print ''

bow_transformer = CountVectorizer(analyzer=split_into_lemmas).fit(tokens)
#print 'bow vocabulary:', len(bow_transformer.vocabulary_)
#print 'type bow', type(bow_transformer)

wordstfidf = ' '.join([x for x in tokens])


paper1 = papers['paper'][1]
bow1 = bow_transformer.transform([paper1])
#print 'bow1:'
#print len(bow1.data)
#print len(bow1.indices)
#print ''


data = []
for i in range(len(papers['label'])):
    if papers['label'][i] == 'Data':
        data.append(papers['paper'][i])

papers_bow = bow_transformer.transform(papers['paper'])
freq = [0]*2691
print 'bow shape:',papers_bow.shape


'''
for i in range(len(bow1.indices)):
    freq[int(bow1.indices[i])] += int(bow1.data[i])

for i in range(len(freq)):
    if freq[i] != 0:
        print i, ':', freq[i]
'''

tfidf_transformer = TfidfTransformer().fit(papers_bow)
tftest = tfidf_transformer.transform(wordstfidf)



#papers_tfidf = tfidf_transformer.transform(papers_bow)
#papers_bow = papers_tfidf


'''
count = 0
for i in range(len(papers['label'])):
    if papers['label'][i] != 'Data':
        continue
    count += 1
    bow = papers_bow[i]
    for t in range(len(bow.indices)):
        freq[int(bow.indices[t])] += float(bow.data[t])
print count
print freq[:10]

freqMap = {}
for i in range(len(freq)):
    word = bow_transformer.get_feature_names()[i]
    if freq[i] not in freqMap.keys():
        freqMap[freq[i]] = [word]
    else:
        freqMap[freq[i]].append(word)

key = freqMap.keys()
key.sort()
key.reverse()
out = [['freq', 'words']]
for k in key:
    out.append([k, '   '.join(freqMap[k])])

with open('wordTfidf.csv','wb') as cf:
    wr = csv.writer(cf, delimiter = ',', quotechar='"')
    wr.writerows(out)
'''
    



'''
papers_bow = bow_transformer.transform(papers['paper'])
tfidf_transformer = TfidfTransformer().fit(papers_bow)
papers_tfidf = tfidf_transformer.transform(papers_bow)
print 'tfidf type',type(papers_tfidf)
print 'papers_tfidf[1]:'
print len(papers_tfidf[1].data)
print len(papers_tfidf[1].indices)


data_tf = []
nondata_tf = []
print papers_tfidf.nnz
print papers_tfidf.shape
print len(papers['label'])


print 'tfidf 1:'
print papers_tfidf[1].data
print 'sum 1:', sum(papers_tfidf[1].data)
for i in range(len(papers['label'])):
    if papers['label'][i] == 'Data':
        data_tf.append(sum(papers_tfidf[i].data))
    else:
        nondata_tf.append(sum(papers_tfidf[i].data))

print len(data_tf)
print 'data_tf[1]:', data_tf[1]
print len(nondata_tf)

out = [['data', x] for x in data_tf] + [['non-data', x] for x in nondata_tf]
out = [['label','tfidf']]+out

with open('tfidf_sentences.csv','wb') as cf:
    wr = csv.writer(cf, delimiter = ',', quotechar='"')
    wr.writerows(out)
'''



'''
#bow_transformer = CountVectorizer(analyzer=split_into_lemmas).fit(papers['paper'])
bow_transformer = CountVectorizer(analyzer=split_into_lemmas).fit(split_into_tokens(dataStc))
print 'bow vocabulary:', len(bow_transformer.vocabulary_)
'''
'''
papers_bow = bow_transformer.transform(papers['paper'])
print 'sparse matrix shape:', papers_bow.shape

tfidf_transformer = TfidfTransformer().fit(papers_bow)

papers_tfidf = tfidf_transformer.transform(papers_bow)

#to check whether the paper is 'data' or 'non-data'
paper_cat1 = {}  #for MNB model
paper_cat2 = {}  #for BNB model
paper_cat3 = {}  #for SGD model

for n in papers['paperName']:
    paper_cat1[n] = 'Non-data'
    paper_cat2[n] = 'Non-data'
    paper_cat3[n] = 'Non-data'

X = papers_tfidf
y = papers['label']
kf = StratifiedKFold(n_splits=10)
cfMtx_MultiNB = np.array([[0,0],[0,0]])
cfMtx_BNB = np.array([[0,0],[0,0]])
cfMtx_SGD = np.array([[0,0],[0,0]])

print 'Start modeling...'
for train_index, test_index in kf.split(X, y):
    X_test = X[test_index]
    y_test = y[test_index]
    paperName_test = papers['paperName'][test_index]

    #Dealing with unbalanced sample
    #Copying
    copy = []
    for i in train_index:
        if y[i] == 'Data':
            copy.append(i)
    copy = np.array(copy)
    for t in range(74):
        train_index = np.hstack((train_index, copy))
    X_train = X[train_index]
    y_train = y[train_index]
    
    #modeling
    model1 = MultinomialNB().fit(X_train, y_train)
    predict1 = model1.predict(X_test)
    cfMtx_MultiNB += confusion_matrix(y_test, predict1)

    for i in range(len(predict1)):
        if predict1[i] == 'Data':
            paper_cat1[paperName_test[test_index[i]]] = 'Data'

    model2 = BernoulliNB().fit(X_train, y_train)
    predict2 = model2.predict(X_test)
    cfMtx_BNB += confusion_matrix(y_test, predict2)

    for i in range(len(predict2)):
        if predict2[i] == 'Data':
            paper_cat2[paperName_test[test_index[i]]] = 'Data'

    model3 = SGDClassifier().fit(X_train, y_train)
    predict3 = model3.predict(X_test)
    cfMtx_SGD += confusion_matrix(y_test, predict3)

    for i in range(len(predict3)):
        if predict3[i] == 'Data':
            paper_cat3[paperName_test[test_index[i]]] = 'Data'


print 'MultinomialNB Confusion Matrix:'
print cfMtx_MultiNB
print 'BernoulliNB Confusion Matrix:'
print cfMtx_BNB
print 'SGD Confusion Matrix:'
print cfMtx_SGD

cfMtx_paper_MNB = [0, 0, 0, 0] # true positive, true negative, false positive, false negative
cfMtx_paper_BNB = [0, 0, 0, 0]
cfMtx_paper_SGD = [0, 0, 0, 0]
with open('MLpapers.csv','rU') as cf:
    rd = csv.reader(cf, delimiter = ',', quotechar = '"')
    header = rd.next()
    for row in rd:
        try:
            pdfname = row[-1]
            if row[-2] == 'Data':
                if paper_cat1[pdfname] == 'Data':
                    cfMtx_paper_MNB[0] += 1
                else:
                    cfMtx_paper_MNB[3] += 1
                    #print 'false negative paper num: ', row[-1]
                if paper_cat2[pdfname] == 'Data':
                    cfMtx_paper_BNB[0] += 1
                else:
                    cfMtx_paper_BNB[3] += 1
                if paper_cat3[pdfname] == 'Data':
                    cfMtx_paper_SGD[0] += 1
                else:
                    cfMtx_paper_SGD[3] += 1
            else:
                if paper_cat1[pdfname] == 'Non-data':
                    cfMtx_paper_MNB[1] += 1
                else:
                    cfMtx_paper_MNB[2] += 1
                if paper_cat2[pdfname] == 'Non-data':
                    cfMtx_paper_BNB[1] += 1
                else:
                    cfMtx_paper_BNB[2] += 1
                if paper_cat3[pdfname] == 'Non-data':
                    cfMtx_paper_SGD[1] += 1
                else:
                    cfMtx_paper_SGD[2] += 1
        except:
            print 'key Error:', pdfname

print 'MNB:',cfMtx_paper_MNB
print 'BNB:',cfMtx_paper_BNB
print 'SGD:',cfMtx_paper_SGD
'''
