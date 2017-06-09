import csv

out = []

f = open('rawPapers.txt','r')

out = f.readlines()

whole = ''.join(out).split('|||')
whole = whole[1:]


for i in range(len(whole)/2):
    if int(whole[i*2]) == 7:
        print whole[i*2+1]
