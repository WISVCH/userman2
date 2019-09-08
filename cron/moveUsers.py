#!/usr/bin/env python3

import string
from config import *
from user import User
import re
import os


def moveUser(user):
    if user.getUID() == "root":
        return

    p = re.compile("([1|2][9|0][9|0]\d)")
    m = p.search(user.getHomeDirectory("ank.chnet"))
    if m:
        return
    #    m = p.search (user.getHomeDirectory("ch.chnet"))
    #    if not m:
    #        return

    oldHomeDir = user.getHomeDirectory("ank.chnet")
    #    newHomeDir = "/export/gebruikers/" + m.group() + "/" + user.getUID()
    newHomeDir = "/export/gebruikers/" + "BC" + "/" + user.getUID()

    if os.path.exists(oldHomeDir):
        print(oldHomeDir)

    print("Moving User:", user.getUID(), "from", oldHomeDir, "to", newHomeDir)
    user.setHomeDirectory("ank.chnet", newHomeDir)
    os.makedirs(newHomeDir)
    os.rename(oldHomeDir, newHomeDir)


# This script can be called individually, to manually regen login scripts
if __name__ == "__main__":
    import sys
    import ldap

    if len(sys.argv) != 2:
        print("Usage: " + sys.argv[0] + " <username | --all>")
        sys.exit(1)

    try:
        l = ldap.initialize(ldapServername)

        try:
            l.simple_bind_s(ldapUsername, ldapPass)
        except ldap.LDAPError as e:
            sys.stderr.write("Fatal Error.\n")
            sys.stderr.write("Error: %s" % e)
            sys.exit()

        if sys.argv[1] == "--all":
            res = l.search_s(ldapUserOU, ldap.SCOPE_ONELEVEL)
            for (dn, _) in res:
                user = User(l, dn)
                moveUser(user)

        else:
            user = User(l, "uid=" + sys.argv[1] + "," + ldapUserOU)
            moveUser(user)

    finally:
        try:
            l.unbind()
        except ldap.LDAPError as e:
            pass
