#Muwei Zheng
#
#This script takes two arguments:
#1. The name of the pdf file or the pdf folder that we want to convert to plain txt
#2. The output folder name that we want to save our converted txt files
#
#The script will convert all pdfs in the given folder into plain txt and store them in
#a new folder
#
#Example: python pdfParser.py papersTotal papersTotalTXT

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


#The convert method. It should convert the pdf three times, and save the one has the largest length
def convert(path):
    len_map = {}
    for i in range(3):
        text = convert_pdf_to_txt(path)
        length = len(text)
        len_map[length] = text
    if len(len_map.keys()) > 1:
        print 'IT'
        maxlen = max(len_map.keys())
        return len_map[maxlen]
    else:
        return len_map.values()[0]


#Method to check if the folder exist:
def checkFolder(path):
    folder = path
    if not folder.isalnum():
        print 'output folder name should be alphanumeric and there is at least one character. System aborted'
        sys.exit(1)
    if folder not in os.listdir('./'):
        return False
    return True


#The write method, write the out put into the given folder.
def writeOut(txt, name, folder):
    f = open('./'+folder+'/'+name, 'w')
    f.write(txt)
    f.close()



#Check if the input argument is a folder or a file
#if it is a file, then directly convert it into txt.
outFolder = sys.argv[2]
if sys.argv[1].endswith('.pdf'):
    if not checkFolder(outFolder):
        os.mkdir(outFolder)
    txt = convert(sys.argv[1])
    filename = sys.argv[1][:-3]+'txt'
    writeOut(txt, filename, outFolder)
#if it is a folder, then convert every pdf files inside the folder into txt.
else:
    inFolder = sys.argv[1]
    if not checkFolder(inFolder):
        print 'The input folder', inFolder, "doesn't exist."
        sys.exit(1)
    pdfs = [x for x in os.listdir(inFolder) if x.endswith('.pdf')]
    if not checkFolder(outFolder):
        os.mkdir(outFolder)
    #check all files in the output folder
    exist = set([x for x in os.listdir(outFolder) if x.endswith('.txt')])
    for pdf in pdfs:
        #if the file already in the output folder, skip it
        if pdf[:-3]+'txt' in exist:
            continue
        try:
            txt = convert('./'+inFolder+'/'+pdf)
            filename = pdf[:-3]+'txt'
            writeOut(txt, filename, outFolder)
        except:
            print pdf
