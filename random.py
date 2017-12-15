import csv, helper, re

header = []
info = {}
wantToMap = []
lost = []
header1 = []

def replace(string):
    string = re.sub('[^0-9a-zA-Z]+', ' ', string)
    string = re.sub(' +', ' ', string)
    return string.strip().lower()


with open('400papersCitations.csv','r') as cf:
    rd = csv.reader(cf)
    header1 = rd.next()
    count = 0
    for r in rd:
        name = replace(r[0])
        info[name] = count
        wantToMap.append(r)
        count += 1

with open('muweiprove.csv', 'r') as cf:
    rd = csv.reader(cf)
    header = rd.next()
    for r in rd:
        lost.append(r)

indO = header.index('Origin')

data = {}
error = []
for i in range(len(lost)):
    title = replace(lost[i][1])
    org = lost[i][6]
    pub = lost[i][8]
    if title in info.keys():
        if title not in data:
            data[title] = 'Yes'
        if pub == 'No':
            data[title] = 'No'
    else:
        error.append(lost[i])


for title in data.keys():
    wantToMap[info[title]].append(data[title])

header1.append('Public')
out = [header1]
out += wantToMap
with open('400papersCitations2.csv', 'wb') as cf:
    wr = csv.writer(cf)
    wr.writerows(out)

helper.writeCSV('error.csv', error)
