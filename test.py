import csv, re
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
from os import listdir

#helper method to extract content from pdf
def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text






abstr = []
with open('rawPaperLabel.csv','rb') as cf:
    reader = csv.reader(cf, delimiter=',', quotechar='|')
    a=0
    for row in reader:
        paper = row[1]
        paper = paper.lower()
        #index = paper.find('references')
        start = paper.find('abstract')
        end = paper.find('introduction')
        if start != -1 and end != -1:
            abstr.append( paper[start: end])
        else:
            abstr.append(paper)
            print a, ': No intro'
        a += 1

print str(len(abstr))
'''
redo = [7, 22, 57, 59]
correct = []

for num in redo:
    for i in range(3):
        content = convert_pdf_to_txt('./papers/'+str(num)+'.pdf')
        bad = 0
        for s in content:
            if ord(s) > 128:
                bad +=1
        print str(bad)
        page = ''.join([i if ord(i) > 0 else ' ' for i in content])
        #page = ''.join(page)
        check = page.lower().find('references')
        #check if the converter convert pdf files completely
        if check == -1:
            if i == 2:
                print 'Error! '+ pdf+' :' +str(len(page))
        else:
            correct.append(page)
            break
'''
'''
fh = open('rawPaperLabel.txt', 'w')
for row in correct:
    #row = '|'+'|,|'.join(row)
    fh.write(row)
fh.close()
'''
