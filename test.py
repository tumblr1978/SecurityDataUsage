import csv, sys
csv.field_size_limit(sys.maxsize)

papers_info = []
with open('papers400_whole.csv','rU') as cf:
    rd = csv.reader(cf, delimiter=',', quotechar='|')
    for r in rd:
        papers_info.append(r)

f = open('dataNames.txt', 'r')
words = [x for x in f.read().split()]
f.close()

true = 0
false = 0

for paper in papers_info:
    name, text, label = paper[0], paper[1], paper[2]
    for word in words:
        if word in text:
            if label =='Data':
                true += 1
                break
            else:
                false += 1
                print name, word
                break

print 'true', true
print 'false', false
