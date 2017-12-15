import helper

reqs, header = helper.readCSV('./request/requestApprovedAcademia.csv')

thesis = [' thesis', '-thesis', ' master', 'doctora', 'phd ',' ph.d', ' undergrad',' class.',' class ', 'graduate','independent study','student']

keywordslist = ['student research','evaluating something','develop something','new approach','related to previous work or datasets',
        'effect or improve','analysis on datasets','project relating to detection', 'explain usage']

keywords = {}
keywords['student research'] = thesis
keywords['evaluating something'] = ['evaluat', ' test', 'validat', 'verify','testing']
keywords['new approach'] = ['classifi', ' model', 'system', 'platform', 'algorithm']
keywords['related to previous work or datasets'] = ['recreate', 'update', 'review']
keywords['develop something'] = ['develop','train']
keywords['effect or improve'] = ['effect','improve']
#keywords['extract'] = ['extract']
keywords['analysis on datasets'] = ['analys', 'analyz', 'examin','correlate','find','compare','comparison','investigate','mine','integrate']
keywords['project relating to detection'] = ['detection','determin']
keywords['explain usage'] = ['use','help']

reqInd = header.index('reason')
userInd = header.index('idUser')

finished = set()
out = [['reason', 'type','keyWord']]

for req in reqs:
    reason = req[reqInd]
    user = req[userInd]
    unique = (reason, user)
    if unique in finished:
        continue
    finished.add(unique)
    result = [reason]
    reason = reason.lower()
    for keyword in keywordslist:
        flag = False
        for word in keywords[keyword]:
            if word in reason:
                result.append(keyword)
                result.append(word)
                flag = True
                break
        if flag:
            break
    if len(result) == 1:
        result.append('others')
        result.append('others')
    out.append(result)

helper.writeCSV('./testout2.csv',out)
