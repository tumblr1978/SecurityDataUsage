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

papers = pandas.read_csv('./rawSentencesLabelCopy.csv', delimiter=',', quotechar='|',
                           names=["paper", "label","paperID"])

#using short discription as words base
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
paper_cat1 = ['Non-data']*169
paper_cat2 = ['Non-data']*169

X = papers_tfidf
y = papers['label']
kf = StratifiedKFold(n_splits=5)
cfMtx_MultiNB = np.array([[0,0],[0,0]])
cfMtx_BNB = np.array([[0,0],[0,0]])

for train_index, test_index in kf.split(X, y):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    paperID_test = papers['paperID'][test_index]

    model1 = MultinomialNB().fit(X_train, y_train)
    predict1 = model1.predict(X_test)
    cfMtx_MultiNB += confusion_matrix(y_test, predict1)

    for i in range(len(predict1)):
        if predict1[i] == 'Data':
            try:
                if int(paperID_test[test_index[i]]) <= 168:
                    paper_cat1[int(paperID_test[test_index[i]])] = 'Data'
                else:
                    print 'ID Error: ',paperID_test[i]
            except:
                print 'error i:', i

    model2 = BernoulliNB().fit(X_train, y_train)
    predict2 = model2.predict(X_test)
    cfMtx_BNB += confusion_matrix(y_test, predict2)

    for i in range(len(predict2)):
        if predict2[i] == 'Data':
            paper_cat2[int(paperID_test[test_index[i]])] = 'Data'


print 'MultinomialNB Confusion Matrix:'
print cfMtx_MultiNB
print 'BernoulliNB Confusion Matrix:'
print cfMtx_BNB

cfMtx_paper_MNB = [0, 0, 0, 0] # true positive, true negative, false positive, false negative
cfMtx_paper_BNB = [0, 0, 0, 0]
with open('sample.csv','rU') as cf:
    rd = csv.reader(cf, delimiter = ',', quotechar = '"')
    for row in rd:
        if row[-2] == 'Data':
            if paper_cat1[int(row[-1])] == 'Data':
                cfMtx_paper_MNB[0] += 1
            else:
                cfMtx_paper_MNB[3] += 1
                print 'false negative paper num: ', row[-1]
        else:
            if paper_cat1[int(row[-1])] == 'Non-data':
                cfMtx_paper_MNB[1] += 1
            else:
                cfMtx_paper_MNB[2] += 1

print cfMtx_paper_MNB
            

