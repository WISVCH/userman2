import ldap
from ldapconn import LDAPConn
from ldap.cidict import cidict
from django.conf import settings

def getCnForUid(uid, ld=None):
    if not ld:
        ld = LDAPConn()
        ld.connectAnon()
    res = ld.l.search_s(settings.LDAP_ALIASDN, ldap.SCOPE_SUBTREE, 'rfc822MailMember=' + uid)
    return [ attribs["cn"][0] for dn, attribs in res ]

def getIndirectCnForUid(uid, recurse=False, ld=None):
    if not ld:
        ld = LDAPConn()
        ld.connectAnon()
    aliases = getCnForUid(uid, ld)
    retval = []
    if recurse:
        retval += aliases
    for alias in aliases:
	retval += getIndirectCnForUid(alias, True, ld)
    return retval
