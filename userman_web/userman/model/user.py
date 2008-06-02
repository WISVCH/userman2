#!/usr/bin/env python
import ldap, ldif
from StringIO import StringIO
from ldapconn import LDAPConn
from ldap.cidict import cidict
from django.conf import settings
from userman.model import group
from userman.model import alias

class User (LDAPConn):
    """Represents a user in the ldap tree."""
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

    def _get_uid(self):
        return self.__attrs["uid"][0]
    uid = property (_get_uid)


    def _get_uidNumber(self):
        return int(self.__attrs["uidNumber"][0])
    uidNumber = property (_get_uidNumber)

    # gecos, cn, displayName attributes
    def _get_gecos(self):
        """Returns a dictionary describing the gecos attribute, consisting of full_name, room_number, work_phone, and home_phone"""
        if not 'gecos' in self.__attrs:
            gecos = self.__atrs['cn'][0]
        else:
            gecos = self.__attrs["gecos"][0].split(',')

        if len(gecos) == 4:
            return {'full_name': gecos[0], 'room_number': gecos[1], 'work_phone': gecos[2], 'home_phone': gecos[3]} 
        return {'full_name': gecos[0], 'room_number': '', 'work_phone': '', 'home_phone': ''} 

    def _set_gecos(self, gecos):
        """Sets the gecos, displayName, and cn attributes according to the values specified in the dictionary"""
        newgecos = ",".join((gecos['full_name'], gecos['room_number'], gecos['work_phone'], gecos['home_phone']))
        self.modifyEntries({'cn': str(gecos['full_name']), 'displayName': str(gecos['full_name']), 'gecos': str(newgecos) })

    gecos = property (_get_gecos, _set_gecos, None, "Dictionary containing the user gecos information")

    # description attribute
    def _get_description(self):
        """Returns the user description"""
        if not 'description' in self.__attrs:
            return ""
        return self.__attrs["description"][0]

    def _set_description(self, description):
        """Sets the user description, or removes it for an empty string"""
        if description == "": description = None
        self.modifyEntries({'description': description})

    description = property (_get_description, _set_description, None, "The user's description")

    # loginShell attribute
    def _get_loginShell(self):
        """Returns the user's shell"""
        return self.__attrs["loginShell"][0]

    def _set_loginShell(self, loginShell):
        """Sets the user's shell"""
        self.modifyEntries({'loginShell': loginShell})

    loginShell = property (_get_loginShell, _set_loginShell, None, "The user's login shell")

    # gidNumber attribute
    def _get_gidNumber(self):
        """Returns the user's primary group ID number"""
        return int(self.__attrs["gidNumber"][0])
	
    def _set_gidNumber(self, gidNumber):
        """Sets the user's primary group ID number"""
        self.modifyEntries({'gidNumber': gidNumber})

    gidNumber = property (_get_gidNumber, _set_gidNumber, None, "The user's primary group ID number")

    # login permissions
    def get_chLocal(self):
        return "ssh@ch" in self.authorizedServices
    chLocal = property (get_chLocal)

    def get_ankLocal(self):
        return "ssh@ank" in self.authorizedServices
    ankLocal = property (get_ankLocal)

    def get_ankSamba(self):
        return "samba@ank" in self.authorizedServices
    ankSamba = property (get_ankSamba)

    def get_chSamba(self):
#        assert False, self.authorizedServices
        return "samba@ch" in self.authorizedServices
    chSamba = property (get_chSamba)

    def _get_authorizedServices(self):
        if 'authorizedservice' in self.__attrs:
            return self.__attrs["authorizedService"]
        return []
    authorizedServices = property (_get_authorizedServices)

    def addAuthorizedService(self, service):
        self.addEntries({'authorizedService': service})

    def removeAuthorizedService(self, service):
        self.removeEntries({'authorizedService': service})
        
    def get_homeDirCH(self):
        return self.__attrs["homeDirectoryCH"][0]
    homeDirectoryCH = property(get_homeDirCH)

    def get_homeDir(self):
        return self.__attrs["homeDirectory"][0]
    homeDirectoryAnk = property(get_homeDir)

    def get_ldif(self):
        out = StringIO()
        ldif_out = ldif.LDIFWriter(out)
        ldif_out.unparse(self.dn, dict(self.__attrs))
        return out.getvalue()
    ldif = property(get_ldif)

#    def getHomeDirectory(self, host):
#	if host == 'ch.chnet':
#	    return self.attrs["homeDirectoryCH"][0]
#	else:
#	    return self.attrs["homeDirectory"][0]
#
#    def _set_homeDirectory(self, host, homeDir):
#	if host == 'ch.chnet':
#	    self.l.modify_s (self.dn, [(ldap.MOD_REPLACE, 'homeDirectoryCH', homeDir)])	
#	    res = self.l.search_s(self.dn, ldap.SCOPE_BASE)
#	    (_, attrs) = res[0]
#	    self.attrs = cidict(attrs)
#	    return self.attrs["homeDirectoryCH"][0]
#	else:
#	    self.l.modify_s (self.dn, [(ldap.MOD_REPLACE, 'homeDirectory', homeDir)])	
#	    res = self.l.search_s(self.dn, ldap.SCOPE_BASE)
#	    (_, attrs) = res[0]
#	    self.attrs = cidict(attrs)
#	    return self.attrs["homeDirectory"][0]

#    def getPrimaryGroup (self):
#	res = self.l.search_s(config.ldapGroupOU, ldap.SCOPE_SUBTREE, 'gidNumber=' + self.attrs["gidNumber"][0])
#	if len (res) != 1:
#	    return "none"
#	(_, attrs) = res[0]
#	return attrs["cn"][0];
	
    def getSecondaryGroups(self):
        return group.getCnForUid(self.uid)

    def getDirectAliases(self):
        return alias.getCnForUid(self.uid, ld=self)

    def getIndirectAliases(self):
        return alias.getIndirectCnForUid(self.uid, ld=self)

#    def getGroups(self):
#	sec = self.getSecondaryGroups();
#	pri = self.getPrimaryGroup()
#	if pri in sec:
#	    return sec
#	else:
#	    return sec + [pri]

    def __str__(self):
	return "User: [ dn:'" + self.dn + ", uid:'" + self.uid + "', cn:'" +self.cn + "' ]"

def fromUID(uid):
    try:
        return User("uid=" + uid + "," + settings.LDAP_USERDN)
    except ldap.LDAPError, e:
        raise Exception, "Error finding user " + uid

def getAllUserNames():
    ld = LDAPConn()
    ld.connectAnon()
    res = ld.l.search_s(settings.LDAP_USERDN, ldap.SCOPE_ONELEVEL)
    res.sort()
    return [attrs['uid'][0] for (dn, attrs) in res]
    
    
def getAllUsers(filter_data=False):
    ld = LDAPConn()
    ld.connectRoot()
    if filter_data:
        filter_string = "(&"
        if filter_data['uid']: filter_string += "(uid=*" + filter_data['uid'] + "*)"
        if filter_data['cn']: filter_string += "(cn=*" + filter_data['cn'] + "*)"
        if filter_data['uidnumber']: filter_string += "(uidNumber=" + str(filter_data['uidnumber']) + ")"
        if filter_data['chlocal']: filter_string += "(allowLocalLogonCH=TRUE)"
        if filter_data['nochlocal']: filter_string += "(allowLocalLogonCH=FALSE)"
        if filter_data['chsamba']: filter_string += "(allowSambaLogonCH=TRUE)"
        if filter_data['nochsamba']: filter_string += "(allowSambaLogonCH=FALSE)"
        if filter_data['anklocal']: filter_string += "(allowLocalLogonAnk=TRUE)"
        if filter_data['noanklocal']: filter_string += "(allowLocalLogonAnk=FALSE)"
        if filter_data['anksamba']: filter_string += "(allowSambaLogonAnk=TRUE)"
        if filter_data['noanksamba']: filter_string += "(allowSambaLogonAnk=FALSE)"
        filter_string += ")"
        res = ld.l.search_s(settings.LDAP_USERDN, ldap.SCOPE_ONELEVEL, filter_string)
    else:
        res = ld.l.search_s(settings.LDAP_USERDN, ldap.SCOPE_ONELEVEL)
    res.sort()
    ret = [User(dn, attrs) for (dn, attrs) in res]
    return ret

def getPrimaryMembersForGid(gid):
    ld = LDAPConn()
    ld.connectRoot()
    res = ld.l.search_s(settings.LDAP_USERDN, ldap.SCOPE_ONELEVEL, 'gidNumber='+str(gid))
    return [ attribs["uid"][0] for dn, attribs in res ]

def Exists(uid):
    ld = LDAPConn()
    ld.connectAnon()
    res = ld.l.search_s(settings.LDAP_USERDN, ldap.SCOPE_SUBTREE, "uid="+uid)
    return len(res) != 0 
  