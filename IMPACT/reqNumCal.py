import csv

ds = {}  # key: (organization, dataset_name) value: list from 2006-2017 requests and the end entry is the available year and its end year
add2007 = 0
with open('reqDesc.csv', 'rb') as cf:
    reader = csv.reader(cf, delimiter = ',', quotechar = '"')
    reader.next() #remove header
    for row in reader:
        ds[(row[0], row[2])] = [0]*12+[row[13][:4], row[14][:4]]
        if row[13][:4] == '2007':
            add2007 += 1

print 'add2007', add2007

count2007 = 0 #check how many times 2007 appears
req2007 = 0   #check how many requests for 2007
with open('reqMon.csv', 'rb') as cf:
    reader = csv.reader(cf, delimiter = ',', quotechar = '"')
    reader.next() #remove header
    for row in reader:
        key = (row[0], row[1])
        if key in ds:
            ds[key][int(row[2])-2006] += int(row[4])
        else:
            print 'Error:', key
        if row[2]=='2007':
            count2007 += 1
            req2007 += int(row[4])

print 'count2007', count2007
print 'req2007', req2007

header = ['Institution','Name']
outSumheader = ['']
for i in range(12):
    header.append(str(2006+i))
    outSumheader.append(str(2006+i))
header.append('availableYear')
header.append('EndYear')

out = [header]
outSum = [outSumheader]
outSum.append(['Num_datasets']+[0]*12)
outSum.append(['Num_requests']+[0]*12)

for key in ds.keys():
    value = ds[key]
    out.append([key[0],key[1]]+value)
    yearAvail = value[12]
    if not yearAvail.isdigit():
        print 'YearError:', key, yearAvail
        continue
    yearAvail = int(yearAvail)
    if yearAvail < 2006:
        outSum[1][1] += 1
    else:
        outSum[1][yearAvail-2005] += 1
    for i in range(12):
        outSum[2][i+1] += value[i]
    
    yearEnd = value[13]
    if yearEnd == 'NULL':
        continue
    if not yearEnd.isdigit():
        print 'YearEndError:', key, yearEnd
        continue
    yearEnd = int(yearEnd)
    if yearEnd < 2017 and yearEnd > 2006:
        outSum[1][yearEnd-2005] -= 1

for i in range(11):
    outSum[1][i+2] += outSum[1][i+1]

with open('reqsSum_year.csv','wb') as cf:
    wr = csv.writer(cf, delimiter = ',', quotechar = '"')
    wr.writerows(outSum)

with open('reqs_individual_year.csv','wb') as cf:
    wr = csv.writer(cf, delimiter = ',', quotechar = '"')
    wr.writerows(out)







            
        

