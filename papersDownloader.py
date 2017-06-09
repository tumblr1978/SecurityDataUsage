import csv, subprocess, os, urllib2, time, random

urls = []

#open all url lists
with open('sample.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        urls.append(row[1])

#to check if the directory storing the papers exist
if 'papers' not in os.listdir('./'):
    os.mkdir('papers')

#locate links directing to the pdf files
print "start crawling websites and downloading pdfs"
for i in range(155,len(urls)):
    pdfURL = ''
    url = urls[i]
    
    if url.endswith('.pdf') or 'ieeexplore.ieee.org' in url:
        pdfURL = url
    else:
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}
        req = urllib2.Request(url, headers=hdr)
        try:
            urlf = urllib2.urlopen(req, timeout=20)
            page = urlf.read()
        except urllib2.HTTPError,e:
            print e.fp.read()
        #find the citation
        #if it is a paper on usenix conference
        pdfURLstart = 0
        pdfURLend = 0
        if 'usenix' in url:
            loc = page.index('.pdf')
        else:
            loc = page.index("citation_pdf_url")
        pdfURLstart = page.index('http', loc)
        pdfURLend = page.index('"', pdfURLstart)
        pdfURL = page[pdfURLstart:pdfURLend]
        #ccs will redirect the page, so need the redirecting URL
        req = urllib2.Request(pdfURL, headers=hdr)
        opener = urllib2.build_opener()
        pdfURL = opener.open(req).url

    #dowload paper
    subprocess.call(['curl',pdfURL, '-o', './papers/'+str(i)+'.pdf'])
    print 'paper '+ str(i)+' done'
    #Delay program for around 20 seconds.
    wait = random.randint(10,30)
    print 'waiting for '+str(wait)+'s'
    time.sleep(wait)
print "crawling done"


