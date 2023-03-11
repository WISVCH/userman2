#!/usr/bin/env python3
import sys
import traceback

import config
import ldap
from action import Action
from mail import mailAdmin


def process(action):
    """Process a tree of actions from the bottom up."""

    # Process Children
    processed = True
    for child in action.getChildren():
        if not process(child):
            processed = False

    # Check whether or not to proceed with execution
    if not processed or (action.getHost() != config.localHostname) or action.isLocked():
        return False

    # Try execution
    try:
        action.lock()
        if action.execute():
            mailAdmin("Success: " + action.getDescription(), "The following action has been processed: " + str(action))
            action.delete()
            return True
        else:
            action.unlock()
            return False
    except Exception:
        mailAdmin(
            "ERROR: " + action.getDescription(),
            "An error occurred while processing "
            + str(action)
            + "\n\n"
            + traceback.format_exc()
            + "\nThe Action has been locked, and must be re-enabled manually.",
        )
        action.lock()


# Main loop, read pending actions and process them
try:
    l = ldap.initialize(config.ldapServername)

    try:
        l.simple_bind_s(config.ldapUsername, config.ldapPass)
    except ldap.LDAPError as e:
        sys.stderr.write("Fatal Error.\n")
        sys.stderr.write("Error: %s" % e)
        sys.exit()

    res = l.search_s(config.ldapActionsOU, ldap.SCOPE_ONELEVEL)

    for dn, _ in res:
        action = Action(l, dn)
        process(action)

finally:
    try:
        l.unbind()
    except ldap.LDAPError as e:
        pass
