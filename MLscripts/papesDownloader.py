#Muwei Zheng
#
#This program takes a csv file as input,
#and then download all papers listed in the csv file into
#a given output folder. The file should have a header,
#And the header should be like 'PaperName, URL, Conference, Year'.
#Conferenc entry is the abbreviation from DBLP database,
#and the URL entry should be the url provided also by DBLP.
#It can only recognize and handle the following conferences:
#    ACM Conference on Computer and Communications Security,ccs
#    AI & Security Workshop at CCS,ccsaisec
#    USENIX Security Symposium,uss
#    IEEE Symposium on Security and Privacy,sp
#    Network and Distributed System Security Symposium,ndss
#    APWG Symposium on Electronic Crime Research,ecrime         (something error with ecrime. DBLP can't get all ecrime papers.)
#    Cyber Security Experimentation and Test Workshop at USENIX,usscset
#    International Conference on Financial Cryptography and Data Security,fc (2012-2016)
#    Workshop on Bitcoin and Bitcoin Chain Study at FC, fcw
#    Internet Measurement Conference, imc
#
#Example: python papersDownloader.py downloadTest.csv papers


import csv, os, subprocess, time, sys, re
from random import randint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

#allow maximum size of memory usage
csv.field_size_limit(sys.maxsize)


#open the file given by the command line argument
fileName = sys.argv[1]
if not fileName.endswith('csv'):
    print 'A valid file should be in .csv format.'
    sys.exit()


#extract all paper info from the spreadsheet
paperInfo =  []
with open(fileName, 'rU') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    reader.next() # remove header
    for row in reader:
        paperInfo.append(row)


#to check if the directory storing the papers exist
folder = sys.argv[2]
if not folder.isalnum():
    print 'output folder name should be alphanumeric and there is at least one character. System aborted'
    sys.exit()

if folder not in os.listdir('./'):
    os.mkdir(folder)


#set up a dictionary for fc conferences webpages:
fc = {'2016':'http://fc16.ifca.ai/program.html',
      '2015':'http://fc15.ifca.ai/schedule.html',
      '2014':'http://fc14.ifca.ai/program.html',  #different
      '2013':'http://fc13.ifca.ai/program.html',
      '2012':'http://fc12.ifca.ai/program.html'}

fcw = {'2016':'http://fc16.ifca.ai/bitcoin/program.html',
       '2015':'http://fc15.ifca.ai/bitcoin/schedule.html',
       '2014':'http://fc14.ifca.ai/bitcoin/program.html'}


#Start downloading papers

#set up chrome driver options:
#1. change download folder
#2. change download preference so that chrome will download pdf instead of reviewing it in new tab
prefs = {"download.default_directory":os.getcwd()+'/'+folder+'/',
        "plugins.always_open_pdf_externally": True}
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_experimental_option("prefs",prefs)

#create a error log to log all papers that fail downloading.
error = []

#create a log to log all successful papers.
success = []

#open chrome
driver = webdriver.Chrome(chrome_options=chromeOptions)
paperNum = len(os.listdir('./'+folder))
print 'start downloading papers...'
last_conf = ''
for paper in paperInfo:
    name, url, conf, year, pdfName = paper[0], paper[1], paper[2], paper[3], paper[-1]
    #check if the paper is already processed:
    if pdfName.endswith('.pdf'):
        continue
    elif pdfName != '':
        print 'strange pdf name:', name, ':', pdfName

    elem = ''

    if conf == last_conf:
        time.sleep(0.001*randint(20000,40000))
    else:
        last_conf = conf
        time.sleep(0.001*randint(10000,20000))
    try:
        if url.endswith('.pdf'):
            driver.get(url)
            success.append(paper)
            continue

        if not conf == 'fc' and not conf == 'fcw' and not conf == 'ndss': #for not fc conferences
            driver.get(url)
            if conf == 'uss' or conf == 'usscset':
                elem = driver.find_element_by_class_name("file")
                #scroll down to element
                driver.execute_script("arguments[0].scrollIntoView();", elem)
            elif conf in ['ccs', 'ccsaisec', 'imc']:
                page = driver.page_source
                ind = page.find('citation_pdf_url')
                start = page.find('http', ind)
                end = page.find('"', start)
                driver.get(page[start:end])
                success.append(paper)

            elif conf == 'sp':
                url=driver.current_url
                routes = url.split('/')
                paperID = routes[4]
                time.sleep(0.001*randint(4000,6000))
                driver.get('http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber='+str(paperID))
                success.append(paper)
            elif conf != 'fc':
                print 'Cannot handle conference:', conf
        elif conf == 'ndss':
            start = url.rfind('/')
            if year != '2014':
                url = 'https://www.ndss-symposium.org/ndss'+year+'/ndss-'+year+'-programme'+ url[start:]
            elif year == '2014':
                url = 'https://www.ndss-symposium.org/ndss2014/programme'+url[start:]
            driver.get(url)
            print url
            elem = driver.find_element_by_link_text("Paper")
            #scroll down to element
            driver.execute_script("arguments[0].scrollIntoView();", elem)
        else:  #for fc conference
            if year not in fc.keys():
                #print 'Need to add', year+'th', 'Financial Cryptography conference webpage url into script.'
                error.append(paper)
                #print name
                continue
            if conf == 'fc':
                driver.get(fc[year])
            else:
                if year not in fcw.keys():
                    error.append(paper)
                    #print 'Need to add', year+ 'th','Financial Cryptography conference bitcoin and block chain workshop webpage url into script.'
                    #print name
                    continue
                driver.get(fcw[year])
            page = driver.page_source
            if len(name) > 10:
                ind = re.search(name[:10], page, re.IGNORECASE).start()
                #print page[ind:ind+10]
            if year != '2014':
                start = page.rfind('>',0,ind)
                end = page.find('<',ind)
                #print page[start+1:end]
                elem = driver.find_element_by_link_text(page[start+1:end])
                #scroll down to element
                driver.execute_script("arguments[0].scrollIntoView();", elem)
            else:
                start = page.find('"', ind)
                end = page.find('"', start+1)
                driver.get('http://fc14.ifca.ai/'+page[start+1:end])
                success.append(paper)

        if elem != '':
            #print elem
            time.sleep(0.001*randint(4000,6000))
            elem.click()
            success.append(paper)

        if len(os.listdir('./'+folder)) == (paperNum+1):
            paperNum += 1
        elif len(os.listdir('./'+folder)) == (paperNum):
            print 'Failed download paper:', name
        else:
            print 'Error!'
    except Exception, err:
        print Exception, err
        error.append(paper)

driver.close()

#write error log to log file:
with open('downloaderr.csv','w') as cf:
    wr = csv.writer(cf, delimiter=',', quotechar='"')
    wr.writerows(error)

with open('downloadsuccess.csv','a') as cf:
    wr = csv.writer(cf, delimiter=',', quotechar='"')
    wr.writerows(success)

print ""
print 'finish downloading'
