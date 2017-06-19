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

#papers = pandas.read_csv('./rawPaperLabelab.csv', delimiter=',', quotechar='|',
#                           names=["label", "paper"])
#papers = pandas.read_csv('./rawPaperLabelabstract.csv', delimiter=',', quotechar='|',
#                           names=["label", "paper"])
papers = pandas.read_csv('./rawSentencesLabel.csv', delimiter=',', quotechar='|',
                           names=["paper", "label","paperID"])
print type(papers)


#using short discription as words base
'''
wordsList = []
with open('sample.csv','rb') as cf:
    reader = csv.reader(cf, delimiter=',', quotechar='"')
    for row in reader:
        s = row[5]+row[7]
        s = ''.join([x if ord(x) < 128 else ' ' for x in s])
        wordsList.append(s)
'''

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

#data_detector = MultinomialNB().fit(papers_tfidf, papers['label'])


'''
all_predictions = data_detector.predict(papers_tfidf)
for i in range(100):
    if all_predictions[i] != papers.label[i]:
        print 'label: '+papers.label[i]+'\t'+'predict: '+all_predictions[i]   


print 'accuracy', accuracy_score(papers['label'], all_predictions)
print 'confusion matrix\n', confusion_matrix(papers['label'], all_predictions)
print '(row=expected, col=predicted)'
print '\n'
'''

pipeline = Pipeline([
    ('bow', CountVectorizer(analyzer=split_into_lemmas)),  # strings to token integer counts
    ('tfidf', TfidfTransformer()),  # integer counts to weighted TF-IDF scores
    ('classifier', MultinomialNB()),  # train on TF-IDF vectors w/ Naive Bayes classifier
])

#paper_train, paper_test, label_train, label_test=\
        #train_test_split(papers['paper'],papers['label'], test_size=0.2)
'''
predicts = cross_val_predict(pipeline,
                            papers['paper'],
                            papers['label'],
                            cv=10,
                            n_jobs=-1
                            )
'''

X = papers_tfidf
y = papers['label']
kf = StratifiedKFold(n_splits=5)
for train_index, test_index in kf.split(X, y):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

    model1 = MultinomialNB().fit(X_train, y_train)
    print 'MultinomialNB:'
    print confusion_matrix(y_test, model1.predict(X_test))
    model2 = BernoulliNB().fit(X_train, y_train)
    print 'BernoulliNB: '
    print confusion_matrix(y_test, model2.predict(X_test))

