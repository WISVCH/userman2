#!/usr/bin/env python
import ldap
import re
from ldapconn import LDAPConn
from ldap.cidict import cidict
from django.conf import settings

class Group (LDAPConn):
    def __init__ (self, dn, attrs = False):
	LDAPConn.__init__(self)
	self.dn = dn

	if attrs:
	    self.__attrs = attrs
	    return

	self.connectRoot()

	res = self.l.search_s(self.dn, ldap.SCOPE_BASE)
	(_, attrs) = res[0]
	self.__attrs = cidict(attrs)

    def _get_cn(self):
	return self.__attrs["cn"][0]
    cn = property (_get_cn)

#    def getParent(self):
#	return self.dn.split(',')[1].split('=')[1]

#    def getGIDNumber(self):
#	return int(self.attrs["gidNumber"][0])

    def __str__(self):
	return "Group: [ dn:'" + self.dn + ", cn:'" + self.cn + "' ]"

def fromCN(cn):
    try:
	return User("cn=" + cn + "," + settings.LDAP_GROUPDN)
    except ldap.LDAPError, e:
	raise Exception, "Error finding group " + cn

def getAllGroups(filter_data=False):
    ld = LDAPConn()
    ld.connectRoot()
    res = ld.l.search_s(settings.LDAP_GROUPDN, ldap.SCOPE_ONELEVEL)
    res.sort()
    ret = {"None": [Group(dn, attrs) for (dn, attrs) in res if "posixGroup" in attrs["objectClass"] ] }
    children = [(dn, attrs["ou"][0]) for (dn, attrs) in res if "organizationalUnit" in attrs["objectClass"] ]
    for child in children:
	res = ld.l.search_s(child[0], ldap.SCOPE_ONELEVEL)
	res.sort()
	ret[child[1]] = [Group(dn, attrs) for (dn, attrs) in res if "posixGroup" in attrs["objectClass"]]
    return ret
    