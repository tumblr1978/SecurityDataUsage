import matplotlib.pyplot as plt
import csv, unicodedata
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
        message = unicode(message, 'utf8').lower()
    except:
        print message
        return ['errror']
    words = TextBlob(message).words
    # for each word, take its "base form" = lemma 
    return [word.lemma for word in words]

bow_transformer = CountVectorizer(analyzer=split_into_lemmas).fit(papers['paper'])
print 'bow vocabulary:', len(bow_transformer.vocabulary_)

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
            

