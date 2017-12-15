#Muwei Zheng
#Plotting with R

#set working dir
setwd('~/Documents/github/SecurityDataUsage/')

#install necessary package:
#install.packages('vcd')
library(grid)
library(vcd)

#read data
dt <- read.csv('muweiprove.csv')
cit <- read.csv('400papersCitations.csv')

#Mosaic plot: main category vs. Origin
pdf('MainCatVSOrigin.pdf', width=10)
mosaic(Origin ~ Main.Category, data=dt,labeling=labeling_border(varnames=FALSE,rot_labels=c(25,0,0,0), just_labels=c('left', 'center', 'center','right')), direction='v', shade=TRUE, gp=shading_max, main='Main Category vs. Origin')
dev.off()

#Mosaic plot: subCat of attacker Related vs. Origin
attack <- dt[dt$Main.Category=='Attacker Related',]
attack$Sub.Category <- factor(attack$Sub.Category)
attack$Origin <- factor(attack$Origin)
pdf('subattackVSOrigin.pdf', width=10)
mosaic(Origin ~ Sub.Category, data=attack,labeling=labeling_border(varnames=FALSE,rot_labels=c(25,0,0,0), just_labels=c('left', 'center', 'center','right')), direction='v', shade=TRUE, gp=shading_max, main='Attacker Related Sub Category vs. Origin')
dev.off()

#Mosaic plot: subCat of Defender Artifacts vs. Origin
defArt <- dt[dt$Main.Category=='Defender Artifacts',]
defArt$Sub.Category <- factor(defArt$Sub.Category)
defArt$Origin <- factor(defArt$Origin)
pdf('defArtVSOrigin.pdf', width=10)
mosaic(Origin ~ Sub.Category, data=defArt,labeling=labeling_border(varnames=FALSE,rot_labels=c(25,0,0,0), just_labels=c('left', 'center', 'center','right')), direction='v', shade=TRUE, gp=shading_max, main='Defender Artifacts Sub Category vs. Origin')
dev.off()

#Mosaicplot: subCat of Macro-level Internet Characteristics vs. Origin
macroNet <- dt[dt$Main.Category=='Macro-level Internet Characteristics',]
macroNet$Sub.Category <- factor(macroNet$Sub.Category)
macroNet$Origin <- factor(macroNet$Origin)
pdf('macroNetVSOrigin.pdf', width=10)
mosaic(Origin ~ Sub.Category, data=macroNet,labeling=labeling_border(varnames=FALSE,rot_labels=c(25,0,0,0), just_labels=c('left', 'center', 'center','right')), direction='v', shade=TRUE, gp=shading_max, main='Macro-level Internet Characteristics Sub Category vs. Origin')
dev.off()

#Mosaicplot: subCat of Users & Organizations Characteristics vs. Origin
users <- dt[dt$Main.Category=='Users & Organizations Characteristics',]
users$Sub.Category <- factor(users$Sub.Category)
users$Origin <- factor(users$Origin)
pdf('usersVSOrigin.pdf', width=10)
mosaic(Origin ~ Sub.Category, data=users,labeling=labeling_border(varnames=FALSE,rot_labels=c(25,0,0,0), just_labels=c('left', 'center', 'center','right')), direction='v', shade=TRUE, gp=shading_max, main='Macro-level Internet Characteristics Sub Category vs. Origin')
dev.off()

#Box plot: citations vs. Conference
confCit <- cit[cit$Conf. %in% c('CCS','IMC','NDSS','USENIX','SP','FC','WEIS', 'CCS-AISEC', 'USENIX-CERT', 'FC-BTW'),]
confCit$Conf. <- factor(confCit$Conf.)
pdf('ConfVSCit.pdf')
boxplot(citeNum ~ Conf., data=confCit, main='Conferences vs. Citations', xlab='Conferences', ylab='Citation Numbers')
dev.off()

#Box plot: Data or Non-data vs. Citations
pdf('dataVSCit.pdf')
boxplot(citeNum ~ Data, data=cit, main='Data or Non-Data vs. Citations', ylim=c(0,600), ylab='Citation Numbers')
wilcox.test(citeNum ~ Data, data=cit)
dev.off()

#Mosaic plot: Conference vs. Categories.
confdt <- dt[dt$Conference %in% c('CCS','IMC','NDSS','USENIX','SP','FC','WEIS', 'CCS-AISEC', 'USENIX-CERT', 'FC-BTW'),]
confdt$Conference <- factor(confdt$Conference)
pdf('confVScat.pdf', width=14, height=10)
mosaic(Main.Category ~ Conference, data=confdt,labeling=labeling_border(varnames=FALSE,rot_labels=c(90,0,0,-45), just_labels=c('left', 'center', 'center','right')), direction='v', shade=TRUE, gp=shading_max, main='Conferences vs. Main Category')
dev.off()

#Mosaic plot: Conference vs. Data or Non-Data.
pdf('ConfVSdata.pdf', width=10)
mosaic(Data ~ Conf., data=confCit,labeling=labeling_border(varnames=FALSE,rot_labels=c(90,0,0,0), just_labels=c('left', 'center', 'center','right')), direction='v', shade=TRUE, gp=shading_max, main='Conferences vs. Data or Non-Data')
dev.off()

#box plot: Public or Non-public vs. Citations
pdf('publicVSCit.pdf')
boxplot(citeNum ~ Public, data=cit, main='Public or Non-Public vs. Citations', ylab='Citation Numbers')
wilcox.test(citeNum ~ Public, data=cit)
dev.off()

#Regression: Citation vs. Year
cit$Year <- as.numeric(cit$Year)
year <- c(1,2,3,4,5)
totalCite <- c(sum(cit$citeNum[cit$Year==2016],na.rm=TRUE), sum(cit$citeNum[cit$Year==2015]), sum(cit$citeNum[cit$Year==2014]), sum(cit$citeNum[cit$Year==2013]), sum(cit$citeNum[cit$Year==2012]))
wrapCite <- data.frame(year, totalCite)
pdf('numTotCiteVSyears.pdf')
plot(totalCite~year, data=wrapCite, xlab='Number of Years before 2017', ylab='Number of Total Citations', main='Number of Total Citations vs. Years \n(Linear Regression)')
abline(lm(totalCite~year, data=wrapCite))
dev.off()

#Main categories vs. Citations
pdf('mainCatVScit.pdf')
wrapCite$Attack <- c(sum(dt$citeNum[dt$Year=='2016' & dt$Main.Category=='Attacker Related'],na.rm=TRUE), sum(dt$citeNum[dt$Year=='2015' & dt$Main.Category=='Attacker Related'],na.rm=TRUE), sum(dt$citeNum[dt$Year=='2014' & dt$Main.Category=='Attacker Related'],na.rm=TRUE), sum(dt$citeNum[dt$Year=='2013' & dt$Main.Category=='Attacker Related'],na.rm=TRUE), sum(dt$citeNum[dt$Year=='2012' & dt$Main.Category=='Attacker Related'],na.rm=TRUE))
wrapCite$Defend <- c(sum(dt$citeNum[dt$Year=='2016' & dt$Main.Category=='Defender Artifacts'],na.rm=TRUE), sum(dt$citeNum[dt$Year=='2015' & dt$Main.Category=='Defender Artifacts'],na.rm=TRUE), sum(dt$citeNum[dt$Year=='2014' & dt$Main.Category=='Defender Artifacts'],na.rm=TRUE), sum(dt$citeNum[dt$Year=='2013' & dt$Main.Category=='Defender Artifacts'],na.rm=TRUE), sum(dt$citeNum[dt$Year=='2012' & dt$Main.Category=='Defender Artifacts'],na.rm=TRUE))
wrapCite$MacroInt <- c(sum(dt$citeNum[dt$Year=='2016' & dt$Main.Category=='Macro-level Internet Characteristics'],na.rm=TRUE), sum(dt$citeNum[dt$Year=='2015' & dt$Main.Category=='Macro-level Internet Characteristics'],na.rm=TRUE), sum(dt$citeNum[dt$Year=='2014' & dt$Main.Category=='Macro-level Internet Characteristics'],na.rm=TRUE), sum(dt$citeNum[dt$Year=='2013' & dt$Main.Category=='Macro-level Internet Characteristics'],na.rm=TRUE), sum(dt$citeNum[dt$Year=='2012' & dt$Main.Category=='Macro-level Internet Characteristics'],na.rm=TRUE))
wrapCite$Users <- c(sum(dt$citeNum[dt$Year=='2016' & dt$Main.Category=='Users & Organizations Characteristics'],na.rm=TRUE), sum(dt$citeNum[dt$Year=='2015' & dt$Main.Category=='Users & Organizations Characteristics'],na.rm=TRUE), sum(dt$citeNum[dt$Year=='2014' & dt$Main.Category=='Users & Organizations Characteristics'],na.rm=TRUE), sum(dt$citeNum[dt$Year=='2013' & dt$Main.Category=='Users & Organizations Characteristics'],na.rm=TRUE), sum(dt$citeNum[dt$Year=='2012' & dt$Main.Category=='Users & Organizations Characteristics'],na.rm=TRUE))
plot(Attack~year, data=wrapCite,type='l', col=2, xlab='Number of Years before 2017', ylab='Number of Total Citations', main='Main Categories vs. Citations', ylim=c(0,2100))
lines(Defend~year, data=wrapCite,type='l', col=3)
lines(MacroInt~year, data=wrapCite,type='l', col=4)
lines(Users~year, data=wrapCite,type='l', col=5)
legend('topleft', c('Attacker Related','Defender Artifacts','Macro-Level Internet Characteristics','Users & Organizations Characteristics'), fill=c(2:5))
dev.off()

#Barplot for Main categories
pdf('barCat.pdf')
cats <- c('Attacker Related','Defender Artifacts','Macro-Level Internet Characteristics','Users & Organizations Characteristics')
catCites <- c(sum(wrapCite$Attack), sum(wrapCite$Defend), sum(wrapCite$MacroInt), sum(wrapCite$Users))
c <- as.table(setNames(catCites, cats))
x <- barplot(c, xaxt='n', col='white', ylab='Number of Total Citations', main='Main Category vs. Total Citations')
labs <- cats
text(cex=1, x=x-.25, y=-1.25, labs, xpd=TRUE, srt=45)
dev.off()

#boxplot for main categories
pdf('boxCat.pdf')
boxplot(citeNum ~ Main.Category, data=dt, ylim=c(0,400), xaxt='n', ylab='Number of Citations', main='Main Category vs. Citations')
axis(1, labels = FALSE)
text(1:4, par("usr")[3] - 0.25, srt = 45, adj = 1, labels = labs, xpd = TRUE)
dev.off()


#regression: citation vs. year+conf
citConf <- cit[cit$Conf. %in% c('CCS','IMC','NDSS','USENIX','SP','FC','WEIS', 'CCS-AISEC', 'USENIX-CERT', 'FC-BTW'),]
citConf$yearPast <- (2017-citConf$Year)
citConf$Conf. <- factor(citConf$Conf.)
allpaperConf <- lm(citeNum~yearPast+Conf., data=citConf)

#regression: citation vs. Data or non-data
allpaperDataOrNot <- lm(citeNum~yearPast+Data, data=citConf)

#regression: datapaper create or exist
dtConf <- dt[dt$Conference %in% c('CCS','IMC','NDSS','USENIX','SP','FC','WEIS', 'CCS-AISEC', 'USENIX-CERT', 'FC-BTW'),]
dtConf$yearPast <- (2017-dtConf$Year)
dtConf$Conference <- factor(dtConf$Conference)
dtConf$Exist <- ifelse(dtConf$Origin=='Existing', 'Yes', 'No')
datapaperExist <- lm(citeNum~Exist, data=dtConf)


#regression: datapaper category
datapaperCat <- lm(citeNum~yearPast+Main.Category, data=dtConf)



