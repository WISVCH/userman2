#!/usr/bin/env python
import ldap
import re
import random
from ldapconn import LDAPConn
from ldap.cidict import cidict
from django.conf import settings

class Action (LDAPConn):
    def __init__ (self, dn, attrs = False):
        LDAPConn.__init__(self)
        self.dn = dn

        if attrs:
            self.__attrs = cidict(attrs)
            return

        self._reload()

    def _reload(self):
        self.connectRoot()

        res = self.l.search_s(self.dn, ldap.SCOPE_BASE)
        (_, attrs) = res[0]
        self.__attrs = cidict(attrs)
        
    def _get_cn(self):
        return self.__attrs["cn"][0]
    cn = property (_get_cn)

    def _get_actionName(self):
        return self.__attrs["actionName"][0]
    actionName = property (_get_actionName)

    def _get_host(self):
        return self.__attrs["host"][0]
    host = property (_get_host)
    
    def _get_affectedDN(self):
        return self.__attrs['affectedDN'][0]
    def _set_affectedDN(self, dn):
        self.modifyEntries({'affectedDN': dn})
    
    affectedDN = property(_get_affectedDN,_set_affectedDN)
    
    def _get_arguments(self):
        return self.__attrs['arguments'][0]
    def _set_arguments(self, arg):
        self.modifyEntries({'arguments': arg})
    arguments = property(_get_arguments, _set_arguments)

    def _get_description(self):
        return self.__attrs['description'][0]
    def _set_description(self, description):
        self.modifyEntries({'description': description})
    description = property(_get_description, _set_description)

    def _get_locked(self):
        return self.__attrs["locked"][0] == "TRUE"
    def _set_locked(self, locked):
        if locked:
            self.modifyEntries({'actionLocked': 'TRUE'})
        else: 
            self.modifyEntries({'actionLocked': 'FALSE'})
        self._reload()
    locked = property(_get_locked,_set_locked, None, "Whether or not the action is locked")
    
    def remove(self):
        self.delObject()

    def __str__ (self):
        return "Action: " + self.dn + ", " + self.description

def FromCN(cn, ld=None):
    if not ld:
        ld = LDAPConn()
        ld.connectAnon()
    res = ld.l.search_s(settings.LDAP_ACTIONDN, ldap.SCOPE_SUBTREE, "cn=" + cn)
    if not res:
        raise Exception, "Error finding action " + cn

    (dn, attrs) = res[0]
    return Action(dn, attrs)

def Exists(cn, ld=None):
    if not ld:
        ld = LDAPConn()
        ld.connectAnon()
    res = ld.l.search_s(settings.LDAP_ACTIONDN, ldap.SCOPE_SUBTREE, "cn="+cn)
    return len(res) != 0 

def Add(actionName, host, parentDN=False):
    ld = LDAPConn()
    ld.connectRoot()

    while True:
        cn = str(random.randint(1, 10000))
        if not Exists(cn, ld):
            break;

    if parentDN:
        dn = 'cn=' + cn + ',' + parentDN
    else: 
        dn = 'cn=' + cn + ',' + settings.LDAP_ACTIONDN
    
    ld.addObject(dn, {'objectClass': 'chAction', 'cn': cn, 'actionName': actionName, 'host': host, 'actionLocked': 'TRUE'})

    return FromCN(cn, ld)
    