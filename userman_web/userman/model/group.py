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

    def _get_parent(self):
	return self.dn.split(',')[1].split('=')[1]

    def _get_type(self):
        parent = self._get_parent()
        if parent == "Group":
            return "None"
        return parent
    type = property(_get_type)

    def _get_gidNumber(self):
	return int(self.__attrs["gidNumber"][0])
    gidNumber = property(_get_gidNumber)

    def _get_members(self):
	if 'memberUid' in self.__attrs:
    	    return self.__attrs["memberUid"]
	return []
    members = property(_get_members)

    def getPrimaryMembers(self):
        from userman.model import user
        return user.getPrimaryMembersForGid(self.gidNumber)

    def __str__(self):
	return "Group: [ dn:'" + self.dn + ", cn:'" + self.cn + "' ]"

def fromCN(cn):
    ld = LDAPConn()
    ld.connectAnon()
    res = ld.l.search_s(settings.LDAP_GROUPDN, ldap.SCOPE_SUBTREE, "cn="+cn)
    if not res:
        raise Exception, "Error finding group " + cn

    (dn, attrs) = res[0]
    return Group(dn, attrs)

def getAllGroups(filter_data=False):
    ld = LDAPConn()
    ld.connectAnon()
    res = ld.l.search_s(settings.LDAP_GROUPDN, ldap.SCOPE_ONELEVEL)
    res.sort()
    ret = {"None": [Group(dn, attrs) for (dn, attrs) in res if "posixGroup" in attrs["objectClass"] ] }
    children = [(dn, attrs["ou"][0]) for (dn, attrs) in res if "organizationalUnit" in attrs["objectClass"] ]
    for child in children:
	res = ld.l.search_s(child[0], ldap.SCOPE_ONELEVEL)
	res.sort()
	ret[child[1]] = [Group(dn, attrs) for (dn, attrs) in res if "posixGroup" in attrs["objectClass"]]
    return ret

def groupname(value):
    ld = LDAPConn()
    ld.connectAnon()
    res = ld.l.search_s(settings.LDAP_GROUPDN, ldap.SCOPE_SUBTREE, "(gidNumber=" +value +")")
    if len(res) > 0 and 'cn' in res[0][1]:
	return res[0][1]['cn'][0]
    else:
	return 'unknown group'

def getCnForUid(uid): 
    ld = LDAPConn()
    ld.connectAnon()
    res = ld.l.search_s(settings.LDAP_GROUPDN, ldap.SCOPE_SUBTREE, 'memberUid=' + uid)
    return [ attribs["cn"][0] for dn, attribs in res ]
