import re, csv

#helper function to check if there is numbers in it, return the position of first match
def check(s):
    obj = re.search(r'[ ,][0-9][0-9]([0-9])+ ', s)
    if obj:
        start = obj.start(0)
        end = obj.end(0)
        obj2 = re.search(r' 19[0-9][0-9] | 20[0-2][0-9]' ,s[start-1:end+1])
        obj3 = re.search(r'volume| acm |bits|bytes',s[start-7:end+6])
        if obj2 or obj3:
            return -1
        else:
            return obj.start(0)
    else:
        return -1

#open the file contains all of the papers
papers =[]
try:
    fh = open('rawPapers.txt', 'r')
    papers = ''.join(fh.readlines()).split('|||')[1:]
except IOError as err:
    print err

keys = ['dataset',' alexa ','families','exploits','vulnerabilities','figures','survey','census','crawl','collect']

results = {}
out = []
for i in range(len(papers)):
    paper = papers[i]
    results[i] = ['No','\\']
    index = check(paper)
    if index != -1:
        results[i][0] = 'Yes'
        results[i][1] = ''
        results[i][1] = results[i][1] + paper[index-100:index+100]+'\n'
        results[i].append('number')
    for key in keys:
        if key in paper:
            if results[i][0] == 'No':
                results[i][0] = 'Yes'
                results[i][1] = ''
            index = paper.index(key)
            results[i].append(key)
            results[i][1] = results[i][1] + paper[index-100:index+100]+'\n'
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
