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
        parent = self.dn.split(',')[1].split('=')[1]
        if parent == "Group":
            return "None"
        return parent
    parent = property (_get_parent)

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
    """Returns all groups under LDAP_GROUPDN, in a dictionary sorted by their ou"""
    ld = LDAPConn()
    ld.connectAnon()

    if filter_data:
        filter_string = "(&"
        if filter_data['uid']: filter_string += "(memberUid=*" + filter_data['uid'] + "*)"
        if filter_data['cn']: filter_string += "(cn=*" + filter_data['cn'] + "*)"
        if filter_data['gidnumber']: filter_string += "(gidNumber=" + str(filter_data['gidnumber']) + ")"
        filter_string += "(objectClass=posixGroup))"
    else:
        filter_string += "(objectClass=posixGroup)"
        
    res = ld.l.search_s(settings.LDAP_GROUPDN, ldap.SCOPE_SUBTREE, filter_string)

    res.sort()
    ret = {}
    for dn, attrs in res:
        group = Group(dn, attrs)
        if not group.parent in ret:
            ret[group.parent] = []
        ret[group.parent] += [group]
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
