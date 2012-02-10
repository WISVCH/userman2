#!/usr/bin/python
import sys
import time
import re
import subprocess
import time
import os

sys.path.append("..")

import userman2.model.user
import lastlog

result = {}

for curUser in userman2.model.user.GetAllUsers():
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

# Open lastlog file
try:
    llfile = open("/var/log/lastlog",'r')
except:
    print "Unable to open /var/log/lastlog"
    sys.exit(1)

print 'UID,Full Name,Homedir Year,Last Login,Last Mail Received,Forward'

# Print results
for year,users in result.items():
    users.sort()
#    print year, ':'
    for user in users:
        # Basic info
        print user.uid + ',', user.gecos['full_name'] + ',', year + ',',

        # lastlog
        record = lastlog.getrecord(llfile,user.uidNumber)
        if record and record[0] > 0:
            print time.strftime('%d %b %Y' , time.localtime(record[0])) + ',',
        else:
            print 'Never logged in' + ',',
        
        # Last mail message
        output = subprocess.Popen(["./mailboxinfo.pl", user.uid, "lastupdate"], stdout=subprocess.PIPE).communicate()[0]
        if output:
            match = re.search('(\d+-\w+-\d+ \d+:\d+:\d+)', output)
            stamp = time.strptime(match.group(), "%d-%b-%Y %H:%M:%S")
            print time.strftime('%d %b %Y' , time.strptime(match.group(), "%d-%b-%Y %H:%M:%S")) + ',',
        else:
            print 'No Mailbox' + ',',
            
        # .forward
        if os.path.exists(user.homeDirectoryCH + '/' + '.forward'):
            filehandle = open (user.homeDirectoryCH + '/' + '.forward')
            contents = ';'.join(filehandle.read().replace(',','').split())
            print contents
        else:
            print 'False'
    print

llfile.close()

