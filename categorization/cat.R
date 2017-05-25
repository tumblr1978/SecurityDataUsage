#Muwei 
#set working directory
setwd('~/Downloads/cat2/')

#read data
impact <- read.csv("IMPACTcat.csv", sep=',',quote='"')
papers <- read.csv('paperscat.csv',sep=',',quote='"')

#clean up "papers"
papers$Public.[papers$Public. =="Yes\n"] <- 'Yes'
papers$public <-ifelse(papers$Public. == 'Yes', 'public', 'non-public')
papers$public <- as.factor(papers$public)

papers$Year <- as.factor(papers$Year)

papers$In.IMPACT[papers$In.IMPACT =="No\n"] <- 'No'
papers$inIMPACT <-ifelse(papers$In.IMPACT == 'No', 'outside-IMPACT', 'in-IMPACT')
papers$inIMPACT <- as.factor(papers$inIMPACT)

#making new tables focus on categories
catIndustry <- table(papers$Research.or.Industry., papers$Data.Category)
catIndustryprop <- round(100*prop.table(catIndustry,1),2)

catPublic <- table(papers$public, papers$Data.Category)
catPublicprop <- round(100*prop.table(catPublic,1),2)

catInIMPACT <- table(papers$inIMPACT, papers$Data.Category)
catInIMPACTprop <- round(100*prop.table(catInIMPACT,1),2)

catYear <- table(papers$Year, papers$Data.Category)
catYearprop <- round(100*prop.table(catYear,1),2)

catUsed <- table(papers$Data.Used.or.Produced., papers$Data.Category)
catUsedprop <- round(100*prop.table(catUsed,1),2)

catConference <- table(papers$Conference, papers$Data.Category)
catConferenceprop <- round(100*prop.table(catConference,1),2)
    
#IMPACT table
p2<-papers[papers$Research.or.Industry.=='Research',c("Data.Category","Research.or.Industry.")]
p2$paperorimpact<-"papers"
names(p2)<-c("Category","RoI","PoI")

impact$Research.or.Industry.<-"Research"
i2<-impact[,c("ourCategory","Research.or.Industry.")]
i2$paperorimpact<-"impact"
names(i2)<-c("Category","RoI","PoI")
pi2<-rbind(p2,i2)

tempT <- data.frame(unclass(summary(impact$ourCategory)))
tempT <- as.data.frame(t(tempT))
row.names(tempT) <- c('IMPACT')

tempT2 <- data.frame(unclass(summary(papers$Data.Category[papers$Research.or.Industry.=='Research'])))
tempT2 <- as.data.frame(t(tempT2))
row.names(tempT2) <- c('outside-IMPACT')

#pdf('pieIMPACT.pdf',width=8)
#pie(as.numeric(tempT[1,]),labels=names(tempT), main='IMPACT Categorization')
#dev.off()

tempT[c('Cybercrime Infrastructure','Exploits','Offline Characteristics','Password Lists','Vulnerabilities')] <- 0
catPapers <- table(pi2$PoI,pi2$Category)
catPapersprop <- round(100*prop.table(catPapers,1),2)

#IMPACT table vs. Used
p2<-papers[papers$Data.Used.or.Produced.=='Used',c("Data.Category","Data.Used.or.Produced.")]
p2$paperorimpact<-"papers"
names(p2)<-c("Category","U","PoI")

impact$Used.<-"Used"
i2<-impact[,c("ourCategory","Used.")]
i2$paperorimpact<-"impact"
names(i2)<-c("Category","U","PoI")

pi2<-rbind(p2,i2)
catPapersUsed <- table(pi2$PoI,pi2$Category)
catPapersUsedprop <- round(100*prop.table(catPapersUsed,1),2)

#making mosaic plots
pdf('mosaicIMPACT.pdf')
mosaicplot(catPapers, las=1, col=rainbow(7), main='IMPACT vs. outside-IMPACT-research',shade=TRUE)
dev.off()

pdf('mosaicIMPACTUsed.pdf')
mosaicplot(catPapersUsed, las=1, col=rainbow(7), main='IMPACT vs. outside-IMPACT-used',shade=TRUE)
dev.off()

pdf('mosaicReseachIndustry.pdf')
mosaicplot(catIndustry, las=1, col=rainbow(7), main='Outside IMPACT\nResearch vs. Industry',shade=TRUE)
dev.off()

pdf('mosaicUsedProduced.pdf')
mosaicplot(catUsed, las=1, col=rainbow(7), main='Outside IMPACT\nUsed vs. Produced',shade=TRUE)
dev.off()

pdf('mosaicPublic.pdf')
mosaicplot(catPublic, las=1, col=rainbow(7), main='Outside IMPACT\nPublic vs. non-Public',shade=TRUE)
dev.off()

#pdf('pieUsed.pdf',width=8.5)
#pie(as.numeric(catUsed[2,]),labels=names(as.data.frame.matrix(catUsed)), main='outside-IMPACT-used')
#dev.off()

#making barplots
pdf('barIMPACT.pdf')
par(mar=c(9,4,4,2))
x <- barplot(catPapers, beside=T, xaxt="n",col=rainbow(2), main='IMPACT vs. outside-IMPACT-research')
legend("top", c("IMPACT",'outside-IMPACT'),fill=rainbow(2))
labs <- paste(names(as.data.frame.matrix(catPapers)))
text(cex=1, x=colMeans(x)-.25, y=-1.25, labs, xpd=TRUE, srt=45, pos=2)
dev.off()

pdf('barIMPACTused.pdf')
par(mar=c(9,4,4,2))
x <- barplot(catPapersUsed, beside=T, xaxt="n",col=rainbow(2), main='IMPACT vs. outside-IMPACT-used')
legend("top", c("IMPACT",'outside-IMPACT'),fill=rainbow(2))
labs <- paste(names(as.data.frame.matrix(catPapersUsed)))
text(cex=1, x=colMeans(x)-.25, y=-1.25, labs, xpd=TRUE, srt=45, pos=2)
dev.off()

pdf('barUsed.pdf')
par(mar=c(9,4,4,2))
x <- barplot(catUsed, beside=T, xaxt="n",col=rainbow(2), main='Outside IMPACT\nUsed vs. Produced')
legend("top", c("Produced",'Used'),fill=rainbow(2))
labs <- paste(names(as.data.frame.matrix(catUsed)))
text(cex=1, x=colMeans(x)-.25, y=-1.25, labs, xpd=TRUE, srt=45, pos=2)
dev.off()

pdf('barIndustry.pdf')
par(mar=c(9,4,4,2))
x <- barplot(catIndustry, beside=T, xaxt="n",col=rainbow(2), main='Outside IMPACT\nResearch vs. Industry')
legend("top", c("Industry",'Research'),fill=rainbow(2))
labs <- paste(names(as.data.frame.matrix(catIndustry)))
text(cex=1, x=colMeans(x)-.25, y=-1.25, labs, xpd=TRUE, srt=45, pos=2)
dev.off()

pdf('barPublic.pdf')
par(mar=c(9,4,4,2))
x <- barplot(catPublic, beside=T, xaxt="n",col=rainbow(2), main='Outside IMPACT\nPublic vs. non-Public')
legend("top", c("non-Public",'Public'),fill=rainbow(2))
labs <- paste(names(as.data.frame.matrix(catPublic)))
text(cex=1, x=colMeans(x)-.25, y=-1.25, labs, xpd=TRUE, srt=45, pos=2)
dev.off()


#making tables (normal table followed by proptable)
library(gridExtra)
pdf('tableIMPACT.pdf',width=12)
grid.table(catPapers, theme = ttheme_default(base_size=7))
dev.off()

pdf('proptableIMPACT.pdf',width=12)
grid.table(catPapersprop, theme = ttheme_default(base_size=7))
dev.off()

pdf('tableIMPACTUsed.pdf',width=12)
grid.table(catPapersUsed, theme = ttheme_default(base_size=7))
dev.off()

pdf('proptableIMPACTUsed.pdf',width=12)
grid.table(catPapersUsedprop, theme = ttheme_default(base_size=7))
dev.off()

pdf('tableUsed.pdf',width=11.5)
grid.table(catUsed, theme = ttheme_default(base_size=7))
dev.off()

pdf('proptableUsed.pdf',width=11.5)
grid.table(catUsedprop, theme = ttheme_default(base_size=7))
dev.off()

pdf('tablePublic.pdf',width=11.5)
grid.table(catPublic, theme = ttheme_default(base_size=7))
dev.off()

pdf('proptablePublic.pdf',width=11.5)
grid.table(catPublicprop, theme = ttheme_default(base_size=7))
dev.off()

pdf('tableIndustry.pdf',width=11.5)
grid.table(catIndustry, theme = ttheme_default(base_size=7))
dev.off()

pdf('proptableIndustry.pdf',width=11.5)
grid.table(catIndustryprop, theme = ttheme_default(base_size=7))
dev.off()

pdf('tableYear.pdf',width=11.5)
grid.table(catYear, theme = ttheme_default(base_size=7))
dev.off()

pdf('proptableYear.pdf',width=11.5)
grid.table(catYearprop, theme = ttheme_default(base_size=7))
dev.off()

pdf('tableConference.pdf',width=15)
grid.table(catConference, theme = ttheme_default(base_size=7))
dev.off()

pdf('proptableConference.pdf',width=15)
grid.table(catConferenceprop, theme = ttheme_default(base_size=7))
dev.off()

