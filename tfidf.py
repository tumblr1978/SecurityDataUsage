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

whole_paper_nondata = []
with open('MLpapers_whole.csv', 'rb') as cf:
    rd = csv.reader(cf, delimiter=',', quotechar='|')
    for row in rd:
        if row[-1] == 'Non-data':
            whole_paper_nondata.append(row[1])
print 'num of non-data:', len(whole_paper_nondata)


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
print 'bow shape:',papers_bow.shape
#print papers_bow[0]

words = []
dataOne = papers_bow[0].indices
for ind in dataOne:
   words.append(bow_transformer.get_feature_names()[ind])


tfidf_transformer = TfidfTransformer().fit(papers_bow)
print tfidf_transformer.idf_[bow_transformer.vocabulary_['data']]
print words[:5]
#print len(tfidf_transformer[0])
#tftest = tfidf_transformer.transform(wordstfidf)
#paper_score = tftest[0]

test = ['data']
for t in test:
    score = tfidf_transformer.idf_[bow_transformer.vocabulary_[t]]
    score = tfidf_transformer.idf_[bow_transformer.vocabulary_[word]]

score_map = {}
for word in words:
    score = tfidf_transformer.idf_[bow_transformer.vocabulary_[word]]
    if score not in score_map.keys():
        score_map[score] = [word]
    else:
        score_map[score].append(word)
            

scores = score_map.keys()
scores.sort()
scores.reverse()

out = [['tf-idf','word']]

for score in scores:
    out.append([score, '\t'.join(score_map[score])])

with open('tfidf.csv','wb') as cf:
    wt=csv.writer(cf, delimiter=',',quotechar='"')
    wt.writerows(out)
