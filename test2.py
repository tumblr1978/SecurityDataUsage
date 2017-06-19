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
from sklearn.datasets import make_classification
from imblearn.combine import SMOTEENN

#papers = pandas.read_csv('./rawPaperLabelab.csv', delimiter=',', quotechar='|',
#                           names=["label", "paper"])
#papers = pandas.read_csv('./rawPaperLabelabstract.csv', delimiter=',', quotechar='|',
#                           names=["label", "paper"])
papers = pandas.read_csv('./rawSentencesLabel.csv', delimiter=',', quotechar='|',
                           names=['paper', 'label', 'Id'])
print type(papers)

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
#bow_transformer = CountVectorizer(analyzer=split_into_lemmas).fit(wordsList)
print 'bow vocabulary:', len(bow_transformer.vocabulary_)

papers_bow = bow_transformer.transform(papers['paper'])
print 'sparse matrix shape:', papers_bow.shape

tfidf_transformer = TfidfTransformer().fit(papers_bow)

papers_tfidf = tfidf_transformer.transform(papers_bow)


sme = SMOTEENN()
papers_res, label_res = sme.fit_sample(papers_tfidf.toarray(), papers['label'])