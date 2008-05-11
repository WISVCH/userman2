#!/usr/bin/env python
""" Function to Generate a loginscript for a user. This script can be run to generate """

import string
from config import *
from user import User

def generateLoginScript(user):
    """Generate a login script for the specified user"""
    username = user.getUID()
    groups = user.getGroups()
    
    # Read loginScript template
    f = open(loginScriptTemplate)
    loginScript = f.read()
    f.close()

    # Generate rest of loginScript
    loginScript += "XCOPY \\\\ANK\\netlogon\\loginscripts\\" + username + ".kix %WINDIR%\\system\\login.kix /H /R /V /Y\n"
    loginScript += "%WINDIR%\\SYSTEM32\\KIX32.EXE %WINDIR%\\system\\login.kix\n"

    f = open(loginScriptDir + "loginscripts/" + username + ".cmd", "w")
    f.write (string.replace(loginScript, '\n', '\r\n'))
    f.close()

    # Read kix templates    
    f = open(loginScriptKixTemplate)
    loginKix = f.read()
    f.close()

    f = open(loginScriptKixEndTemplate)
    loginKixEnd = f.read()
    f.close()

    # Generate default mappings        
    loginKix += "use h: \"\\\\ANK\\" + username +"\"\n"
    loginKix += "use z: \"\\\\CHBAK\\" + username +"\"\n"
    loginKix += "use p: \"\\\\ANK\\public\"\n"
    loginKix += "SLEEP 5\n"

    # Generate group mappings
    for group in groups:
	if group == "bestuur":
	    loginKix += "use t: \"\\\\ANK\\bestuur\"\n"
	    loginKix += "use s: \"\\\\ANK\\sponsor\"\n"
	elif group == "exchange":
	    loginKix += "use l: \"\\\\LEON\\bestuur_48\"\n"
	elif group == "sponsoradmin":
	    loginKix += "use s: \"\\\\ANK\\sponsor\"\n"
	elif group == "sponsorread":
	    loginKix += "use s: \"\\\\ANK\\sponsor\"\n"
	elif group == "delftread":
	    loginKix += "use s: \"\\\\ANK\\sponsor\"\n"
	elif group == "oudbestuur":
	    loginKix += "use u: \"\\\\ANK\\particul\"\n"
	elif group == "ddb":
	    loginKix += "use w: \"\\\\CHBAK\\ddb_share\"\n"
	elif group == "flitcie":
	    loginKix += "use x: \"\\\\CHBAK\\flitcie_share\"\n"
	elif group == "useradmin" or group == "powusers" or group == "domusers" or group == "guests" or group == "machines":
	    continue
	elif group == "staff" or group == "users" or group == "root":
	    continue
	elif group == "voorzitter" or group == "penningmeester" or group == "secretaris" or group == "coi" or group == "cpr" or group == "cow" or group == "coe":
	    continue
	elif group == "bitenddb" or group == "tentamen":
	    continue
	else:
	    loginKix += "gosub getnextdrive\n"
	    loginKix += "use $Y \"\\\\ANK\\" + group + "\"\n"

    loginKix += loginKixEnd

    f = open(loginScriptDir + "loginscripts/" + username + ".kix", "w")
    f.write (string.replace(loginKix, '\n', '\r\n'))
    f.close()

# This script can be called individually, to manually regen login scripts
if __name__ == "__main__":
    import sys, ldap
    if len(sys.argv) != 2:
	print "Usage: " + sys.argv[0] + " <username | --all>"
    
    try:
	l = ldap.initialize(ldapServername)

	try:
    	    l.simple_bind_s(ldapUsername, ldapPass)
	except ldap.LDAPError, e:
    	    sys.stderr.write("Fatal Error.\n")
    	    if type(e.message) == dict:
        	for (k, v) in e.message.iteritems():
            	    sys.stderr.write("%s: %sn" % (k, v))
    	    else:
        	sys.stderr.write("Error: %sn" % e.message);

    	    sys.exit()
	
	if (sys.argv[1] == "--all"):
	    res = l.search_s(ldapUserOU, ldap.SCOPE_ONELEVEL)
    	    for (dn, _) in res:
		user = User (l, dn)
		print "Generating login script for user: " + str(user)
		generateLoginScript (user);
		
	else:
	    user = User (l, "uid=" + sys.argv[1] + "," + ldapUserOU)
	    print "Generating login script for user: " + str(user)
	    generateLoginScript (user);

    finally:
	try:
    	    l.unbind()
	except ldap.LDAPError, e:
    	    pass
