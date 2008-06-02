import ldap
from ldapconn import LDAPConn
from ldap.cidict import cidict
from django.conf import settings
class Alias (LDAPConn):
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

    def _get_cn(self):
        return self.__attrs["cn"][0]
    cn = property (_get_cn)

    def _get_parent(self):
        parent = self.dn.split(',')[1].split('=')[1]
        if parent == "Aliases":
            return "None"
        return parent
    parent = property (_get_parent)

    def _get_members(self):
        if 'rfc822mailmember' in self.__attrs:
            return self.__attrs['rfc822MailMember']
        return []
    members = property(_get_members)

    def removeMember(self, member):
        self.removeEntries({'rfc822MailMember': member})

    def addMember(self, member):
        self.addEntries({'rfc822MailMember': member})

    def remove(self):
        self.delObject()
        
    def __str__(self):
        return "Alias: [ dn:'" + self.dn + ", cn:'" + self.cn + "' ]"

def getCnForUid(uid, ld=None):
    if not ld:
        ld = LDAPConn()
        ld.connectAnon()
    res = ld.l.search_s(settings.LDAP_ALIASDN, ldap.SCOPE_SUBTREE, 'rfc822MailMember=' + uid)
    return [ attribs["cn"][0] for dn, attribs in res ]

def fromCN(cn, ld=None):
    if not ld:
        ld = LDAPConn()
        ld.connectAnon()
    res = ld.l.search_s(settings.LDAP_ALIASDN, ldap.SCOPE_SUBTREE, "cn="+cn)
    if not res:
        raise Exception, "Error finding alias " + cn

    (dn, attrs) = res[0]
    return Alias(dn, attrs)

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

def getAllAliasNames():
    ld = LDAPConn()
    ld.connectAnon()
    res = ld.l.search_s(settings.LDAP_ALIASDN, ldap.SCOPE_SUBTREE, "objectClass=nisMailAlias")
    res.sort()
    return [attrs['cn'][0] for (dn, attrs) in res]
    
def getAllAliases(filter_data=False):
    """Returns all aliases under LDAP_ALIASDN, in a dictionary sorted by their ou"""
    ld = LDAPConn()
    ld.connectAnon()

    if filter_data:
        filter_string = "(&"
        if filter_data['uid']: filter_string += "(rfc822MailMember=" + filter_data['uid'] + ")"
        if filter_data['cn']: filter_string += "(cn=*" + filter_data['cn'] + "*)"
        filter_string += "(objectClass=nisMailAlias))"
    else:
        filter_string = "(objectClass=nisMailAlias)"
    res = ld.l.search_s(settings.LDAP_ALIASDN, ldap.SCOPE_SUBTREE, filter_string)

    res.sort()
    ret = {}
    for dn, attrs in res:
        alias = Alias(dn, attrs)
        if not alias.parent in ret:
            ret[alias.parent] = []
        ret[alias.parent] += [alias]
        # Find indirect aliases
        if filter_data and filter_data['uid']:
            for iCN in getIndirectCnForUid(alias.cn, True, ld):
                iAlias = fromCN(iCN,ld)
                if not iAlias.parent in ret:
                    ret[iAlias.parent] = []
                ret[iAlias.parent] += [iAlias]

    return ret
def GetParents():
    """Returns the possible parents of an alias"""
    ld = LDAPConn()
    ld.connectAnon()

    filter_string = "(objectClass=organizationalUnit)"
    res = ld.l.search_s(settings.LDAP_ALIASDN, ldap.SCOPE_ONELEVEL, filter_string)
    res.sort()
    return [ attribs['ou'][0] for (_, attribs) in res]

def Exists(cn):
    ld = LDAPConn()
    ld.connectAnon()
    res = ld.l.search_s(settings.LDAP_ALIASDN, ldap.SCOPE_SUBTREE, "cn="+cn)
    return len(res) != 0 
    
def Add(parent, cn):
    dn = 'cn=' +cn +',ou=' + parent + ',' + settings.LDAP_ALIASDN
    ld = LDAPConn()
    ld.connectRoot()
    ld.addObject(dn, {'objectClass': 'nisMailAlias', 'cn': cn})
