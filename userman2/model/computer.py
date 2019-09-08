import re

import ldap
from django.conf import settings
from ldap.cidict import cidict

from .ldapconn import LDAPConn
from userman2.scripts import execute_script


class Computer(LDAPConn):
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

    def _get_uid(self):
        return self.__attrs["uid"][0]

    uid = property(_get_uid)

    def _get_uidNumber(self):
        return int(self.__attrs["uidNumber"][0])

    uidNumber = property(_get_uidNumber)

    def remove(self):
        self.delObject()


def getAllComputers():
    """Returns all aliases under LDAP_ALIASDN, in a dictionary sorted by their ou"""
    ld = LDAPConn()
    ld.connectAnon()
    res = ld.l.search_s(settings.LDAP_COMPUTERDN, ldap.SCOPE_ONELEVEL)

    res.sort(key=lambda computer: computer[0].lower())
    ret = [Computer(dn, attrs) for (dn, attrs) in res]
    return ret


def FromUID(uid):
    try:
        return Computer("uid=" + uid + "," + settings.LDAP_COMPUTERDN)
    except ldap.LDAPError as e:
        raise Exception("Error finding computer " + uid)


def GetFreeUIDNumber():
    ld = LDAPConn()
    ld.connectAnon()
    for i in range(settings.MIN_COMPUTER_ID, settings.MAX_COMPUTER_ID + 1):
        res = ld.l.search_s(settings.LDAP_COMPUTERDN, ldap.SCOPE_SUBTREE, "uidNumber=" + str(i))
        if len(res) == 0:
            return i

    raise Exception("No more free user IDs")


def Add(computer_name):
    ld = LDAPConn()
    ld.connectRoot()

    dn = "uid=" + computer_name + "," + settings.LDAP_COMPUTERDN
    entry = {
        "uid": computer_name,
        "objectClass": ["account", "chbakAccount"],
        "uidNumber": str(GetFreeUIDNumber()),
        "cn": "Machine Account " + computer_name,
        "gidNumber": str(settings.MACHINE_GIDNUMBER),
        "homeDirectory": "/dev/null",
        "authorizedService": "samba@ank",
    }
    ld.addObject(dn, entry)

    execute_script("sudo /usr/local/userman/scripts/createsambamachine %s" % re.escape(computer_name))


def Exists(uid):
    ld = LDAPConn()
    ld.connectAnon()
    res = ld.l.search_s(settings.LDAP_COMPUTERDN, ldap.SCOPE_SUBTREE, "uid=" + uid)
    return len(res) != 0
