rq <- read.csv('requestMod2.csv', sep = ',', quote = '"', header = TRUE)

cat <- aggregate(Requests~Catergory, rq, sum)

c1 <- c(111, 865, 0, 0, 0, 0, 18, 289, 351, 1052, 0)

name <- c("Adverse Events","Attacks","Cybercrime Infrastructure","Exploits","Offline Characteristics","Password Lists","PopulationEnumeration","Regular Network/Behavior Data","Synthetic Data","Topology/ScanData","Vulnerabilities")

cat <- data.frame(matrix(ncol = 11, nrow = 0))
colnames(cat)<-name
cat <- rbind(cat, c1)
par(mar=c(9,4,4,2))

x <- barplot(as.matrix(cat), xaxt='n', main = 'IMPACT Requests', col = 'green')
labs <- paste(names(cat))
text(cex=1, x=x+0.25, y=-10.25, labs, xpd=TRUE, srt=45, pos=2)

