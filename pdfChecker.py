#Muwei Zheng
#
#This script takes three arguments:
#1. The name of the .csv file that contains all papers info
#2. The folder name that contains all pdf papers. It should under current dir.
#3. The name of the .csv file where we want to save the output.
#
#The script will convert all pdfs in the given folder into plain txt and store them in 
#a new csv file. The header will be [pdf_name | txt]. It uses '|' as delimiter.
#
#Example: python pdfChecker.py downloadTest.csv papers papers.csv

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO
import csv, os, sys

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


#open all pdf files in the 'papers' folder and also sort them into Modification time order
try:
    pdfsPath = './'+sys.argv[2]+'/'
    pdfs = [(os.path.join(pdfsPath, fn), fn) for fn in os.listdir(pdfsPath) if fn.endswith('.pdf')]
    pdfs = [(os.stat(path), fn) for path, fn in pdfs]
    pdfs = [fn for stat, fn in sorted(pdfs)]
except:
    print "Can't not locate folder", sys.argv[2]
    sys.exit()

#Match the pdf file names back to the entries in csv file
fileName = sys.argv[1]
if not fileName.endswith('csv'):
    print 'A valid file should be in .csv format.'
    sys.exit()

entries = []
with open(fileName, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    header = reader.next() 
    for row in reader:
        entries.append(row)

header.append('PDF_file_name')
out = [header]

#the number of papers in the folder should equal to the number of entries in the csv file
if len(entries) != len(pdfs):
    print 'papers number not match. Abort program.'
    print 'len(entries):',len(entries),'\t','len(pdfs):', len(pdfs)
    sys.exit()
    
for i in range(len(pdfs)):
    entries[i].append(pdfs[i])
    out.append(entries[i])

#write back to the csv file
with open(fileName,'wb') as csvfile:
    writer = csv.writer(csvfile,delimiter=',')
    writer.writerows(out)



#convert all pdfs into plain text, and then map them with their names in csv file
out = [['pdf_name','text']]
for pdf in pdfs:
    #do it three times in case it is not converted completely
    for t in range(3):
        content = convert_pdf_to_txt(pdfsPath+pdf)
        page = ''.join([x if ord(x) > 0 else ' ' for x in content])#replace all the null characters
        page = page.replace('|', ' ') #replace all '|' character in paper, therefore we can use '|' as delimiter.
        check = page.lower().find('references')
        #check if the converter convert pdf files completely
        if check == -1:
            if t == 2:
                print 'Error! '+ pdf+' :' +str(len(page))
        else:
            out.append([pdf, page])
            break
    print pdf, 'done'


#write to a csv file
fileName = sys.argv[3]
if not fileName.endswith('csv'):
    print 'A valid file should be in .csv format.'
    sys.exit()

with open(fileName,'wb') as csvfile:
    writer = csv.writer(csvfile,delimiter=',', quotechar = '|')
    writer.writerows(out)
