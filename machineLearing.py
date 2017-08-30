import matplotlib.pyplot as plt
import csv, unicodedata,re
from textblob import TextBlob
import pandas
import sklearn
import cPickle
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB, GaussianNB
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

papers = pandas.read_csv('./MLpapers_whole.csv', delimiter=',', quotechar='|',
                           names=["paperName","paper","label"])




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

bow_transformer = CountVectorizer(analyzer=split_into_lemmas).fit(papers['paper'])
print 'bow vocabulary:', len(bow_transformer.vocabulary_)

papers_bow = bow_transformer.transform(papers['paper'])
print 'sparse matrix shape:', papers_bow.shape

tfidf_transformer = TfidfTransformer().fit(papers_bow)

papers_tfidf = tfidf_transformer.transform(papers_bow)


X = papers_tfidf
y = papers['label']
kf = StratifiedKFold(n_splits=10)
cfMtx_MultiNB = np.array([[0,0],[0,0]])
cfMtx_BNB = np.array([[0,0],[0,0]])
cfMtx_SGD = np.array([[0,0],[0,0]])
cfMtx_SVC = np.array([[0,0],[0,0]])
cfMtx_GNB = np.array([[0,0],[0,0]])


paper_cat1 = {}  #for MNB model
paper_cat2 = {}  #for BNB model
paper_cat3 = {}  #for SGD model
paper_cat4 = {}  #for SVC model
paper_cat5 = {}  #for GNB model
overall = {}

for n in papers['paperName']:
    paper_cat1[n] = 'Non-data'
    paper_cat2[n] = 'Non-data'
    paper_cat3[n] = 'Non-data'
    paper_cat4[n] = 'Non-data'
    paper_cat5[n] = 'Non-data'
    overall[n] = 0


for train_index, test_index in kf.split(X, y):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    paperName_test = papers['paperName'][test_index]

    model1 = MultinomialNB().fit(X_train, y_train)
    predict1 = model1.predict(X_test)
    cfMtx_MultiNB += confusion_matrix(y_test, predict1)

    model2 = BernoulliNB().fit(X_train, y_train)
    predict2 = model2.predict(X_test)
    cfMtx_BNB += confusion_matrix(y_test, predict2)

    model3 = SGDClassifier().fit(X_train, y_train)
    predict3 = model3.predict(X_test)
    cfMtx_SGD += confusion_matrix(y_test, predict3)

    model4 = LinearSVC().fit(X_train, y_train)
    predict4 = model4.predict(X_test)
    cfMtx_SVC += confusion_matrix(y_test, predict4)

    model5 = GaussianNB().fit(X_train.toarray(), y_train)
    predict5 = model5.predict(X_test.toarray())
    cfMtx_GNB += confusion_matrix(y_test, predict5)

    for i in range(len(predict1)):
        if predict1[i] == 'Data':
            paper_cat1[paperName_test[test_index[i]]] = 'Data'
        if predict2[i] == 'Data':
            paper_cat2[paperName_test[test_index[i]]] = 'Data'
        if predict3[i] == 'Data':
            paper_cat3[paperName_test[test_index[i]]] = 'Data'
        if predict4[i] == 'Data':
            paper_cat4[paperName_test[test_index[i]]] = 'Data'
        if predict5[i] == 'Data':
            paper_cat5[paperName_test[test_index[i]]] = 'Data'


print 'MultinomialNB Confusion Matrix:'
print cfMtx_MultiNB
print 'BernoulliNB Confusion Matrix:'
print cfMtx_BNB
print 'SGD Confusion Matrix:'
print cfMtx_SGD
print 'SVC Confusion Matrix:'
print cfMtx_SVC
print 'GaussianNB Confusion Matrix:'
print cfMtx_GNB

for pdf in overall.keys():
    if paper_cat1[pdf] == 'Data':
        overall[pdf] += 1
    if paper_cat2[pdf] == 'Data':
        overall[pdf] += 1
    if paper_cat3[pdf] == 'Data':
        overall[pdf] += 1
    if paper_cat4[pdf] == 'Data':
        overall[pdf] += 1
    if paper_cat5[pdf] == 'Data':
        overall[pdf] += 1


cfMtx_overall = [0, 0, 0, 0] # true positive, true negative, false positive, false negative
with open('MLpapers.csv','rU') as cf:
    rd = csv.reader(cf, delimiter = ',', quotechar = '"')
    header = rd.next()
    for row in rd:
        try:
            pdfname = row[-1]
            if row[-2] == 'Data':
                if overall[pdfname] >0:
                    cfMtx_overall[0] += 1
                else:
                    cfMtx_overall[3] += 1
            else:
                if overall[pdfname] == 0:
                    cfMtx_overall[1] += 1
                else:
                    cfMtx_overall[2] += 1
        except:
            print 'key Error:', pdfname


print 'overAll:',cfMtx_overall
