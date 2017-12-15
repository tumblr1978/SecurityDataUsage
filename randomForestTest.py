import csv, re, sys, datetime
from textblob import TextBlob
import pandas
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from nltk.corpus import stopwords
from sklearn.ensemble import RandomForestClassifier

#Set random seed
np.random.seed(0)

#Load Data
papers = pandas.read_csv('./papers400_whole.csv', delimiter=',', quotechar='|',
                           names=["paperName","paper","label"])

#Helper function that split articles into tokens
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

#Break papers into tokens
bow_transformer = CountVectorizer(analyzer=split_into_lemmas).fit(papers['paper'])
print 'bow vocabulary:', len(bow_transformer.vocabulary_)

papers_bow = bow_transformer.transform(papers['paper'])
print 'sparse matrix shape:', papers_bow.shape

#Calculate tf-idf for papers
tfidf_transformer = TfidfTransformer().fit(papers_bow)

papers_tfidf = tfidf_transformer.transform(papers_bow)

#Cross-Validation
X = papers_tfidf
y = papers['label']
kf = StratifiedKFold(n_splits=10)

print 'start modeling...', datetime.datetime.now()
leaf_options = [1,5,10,50,100,200,500]
for leaf in leaf_options:
    cfMtx = np.array([[0,0],[0,0]])
    for train_index, test_index in kf.split(X, y):

        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        clf = RandomForestClassifier(n_jobs=-1, random_state=0, n_estimators=1000, min_samples_leaf=leaf)
        clf.fit(X_train, y_train)
        predict = clf.predict(X_test)
        cfMtx += confusion_matrix(y_test, predict)

    print 'leaf:', leaf
    print cfMtx
    print '-----------------'
print 'finish modeling...', datetime.datetime.now()
