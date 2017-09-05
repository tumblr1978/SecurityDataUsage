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
#    APWG Symposium on Electronic Crime Research,ecrime
#    Cyber Security Experimentation and Test Workshop at USENIX,usscset
#    International Conference on Financial Cryptography and Data Security,fc (2012-2016)
#
#Example: python papersDownloader.py downloadTest.csv papers


import csv, os, subprocess, time, sys
from random import randint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

#open the file given by the command line argument
fileName = sys.argv[1]
if not fileName.endswith('csv'):
    print 'A valid file should be in .csv format.'
    sys.exit()


#extract all paper info from the spreadsheet
paperInfo =  []
with open(fileName, 'rb') as csvfile:
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

#open chrome
driver = webdriver.Chrome(chrome_options=chromeOptions)
paperNum = len(os.listdir('./'+folder))
print 'start downloading papers...'
last_conf = ''
for paper in paperInfo:
    name, url, conf, year = paper[0], paper[1], paper[2], paper[3]
    elem = ''

    if conf == last_conf:
        time.sleep(0.001*randint(20000,40000))
    else:
        last_conf = conf
        time.sleep(0.001*randint(10000,20000))
    try:
        if url.endswith('.pdf'):
            driver.get(url)
            continue

        if not conf == 'fc' and not conf == 'fcw': #for not fc conferences
            driver.get(url)
            if conf == 'uss' or conf == 'usscset':
                elem = driver.find_element_by_class_name("file")
            elif conf == 'ccs' or conf == 'ccsaisec':
                page = driver.page_source
                ind = page.find('citation_pdf_url')
                start = page.find('http', ind)
                end = page.find('"', start)
                driver.get(page[start:end])

            elif conf == 'ndss':
                elem = driver.find_element_by_link_text("Download File")
            elif conf == 'sp':
                url=driver.current_url
                routes = url.split('/')
                paperID = routes[4]
                time.sleep(0.001*randint(4000,6000))
                driver.get('http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber='+str(paperID))
            elif conf != 'fc':
                print 'Cannot handle conference:', conf

        else:  #for fc conference
            if year not in fc.keys():
                print 'Need to add', year+'th', 'Financial Cryptography conference webpage url into script.'
                print name
                continue
            if conf == 'fc':
                driver.get(fc[year])
            else:
                if year not in fcw.keys():
                    print 'Need to add', year+ 'th','Financial Cryptography conference bitcoin and block chain workshop webpage url into script.'
                    print name
                    continue
                driver.get(fcw[year])
            page = driver.page_source
            if len(name) > 10:
                ind = page.find(name[:10])
            if year != '2014':
                start = page.rfind('>',0,ind)
                end = page.find('<',ind)
                elem = driver.find_element_by_link_text(page[start+1:end])
            else:
                start = page.frind('"', ind)
                end = page.find('"', start+1)
                driver.get('http://fc14.ifca.ai/'+page[start+1:end])

        if elem != '':
            time.sleep(0.001*randint(4000,6000))
            elem.click()

        if len(os.listdir('./'+folder)) == (paperNum+1):
            paperNum += 1
        elif len(os.listdir('./'+folder)) == (paperNum):
            print 'Failed download paper:', name
        else:
            print 'Error!'
    except:
        print name

driver.close()

print ""
print 'finish downloading'


