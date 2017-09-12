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
from sklearn.svm import LinearSVC
from nltk.corpus import stopwords

papers = pandas.read_csv('./papers400_whole.csv', delimiter=',', quotechar='|',
                           names=["paperName","paper","label"])

#sentences = pandas.read_csv('./MLpapers_sentences.csv', delimiter=',', quotechar='|',
#                           names=["paper", "label","paperName"])

#using short discription as words base

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

'''
#try to use boosted data words
data = []
for i in range(len(papers['label'])):
    if papers['label'][i] == 'Data':
        data.append(papers['paper'][i])

whole_paper_nondata = []
for i in range(len(papers['paper'])):
    if papers['label'][i] == 'Non-data':
        whole_paper_nondata.append(papers['paper'][i])
print 'len non-data',len(whole_paper_nondata)

data = ' '.join(data)

test_sample = [data] + whole_paper_nondata

bow_transformer = CountVectorizer(analyzer=split_into_lemmas).fit(papers['paper'])
papers_bow = bow_transformer.transform(test_sample)

tfidf_transformer = TfidfTransformer().fit(papers_bow)

#----------------------
'''


bow_transformer = CountVectorizer(analyzer=split_into_lemmas).fit(papers['paper'])
papers_bow = bow_transformer.transform(papers['paper'])
tfidf_transformer = TfidfTransformer().fit(papers_bow)
papers_tfidf = tfidf_transformer.transform(papers_bow)

X = papers_tfidf
y = papers['label']

alpha_list = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.55, 0.6]

for a in alpha_list:
    kf = StratifiedKFold(n_splits=10)
    cfMtx_BNB = np.array([[0,0],[0,0]])
    cfMtx_MultiNB = np.array([[0,0],[0,0]])
    cfMtx_SGD = np.array([[0,0],[0,0]])
    for train_index, test_index in kf.split(X, y):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        paperName_test = papers['paperName'][test_index]

        model1 = MultinomialNB(alpha=a).fit(X_train, y_train)
        predict1 = model1.predict(X_test)
        cfMtx_MultiNB += confusion_matrix(y_test, predict1)

        model2 = BernoulliNB(alpha=a).fit(X_train, y_train)
        predict2 = model2.predict(X_test)
        cfMtx_BNB += confusion_matrix(y_test, predict2)

        model3 = SGDClassifier(alpha=a).fit(X_train, y_train)
        predict3 = model3.predict(X_test)
        cfMtx_SGD += confusion_matrix(y_test, predict3)

    print '----------'
    print 'alpha:', a
    print 'MultinomialNB Confusion Matrix:'
    print cfMtx_MultiNB
    print 'BernoulliNB Confusion Matrix:'
    print cfMtx_BNB
    print 'SGD Confusion Matrix:'
    print cfMtx_SGD
    print '----------'

