import ldap
from ldapconn import LDAPConn
from ldap.cidict import cidict
from django.conf import settings

def getCnForUid(uid):
    ld = LDAPConn()
    ld.connectAnon()
    res = ld.l.search_s(settings.LDAP_ALIASDN, ldap.SCOPE_SUBTREE, 'rfc822MailMember=' + uid)
    return [ attribs["cn"][0] for dn, attribs in res ]

def getIndirectCnForUid(uid, recurse=False):
    aliases = getCnForUid(uid)
    retval = []
    if recurse:
        retval += aliases
    for alias in aliases:
	retval += getIndirectCnForUid(alias, True)
    return retval
