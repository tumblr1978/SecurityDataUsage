import unicodedata

out = []
f = open('rawPapers.txt','r')
out = f.readlines()
f.close()

for i in range(len(out)):
    out[i] = unicode(out[i], 'utf-8')
    out[i] = unicodedata.normalize('NFKD', out[i])
    out[i] = out[i].encode('utf-8')

outPut = ' '.join(''.join(out).split('\n'))
outPut = outPut.replace('  ',' ')
f = open('rawPapers2.txt', 'w')
f.write(outPut)
f.close()

