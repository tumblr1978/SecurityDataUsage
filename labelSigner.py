import csv

papers = []

with open('sample.csv','rb') as cf:
    reader = csv.reader(cf, delimiter=',', quotechar='"')
    for row in reader:
        papers.append(row)

for i in range(len(papers)):
    if papers[i][4] == 'Yes' or papers[i][6] == 'Yes':
        papers[i].append('Data')
    else:
        papers[i].append('Non-data')

with open('sample.csv', 'wb') as cf:
    writer = csv.writer(cf, delimiter=',', quotechar='"')
    writer.writerows(papers)
