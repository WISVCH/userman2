#!/usr/bin/env python
import os
import re
import subprocess

import ldap
from django.conf import settings
from ldap.cidict import cidict

from ldapconn import LDAPConn
from userman2.model import action


class Group(LDAPConn):
    def __init__(self, dn, attrs=False):
        LDAPConn.__init__(self)
        self.dn = dn

        if attrs:
            self.__attrs = cidict(attrs)
            return

        self.connectRoot()

        res = self.l.search_s(self.dn, ldap.SCOPE_BASE)
        (_, attrs) = res[0]
        self.__attrs = cidict(attrs)

    def _get_cn(self):
        return self.__attrs["cn"][0]

    cn = property(_get_cn)

    def _get_parent(self):
        parent = self.dn.split(',')[1].split('=')[1]
        if parent == "Group":
            return "None"
        return parent

    parent = property(_get_parent)

    def _get_gidNumber(self):
        return int(self.__attrs["gidNumber"][0])

    gidNumber = property(_get_gidNumber)

    def _get_members(self):
        if 'memberuid' in self.__attrs:
            return self.__attrs["memberUid"]
        return []

    members = property(_get_members)

    def removeMember(self, member):
        self.removeEntries({'memberUid': member})

    def addMember(self, member):
        self.addEntries({'memberUid': member})

    def remove(self):
        if self.parent == "None" or self.parent == "Besturen":
            ld = LDAPConn()
            ld.connectRoot()
            ld.l.delete_s(self.dn)
        else:
            removeAction = action.Add('removeGroup', 'frans.chnet', self.dn,
                                      'Remove group entry in LDAP for ' + self.dn)
            removeAnkGroupDirAction = self.removeGroupDir('ank.chnet', removeAction)
            removeAnkGroupDirAction.locked = False
            removeAction.locked = False

    def getPrimaryMembers(self):
        from userman2.model import user
        return user.GetPrimaryMembersForGid(self.gidNumber)

    def removeGroupDir(self, host, parent):
        return action.Add('removeGroupDir', host, self.dn, 'Remove group directory on ank.chnet for ' + self.cn, parent)

    def createGroupDir(self, host):
        return action.Add('createGroupDir', host, self.dn, "Create group directory on host " + host + " for " + self.cn)

    def addGroupMapping(self):
        raise Exception, "Should create samba group mapping"

    def __str__(self):
        return "Group: [ dn:'" + self.dn + ", cn:'" + self.cn + "' ]"


def FromCN(cn):
    ld = LDAPConn()
    ld.connectAnon()
    res = ld.l.search_s(settings.LDAP_GROUPDN, ldap.SCOPE_SUBTREE, "cn=" + cn)
    if not res:
        raise Exception, "Error finding group " + cn

    (dn, attrs) = res[0]
    return Group(dn, attrs)


def GetAllGroups(filter_data=False):
    """Returns all groups under LDAP_GROUPDN, in a dictionary sorted by their ou"""
    ld = LDAPConn()
    ld.connectAnon()

    if filter_data:
        filter_string = "(&"
        if filter_data['uid']:
            filter_string += "(memberUid=*" + filter_data['uid'] + "*)"
        if filter_data['cn']:
            filter_string += "(cn=*" + filter_data['cn'] + "*)"
        filter_string += "(objectClass=posixGroup))"
    else:
        filter_string = "(objectClass=posixGroup)"

    res = ld.l.search_s(
        settings.LDAP_GROUPDN, ldap.SCOPE_SUBTREE, filter_string)

    res.sort()
    ret = {}
    for dn, attrs in res:
        group = Group(dn, attrs)
        if not group.parent in ret:
            ret[group.parent] = []
        ret[group.parent] += [group]
    return ret


def Groupname(value):
    ld = LDAPConn()
    ld.connectAnon()
    res = ld.l.search_s(
        settings.LDAP_GROUPDN, ldap.SCOPE_SUBTREE, "(gidNumber=" + value + ")")
    if len(res) > 0 and 'cn' in res[0][1]:
        return res[0][1]['cn'][0]
    else:
        return 'unknown group'


def GetCnForUid(uid):
    ld = LDAPConn()
    ld.connectAnon()

    res = ld.l.search_s(
        settings.LDAP_GROUPDN, ldap.SCOPE_SUBTREE, 'memberUid=' + uid)
    return [attribs["cn"][0] for dn, attribs in res]


def GetParents():
    """Returns the possible parents of a group"""
    ld = LDAPConn()
    ld.connectAnon()

    filter_string = "(objectClass=organizationalUnit)"
    res = ld.l.search_s(settings.LDAP_GROUPDN, ldap.SCOPE_ONELEVEL, filter_string)
    res = [attribs['ou'][0] for (_, attribs) in res]
    res.append('None')
    res.sort()
    return res


def Exists(cn):
    ld = LDAPConn()
    ld.connectAnon()
    res = ld.l.search_s(settings.LDAP_GROUPDN, ldap.SCOPE_SUBTREE, "cn=" + cn)
    return len(res) != 0


def GetFreeGIDNumber():
    ld = LDAPConn()
    ld.connectAnon()
    for i in reversed(range(settings.MIN_GROUP_ID, settings.MAX_GROUP_ID + 1)):
        res = ld.l.search_s(settings.LDAP_GROUPDN, ldap.SCOPE_SUBTREE, "gidNumber=" + str(i))
        if len(res) > 0:
            if i == settings.MAX_GROUP_ID:
                raise Exception("No more free group IDs")
            else:
                return i + 1

    # This should never happen: if MAX_GROUP_ID is not taken we should have a free GID
    raise AssertionError("Failure in finding free group ID")


def Add(parent, cn):
    ld = LDAPConn()
    ld.connectRoot()

    ou = '' if parent == 'None' else ',ou=' + parent
    dn = 'cn=' + cn + ou + ',' + settings.LDAP_GROUPDN
    gidNumber = GetFreeGIDNumber()
    ld.addObject(dn, {'objectClass': 'posixGroup', 'cn': cn, 'gidNumber': str(gidNumber)})
    retcode = subprocess.call('sudo ' + os.path.join(
        settings.ROOT_PATH, 'scripts/addgroupmapping') + ' ' + re.escape(cn) + ' ' + re.escape(cn), shell=True)
    if retcode != 0:
        raise Exception("Child failed")
    return FromCN(cn)
