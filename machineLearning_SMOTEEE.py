import matplotlib.pyplot as plt
import csv, unicodedata, datetime
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

print 'program starts at:', datetime.datetime.now() #print out the time because it takes a long time
print '------------------'

#open file in pandas because this is how the tutorial told me to do
papers = pandas.read_csv('./rawSentencesLabel.csv', delimiter=',', quotechar='|',
                           names=['paper', 'label', 'Id'])

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

#Create the vocabulary base
bow_transformer = CountVectorizer(analyzer=split_into_lemmas).fit(papers['paper'])
print 'bow vocabulary:', len(bow_transformer.vocabulary_)

#Fit all 'papers' (actually not papers, but sentences) into vocabulary
papers_bow = bow_transformer.transform(papers['paper'])
print 'sparse matrix shape:', papers_bow.shape

#convet them into tfidf vecters
tfidf_transformer = TfidfTransformer().fit(papers_bow)
papers_tfidf = tfidf_transformer.transform(papers_bow)

#use SMOTEENN model to balance the sample set
sme = SMOTEENN()
tfidf_dense = papers_tfidf.toarray() #SMOTEENN requires a dense array input. This is how to convert it into densearray
papers_res, label_res = sme.fit_sample(tfidf_dense, papers['label'])

#create a dictionary to store the original tfidf, label, and id information
papers_dict = {}
for i in range(len(tfidf_dense)):
    papers_dict[tfide_dense] = [papers['label'],papers['Id']]

#create two lists to store the prediction results
paper_cat1 = ['NA']*169
paper_cat2 = ['NA']*169

#do a 5 fold cross-validation 
X = papers_res
y = label_res
kf = StratifiedKFold(n_splits=5)
#create empty confusion matrix in order to aggregate all resulting confusion matrix
cfMtx_MultiNB = np.array([[0,0],[0,0]])
cfMtx_BNB = np.array([[0,0],[0,0]])

for train_index, test_index in kf.split(X, y):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

    #MultinomialNB prediction model
    model1 = MultinomialNB().fit(X_train, y_train)
    predict1 = model1.predict(X_test)
    cfMtx_MultiNB += confusion_matrix(y_test, predict1) #aggregating confusion matrix
    
    #if one entry is predicted as 'Data' and it is in the original samplebase, mark it as 'Data'
    for i in range(len(predict1)):
        tfidf = X_test[test_index[i]]
        if tfidf in papers_dict:
            if papers_dict[tfidf][0] == 'Data':
                paper_cat1[int(papers_dict[tfidf][1])] = 'Data'
            elif papers_dict[tfidf][0] == 'Non-data':
                paper_cat1[int(papers_dict[tfidf][1])] = 'Non-data'


    #Do the same for BernoulliNB prediction model
    model2 = BernoulliNB().fit(X_train, y_train)
    cfMtx_BNB += confusion_matrix(y_test, model2.predict(X_test))

    for i in range(len(predict2)):
        tfidf = X_test[test_index[i]]
        if tfidf in papers_dict:
            if papers_dict[tfidf][0] == 'Data':
                paper_cat2[int(papers_dict[tfidf][1])] = 'Data'
            elif papers_dict[tfidf][0] == 'Non-data':
                paper_cat2[int(papers_dict[tfidf][1])] = 'Non-data'

cfMtx_paper_MNB = [0, 0, 0, 0] # true positive, true negative, false positive, false negative
cfMtx_paper_BNB = [0, 0, 0, 0]

#open the original file and compare the result to the prediction
with open('sample.csv','rU') as cf:
    rd = csv.reader(cf, delimiter = ',', quotechar = '"')
    for row in rd:
        if row[-2] == 'Data':
            if paper_cat1[int(row[-1])] == 'Data':
                cfMtx_paper_MNB[0] += 1
            else:
                cfMtx_paper_MNB[3] += 1
                print 'false negative paper num (MultiNB): ', row[-1]
            if paper_cat2[int(row[-1])] == 'Data':
                cfMtx_paper_BNB[0] += 1
            else:
                cfMtx_paper_BNB[3] += 1
                print 'false negative paper num (BNB): ', row[-1]
        else:
            if paper_cat1[int(row[-1])] == 'Non-data':
                cfMtx_paper_MNB[1] += 1
            elif paper_cat1[int(row[-1])] == 'Data':
                cfMtx_paper_MNB[2] += 1
            if paper_cat2[int(row[-1])] == 'Non-data':
                cfMtx_paper_BNB[1] += 1
            elif paper_cat2[int(row[-1])] == 'Data':
                cfMtx_paper_BNB[2] += 1

print 'MultinomialNB Confusion Matrix:'
print cfMtx_MultiNB
print 'BernoulliNB Confusion Matrix:'
print cfMtx_BNB
print 'MultiNB papers:',cfMtx_paper_MNB
print 'BernoulliNB papers:',cfMtx_paper_BNB

print '-------------------'
print 'program ends at:', datetime.datetime.now()
