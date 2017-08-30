import matplotlib.pyplot as plt
import csv, unicodedata, sys, re
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
from nltk.corpus import stopwords


csv.field_size_limit(sys.maxsize) #set size limit to maximum

papers = pandas.read_csv('./MLpapers_sentences.csv', delimiter=',', quotechar='|',
                           names=["paper", "label","paperName"])

whole_paper_nondata = []
with open('MLpapers_whole.csv', 'rb') as cf:
    rd = csv.reader(cf, delimiter=',', quotechar='|')
    for row in rd:
        if row[-1] == 'Non-data':
            whole_paper_nondata.append(row[1])
print 'num of non-data:', len(whole_paper_nondata)


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

bow_transformer = CountVectorizer(analyzer=split_into_lemmas).fit(papers['paper'])
#print 'bow vocabulary:', len(bow_transformer.vocabulary_)
#print 'type bow', type(bow_transformer)

wordstfidf = ' '.join([x for x in tokens])


data = []
for i in range(len(papers['label'])):
    if papers['label'][i] == 'Data':
        data.append(papers['paper'][i])

data = ' '.join(data)


test_sample = [data] + whole_paper_nondata

papers_bow = bow_transformer.transform(test_sample)
data_bow = bow_transformer.transform([data])
print 'bow shape:',papers_bow.shape
#print papers_bow[0]


#Evaluate scores for only idf
'''
words = []
dataOne = papers_bow[0].indices
for ind in dataOne:
   words.append(bow_transformer.get_feature_names()[ind])
'''

tfidf_transformer = TfidfTransformer().fit(papers_bow)
#print tfidf_transformer.idf_[bow_transformer.vocabulary_['data']]
#print words[:5]
#print len(tfidf_transformer[0])
#tftest = tfidf_transformer.transform(wordstfidf)
#paper_score = tftest[0]


#Evaluate scores for tfidf of accumulate dataOne
'''
data_score = tfidf_transformer.transform(data_bow)
wordsInd = data_score.indices
score_map = {}
for i in range(len(wordsInd)):
    word = bow_transformer.get_feature_names()[wordsInd[i]]
    score = data_score.data[i]
    if score not in score_map.keys():
        score_map[score] = [word]
    else:
        score_map[score].append(word)
'''

#Evaluate scores for only idf
'''
score_map = {}
for word in words:
    score = tfidf_transformer.idf_[bow_transformer.vocabulary_[word]]
    if score not in score_map.keys():
        score_map[score] = [word]
    else:
        score_map[score].append(word)
'''

#Sort scores and write into files
'''
scores = score_map.keys()
scores.sort()
scores.reverse()

out = [['tf-idf','word']]

for score in scores:
    out.append([score, '\t'.join(score_map[score])])

with open('tfidf2.csv','wb') as cf:
    wt=csv.writer(cf, delimiter=',',quotechar='"')
    wt.writerows(out)


X = papers_tfidf
y = papers['label']
kf = StratifiedKFold(n_splits=10)
'''

papers_bow = bow_transformer.transform(papers['paper'])
papers_tfidf = tfidf_transformer.transform(papers_bow)


X = papers_tfidf
y = papers['label']
kf = StratifiedKFold(n_splits=10)


cfMtx_MultiNB = np.array([[0,0],[0,0]])
cfMtx_BNB = np.array([[0,0],[0,0]])
cfMtx_SGD = np.array([[0,0],[0,0]])


for train_index, test_index in kf.split(X, y):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    #paperName_test = papers['paperName'][test_index]

    model1 = MultinomialNB(class_prior=[0.9,0.1]).fit(X_train, y_train)
    predict1 = model1.predict(X_test)
    cfMtx_MultiNB += confusion_matrix(y_test, predict1)

    model2 = BernoulliNB(class_prior=[0.9,0.1]).fit(X_train, y_train)
    predict2 = model2.predict(X_test)
    cfMtx_BNB += confusion_matrix(y_test, predict2)

    model3 = SGDClassifier().fit(X_train, y_train)
    predict3 = model3.predict(X_test)
    cfMtx_SGD += confusion_matrix(y_test, predict3)

print 'MultinomialNB Confusion Matrix:'
print cfMtx_MultiNB
print 'BernoulliNB Confusion Matrix:'
print cfMtx_BNB
print 'SGD Confusion Matrix:'
print cfMtx_SGD
