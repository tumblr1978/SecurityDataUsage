from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
from os import listdir
import csv

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


#open all pdf files in the specify folder
pdfsPath = './papers/'
pdfs = [f for f in listdir(pdfsPath) if f.endswith('.pdf')]


#create keywords set need to evaluate for each pdf file
keys = ['dataset','Alexa','families','exploits','vulnerabilities','figures','survey']


#evaluate each pdf file, use dictrionary in case some numbers of papers not exist
results = {}
#here 1
out = []
for pdf in pdfs:
    ind = int(pdf[:pdf.index('.')])
    results[ind] = ['No','\\']
    #do it three times in case it is not converted completely
    for t in range(3):
        content = convert_pdf_to_txt(pdfsPath+pdf)
        page = ''.join([x if ord(x) > 0 else ' ' for x in content]) #replace all the null characters
        check = page.lower().find('references')
        #check if the converter convert pdf files completely
        if check == -1:
            if t == 2:
                print 'Error! '+ pdf+' :' +str(len(page))
        else:
#here 1
            out.append("|||"+str(ind)+"|||"+page)
            break
    print pdf + ' done'
'''
    for key in keys:
        if key in page:
            if results[i][0] == 'No':
                results[i][0] = 'Yes'
                results[i][1] = ''
                results[i].append(key)
            index = page.index(key)
            results[i][1] = results[i][1] + page[index-100:index+100]+'\n'
    results[i][1]= '"'+results[i][1]+'"'


#append output to appropriate file
out = []

with open('sample.csv','rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        out.append(row)

for i in range(len(out)):
    if i in results:
        out[i] = out[i]+results[i]

with open('sampleOut.csv','wb') as csvfile:
    writer = csv.writer(csvfile,delimiter=',')
    writer.writerows(out)

'''

f = open('rawPapers.txt','w')
f.writelines(out)
f.close()
