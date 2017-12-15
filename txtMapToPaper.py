#Muwei Zheng
#It mainly will mapping the txt file name back to each paper and
# store the txt name as a feature of the paper
#It takes two arguments:
#1. The name of the csv file which contains all the paper information
#2. The folder of the txt files wanted to be match

import csv, sys, os, re, helper

#Create variables
#incsv: input csv file; inFolder: input folder;
#papersInfo: list to store papers information.
#txtL; txt file list
#txtDict: txt dictionary with format[10-line string: file name]
#unMap: list used to store the txt file name that fail to find a match
#header: csv file header
#ind: the index of column to store the txt name
#conflict: store the conflict names
incsv, inFolder = sys.argv[1], sys.argv[2]
papersInfo = []
txtL = []
txtDict = dict()
unMap = []
header = []
ind = 0
conflict = {}


#check whether the input arguments are correct or not
if not incsv.endswith('.csv'):
    print 'Input', incsv, 'is not a csv file.'
    sys.exit(1)


#Open the csv file
with open(incsv, 'rU') as cf:
    rd = csv.reader(cf, delimiter=',', quotechar='"')
    header = rd.next()
    ind = header.index('txtName')
    for r in rd:
        papersInfo.append(r)




#Open the folder and read every txt file and store the first 10 lines into txtDict
try:
    txtL = [x for x in os.listdir('./'+inFolder) if x.endswith('.txt')]
except:
    print "Cannot find folder:", inFolder
    sys.exit(1)

for txt in txtL:
    f = open('./'+inFolder+'/'+txt, 'r')
    text = f.read()
    f.close()
    headstring = text[:500].replace('\n', ' ')
    headstring = helper.normalizeChar(headstring)
    headstring = helper.cleanStr(headstring)
    txtDict[headstring] = txt
print 'The total num of txt files:', len(txtDict.values())

unMap = txtL[:]


#find the match paper for each txt file
for i in range(len(papersInfo)):
    name = papersInfo[i][0]
    name = helper.cleanStr(name)
    txtName = papersInfo[i][ind]
    if txtName != '':
        continue
    for head in txtDict.keys():
        if name in head:
            txtName = papersInfo[i][ind]
            txt = txtDict[head]
            if txtName != '':
                if name in conflict:
                    conflict[name].append(txt)
                else:
                    conflict[name] = [txtName, txt]
            else:
                papersInfo[i][ind] = txt
                del txtDict[head]
                unMap.remove(txt)

print 'num of unmap:', len(unMap)
print 'num of conflicts:', len(conflict.keys())
sample = txtDict.keys()[0]
print sample, txtDict[sample]

#output unmapped txt file names into "failMap.txt"
f = open('failMap.txt', 'w')
f.write('\n'.join(unMap))
f.close()

#save back the csv file.
out = [header]
out += papersInfo
with open('mapetxt2.csv', 'w') as cf:
    wt = csv.writer(cf, delimiter=',', quotechar='"')
    wt.writerows(out)

#save the conflict files:
f = open('mapConflict.txt', 'w')
out = [x+': '+' '.join(conflict[x]) for x in conflict.keys() ]
f.write('\n'.join(out))
f.close()
