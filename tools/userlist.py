#!/usr/bin/python
import sys
sys.path.append("..")

import userman.model.user
import re

result = {}

for curUser in userman.model.user.GetAllUsers():
    if re.search('/export/gebruikers/([0-9BC]+)/.*', curUser.homeDirectoryAnk):
        year = re.search('/export/gebruikers/([0-9BC]+)/.*', curUser.homeDirectoryAnk).group(1)
        if not year in result:
    	    result[year] = []
	result[year] += [curUser]
    elif re.search('/export/gebruikers/staff/.*', curUser.homeDirectoryAnk):
	if not 'staff' in result:
	    result['staff'] = []
	result['staff'] += [curUser]
    elif re.search('/export/gebruikers/misc/.*', curUser.homeDirectoryAnk):
        if not 'misc' in result:
    	    result['misc'] = []
	result['misc'] += [curUser]
    else:
        print 'Skipped:', curUser.uid, curUser.homeDirectoryAnk

#print result
for year,users in result.items():
    users.sort()
    print year, ':'
    for user in users:
	print user.uid, ':', user.gecos['full_name']
    print
