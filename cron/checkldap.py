#!/usr/bin/env python

#local imports
import config
from action import Action

import sys
import ldap
from ldap.cidict import cidict

def process(action):
    """Process a tree of actions from the bottom up."""

    # Process Children
    processed = True
    for child in action.getChildren():
        if not process(child):
	    processed = False

    # Check wether or not to proceed with execution
    if not processed or (action.getHost() != config.localHostname) or action.isLocked():
        return False

    # Try execution
    try: 
	action.lock()
	if action.execute():
	    action.mailAdmin("Action processed succesfully: " + action.getActionName(), "Admin,\n\nThe following action has been processed: " + str(action) + ".\n\nRegards,\nYour neighbourhood AI")
	    action.delete()	
	    return True
	else:
    	    action.unlock()
    	    return False
    except Exception, err:
	action.mailAdmin("An error occured while processing " + action.getActionName(), "Admin,\n\nAn error occured while processing " + str(action) + ".\nThe error was: " + str(err) + "\nThe Action has been locked, and must be re-enabled manually.\n\nRegards,\nYour neighbourhood AI")
	action.lock()
	

# Main loop, read pending actions and process them
try:
    l = ldap.initialize(config.ldapServername)

    try:
	l.simple_bind_s(config.ldapUsername, config.ldapPass)
    except ldap.LDAPError, e:
        sys.stderr.write("Fatal Error.n")
        if type(e.message) == dict:
            for (k, v) in e.message.iteritems():
                sys.stderr.write("%s: %sn" % (k, v))
        else:
            sys.stderr.write("Error: %sn" % e.message);

        sys.exit()

    res = l.search_s(config.ldapActionsOU, ldap.SCOPE_ONELEVEL)

    for (dn, _) in res:
    	action = Action(l, dn)
	process(action)

finally:
    try:
	l.unbind()
    except ldap.LDAPError, e:
	pass
