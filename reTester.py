import re

s1 = 'we have 1060 errors acros 88 '
s2 = 'sdfs [45]'
s3 = 'sdfsad 2021 '
s4 = 'sdfsfs 1,224,112 i'
s5 = 'sfsfdsfd 2345 bits'

def check(s):
    obj = re.search(r'[ ,][0-9]([0-9])+ ', s)
    if obj:
        start = obj.start(0)
        end = obj.end(0)
        obj2 = re.search(r' 19[0-9][0-9] | 20[0-2][0-9]' ,s[start-1:end+1])
        obj3 = re.search(r'volume| acm |bits|bytes',s[start-7:end+6])
        if obj2 or obj3:
            print -1
        else:
            print obj.start(0)
    else:
        print -1

check(s1)
check(s2)
check(s3)
check(s4)
check(s5)
