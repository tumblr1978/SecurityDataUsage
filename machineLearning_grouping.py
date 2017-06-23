import matplotlib.pyplot as plt
import csv, unicodedata, os
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


def split_into_tokens(message):
    message = unicode(message, 'utf8')  # convert bytes into proper unicode
    return TextBlob(message).words

def split_into_lemmas(message):
    try:
        message = unicode(message, 'utf8').lower()
    except:
        #print message
        return ['errror']
    words = TextBlob(message).words
    # for each word, take its "base form" = lemma 
    return [word.lemma for word in words]

#def machine_learn(filePath,bow_transformer, dict1, dict2):
def machine_learn(filePath, test_set, test_set_count1, test_set_count2):  #option2
    papers = pandas.read_csv(filePath, delimiter=',', quotechar='|',
                               names=["paper", "label","paperID"])

    bow_transformer = CountVectorizer(analyzer=split_into_lemmas).fit(test_set['paper']) #option2
    #bow_transformer = CountVectorizer(analyzer=split_into_lemmas).fit(papers['paper'])

    papers_bow = bow_transformer.transform(papers['paper'])

    tfidf_transformer = TfidfTransformer().fit(papers_bow)

    papers_tfidf = tfidf_transformer.transform(papers_bow)
   
    #option2
    testset_bow = bow_transformer.transform(test_set['paper'])
    testset_tfidf = tfidf_transformer.transform(testset_bow)
    
    #option 2
    model = MultinomialNB().fit(papers_tfidf, papers['label'])
    predict = model.predict(testset_tfidf)
    for i in range(len(predict)):
        if predict[i] == 'Data':
            test_set_count1[i] += 1
    #option2
    model = BernoulliNB().fit(papers_tfidf, papers['label'])
    predict = model.predict(testset_tfidf)
    for i in range(len(predict)):
        if predict[i] == 'Data':
            test_set_count2[i] += 1
    return test_set_count1, test_set_count2

''' 
    X = papers_tfidf
    y = papers['label']
    kf = StratifiedKFold(n_splits=5)

    for train_index, test_index in kf.split(X, y):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        paperID_test = papers['paperID'][test_index]

        model1 = MultinomialNB().fit(X_train, y_train)
        predict1 = model1.predict(X_test)
        for i in range(len(predict1)):
            if predict1[i] == 'Data':
                dict1[int(paperID_test[test_index[i]])] += 1

        model2 = BernoulliNB().fit(X_train, y_train)
        predict2 = model2.predict(X_test)

        for i in range(len(predict2)):
            if predict2[i] == 'Data':
                dict2[int(paperID_test[test_index[i]])] += 1
    
    return dict1, dict2
'''

def add_list(lista, listb):
    if len(lista) != len(listb):
        print "Error, list size not match!"
        return []
    for i in range(len(lista)):
        lista[i] += listb[i]
    return lista

mainPath = './grouping/'
csvFiles = [x for x in os.listdir(mainPath) if x.endswith('.csv')]

paper_cat1 = ['Non-data']*169
paper_cat2 = ['Non-data']*169

'''
num_data1 = {}
num_data2 = {}
for i in range(169):
    num_data1[i] = 0
    num_data2[i] = 0
'''
#option 2
test_set = pandas.read_csv('wholesample_sentences.csv', delimiter=',', quotechar='|', names=['paper','label','paperID'])
num_data1 = {}
num_data2 = {}
for i in range(len(test_set['paperID'])):
    num_data1[i] = 0
    num_data2[i] = 0

overall_MNB = [0,0,0,0]  #true positive, true negative, false positive, false negative
overall_BNB = [0,0,0,0]

test_set = pandas.read_csv('wholesample_sentences.csv', delimiter=',', quotechar='|', names=['paper','label','paperID'])
bow_transformer = CountVectorizer(analyzer=split_into_lemmas).fit(test_set['paper']) #option2

for i in range(len(csvFiles)):
    csvfile = csvFiles[i]
    #num_data1, num_data2 = machine_learn(mainPath+csvfile, bow_transformer, num_data1, num_data2)
    #print 'MultinomialNB:', mnb
    #print 'BernoulliNB:', bnb
    #overall_MNB = add_list(overall_MNB, mnb)
    #overall_BNB = add_list(overall_BNB, bnb)
    
    #option 2
    num_data1, num_data2 = machine_learn(mainPath+csvfile, test_set, num_data1, num_data2)
    print 'finish', i

#option 2
for i in range(len(test_set['paperID'])):
    if num_data1[i] > 5:
        paper_cat1[int(test_set['paperID'][i])] = 'Data'
    if num_data2[i] > 5:
        paper_cat2[int(test_set['paperID'][i])] = 'Data'

#for i in range(169):
#    if num_data1[i] >3 :
#        paper_cat1[i] = 'Data'
#    if num_data2[i] >3:
#        paper_cat2[i] = 'Data'


with open('sample.csv','rU') as cf:
    rd = csv.reader(cf, delimiter = ',', quotechar = '"')
    for row in rd:
        if row[-2] == 'Data':
            if int(row[-1]) in [20,148,157]:
                continue
            if paper_cat1[int(row[-1])] == 'Data':
                overall_MNB[0] += 1
            else:
                overall_MNB[3] += 1
                #print 'false negative paper num: ', row[-1]
            if paper_cat2[int(row[-1])] == 'Data':
                overall_BNB[0] += 1
            else:
                overall_BNB[3] += 1
                #print 'false negative paper num: ', row[-1]
        else:
            if paper_cat1[int(row[-1])] == 'Non-data':
                overall_MNB[1] += 1
            else:
                overall_MNB[2] += 1
            if paper_cat2[int(row[-1])] == 'Non-data':
                overall_BNB[1] += 1
            else:
                overall_BNB[2] += 1
print 'overall_MNB:'
print overall_MNB
print 'overall_BNB:'
print overall_BNB
    

