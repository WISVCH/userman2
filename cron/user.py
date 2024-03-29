#!/usr/bin/env python3

import config
import ldap
from ldap.cidict import cidict


class User:
    """Represents a user in the ldap tree."""

    def __init__(self, l, dn):
        """Constructor, takes an ldap object, and the DN as an argument"""
        self.l = l
        self.dn = dn
        res = l.search_s(self.dn, ldap.SCOPE_BASE)
        (_, attrs) = res[0]
        self.attrs = cidict(attrs)

    def getUID(self):
        return self.attrs["uid"][0].decode()

    def getUIDNumber(self):
        return int(self.attrs["uidNumber"][0])

    def getGIDNumber(self):
        return int(self.attrs["gidNumber"][0])

    def getHomeDirectory(self):
        return self.attrs["homeDirectory"][0].decode()

    def getPrimaryGroup(self):
        res = self.l.search_s(config.ldapGroupOU, ldap.SCOPE_SUBTREE, "gidNumber=" + self.attrs["gidNumber"][0])
        if len(res) != 1:
            return "none"
        (_, attrs) = res[0]
        return attrs["cn"][0]

    def getSecondaryGroups(self):
        res = self.l.search_s(config.ldapGroupOU, ldap.SCOPE_SUBTREE, "memberUid=" + self.attrs["uid"][0])
        return [attribs["cn"][0] for dn, attribs in res]

    def getGroups(self):
        sec = self.getSecondaryGroups()
        pri = self.getPrimaryGroup()
        if pri in sec:
            return sec
        else:
            return sec + [pri]

    def __str__(self):
        return "User: [ dn:'" + self.dn + ", uid:'" + self.attrs["uid"][0] + "', cn:'" + self.attrs["cn"][0] + "' ]"
