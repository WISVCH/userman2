#!/usr/bin/env python
import config
import string
import ldap
from ldap.cidict import cidict


class Group:

    def __init__(self, l, dn):
        self.l = l
        self.dn = dn
        res = l.search_s(self.dn, ldap.SCOPE_BASE)
        (_, attrs) = res[0]
        self.attrs = cidict(attrs)

    def getCN(self):
        return self.attrs["cn"][0]

    def getParent(self):
        return self.dn.split(',')[1].split('=')[1]

    def getGIDNumber(self):
        return int(self.attrs["gidNumber"][0])

    def __str__(self):
        return "Group: [ dn:'" + self.dn + ", cn:'" + self.attrs["cn"][0] + "' ]"
