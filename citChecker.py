#Muwei Zheng

import os, csv, urllib2, time, random

papers = []

#open paper lists and store entries in papers
with open('./dblp/data/papers2012.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        papers.append(row)

#read every page
print "start crawling websites"
for i in range(len(papers)):
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    req = urllib2.Request(papers[i][1], headers=hdr)
    try:
        urlf = urllib2.urlopen(req, timeout=20)
        page = urlf.read()
    except urllib2.HTTPError,e:
        print e.fp.read()
    #find the citation
    loc = page.index("Citation Count")
    citation = page[loc:loc+21].split('<')[0].split(':')[1]
    papers[i].append(citation)
    #Delay program for around 20 seconds.
    time.sleep(random.randint(10,30))
print "crawling done"
    
#store output
with open('./dblp/data/papers2012ci.csv','w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"')
    writer.writerows(papers)
