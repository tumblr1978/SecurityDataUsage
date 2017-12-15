#from http://www.sthda.com/english/wiki/text-mining-and-word-cloud-fundamentals-in-r-5-simple-steps-you-should-know

# Install
#install.packages("tm")  # for text mining
#install.packages("SnowballC") # for text stemming
#install.packages("wordcloud") # word-cloud generator 
#install.packages("RColorBrewer") # color palettes

# Load
library("tm")
library("SnowballC")
library("wordcloud")
library("RColorBrewer")

#set directory
setwd('~/Documents/github/SecurityDataUsage/IMPACT/request/')

#read text file:
text <- readLines('commercialReason.txt')

#Load the data as a corpus
docs <- Corpus(VectorSource(text))

#clean up text:
docs <- tm_map(docs, removeWords, c("data", "use","using",'dataset','need','would','based','study','used','datasets','like'))

#build a term-document matrix
dtm <- TermDocumentMatrix(docs)
m <- as.matrix(dtm)
v <- sort(rowSums(m),decreasing=TRUE)
d <- data.frame(word = names(v),freq=v)

#Generate the word cloud
set.seed(1234)
wordcloud(words = d$word, freq = d$freq, min.freq = 1, max.words=200, random.order=FALSE, rot.per=0.35, colors=brewer.pal(8, "Dark2"))

