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
from sklearn.svm import LinearSVC

papers = pandas.read_csv('./MLpapers_whole.csv', delimiter=',', quotechar='|',
                           names=["paperName","paper","label"])


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


X = papers_tfidf
y = papers['label']

alpha_list = [0]

for a in alpha_list:
    kf = StratifiedKFold(n_splits=10)
    cfMtx_BNB = np.array([[0,0],[0,0]])
    cfMtx_MultiNB = np.array([[0,0],[0,0]])
    cfMtx_SGD = np.array([[0,0],[0,0]])
    for train_index, test_index in kf.split(X, y):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        paperName_test = papers['paperName'][test_index]

        model1 = MultinomialNB(alpha=0.05).fit(X_train, y_train)
        predict1 = model1.predict(X_test)
        cfMtx_MultiNB += confusion_matrix(y_test, predict1)

        model2 = BernoulliNB(alpha=0.05).fit(X_train, y_train)
        predict2 = model2.predict(X_test)
        cfMtx_BNB += confusion_matrix(y_test, predict2)

        model3 = SGDClassifier(alpha=0.05).fit(X_train, y_train)
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

