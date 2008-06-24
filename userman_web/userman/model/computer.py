import ldap
from ldapconn import LDAPConn
from ldap.cidict import cidict
from django.conf import settings
import re
import subprocess

class Computer (LDAPConn):
    def __init__ (self, dn, attrs = False):
        LDAPConn.__init__(self)
        self.dn = dn

        if attrs:
            self.__attrs = cidict(attrs)
            return

        self.connectRoot()

        res = self.l.search_s(self.dn, ldap.SCOPE_BASE)
        (_, attrs) = res[0]
        self.__attrs = cidict(attrs)

def FromUID(uid):
    try:
        return Computer("uid=" + uid + "," + settings.LDAP_COMPUTERDN)
    except ldap.LDAPError, e:
        raise Exception, "Error finding computer " + uid

def GetFreeUIDNumber():
    ld = LDAPConn()
    ld.connectAnon()
    for i in range(settings.MIN_COMPUTER_ID, settings.MAX_COMPUTER_ID+1):
        res = ld.l.search_s(settings.LDAP_COMPUTERDN, ldap.SCOPE_SUBTREE, "uidNumber=" + str(i))
        if len(res) == 0:
            return i
    
    raise Exception, "No more free user IDs"

def Add(uid):
    ld = LDAPConn()
    ld.connectRoot()

    dn = 'uid=' + uid + ',' + settings.LDAP_COMPUTERDN
    entry = {'uid': uid}
    entry['objectClass'] = ['posixAccount']
    entry['uidNumber'] = str(GetFreeUIDNumber())
    entry['cn'] = "Machine Account "+uid
    entry['gidNumber'] = str(settings.MACHINE_GIDNUMBER)
    entry['homeDirectory'] = "/dev/null"

    ld.addObject(dn, entry)
    retcode = subprocess.call('sudo ' + '/var/www_python/userman/scripts/createsambamachine ' + re.escape(uid)), shell=True)
    if retcode != 0:
        raise Exception, "Child failed"