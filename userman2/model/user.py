#!/usr/bin/env python
import ldap
import ldif
from StringIO import StringIO
from ldapconn import LDAPConn
from ldap.cidict import cidict
from django.conf import settings
from userman2.model import group
from userman2.model import alias
from userman2.model import action
from cron.mail import mailAdmin
import random
import string
import os
import time
import re
import subprocess
import datetime


class User (LDAPConn):

    """Represents a user in the ldap tree."""

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
        newgecos = ",".join(
            (gecos['full_name'], gecos['room_number'], gecos['work_phone'], gecos['home_phone']))
        self.modifyEntries(
            {'cn': str(gecos['full_name']), 'displayName': str(gecos['full_name']), 'gecos': str(newgecos)})

    gecos = property(_get_gecos, _set_gecos, None,
                     "Dictionary containing the user gecos information")

    # description attribute
    def _get_description(self):
        """Returns the user description"""
        if not 'description' in self.__attrs:
            return ""
        return self.__attrs["description"][0]

    def _set_description(self, description):
        """Sets the user description, or removes it for an empty string"""
        if description == "":
            description = None
        self.modifyEntries({'description': description})

    description = property(
        _get_description, _set_description, None, "The user's description")

    # loginShell attribute
    def _get_loginShell(self):
        """Returns the user's shell"""
        return self.__attrs["loginShell"][0]

    def _set_loginShell(self, loginShell):
        """Sets the user's shell"""
        self.modifyEntries({'loginShell': loginShell})

    loginShell = property(
        _get_loginShell, _set_loginShell, None, "The user's login shell")

    # gidNumber attribute
    def _get_gidNumber(self):
        """Returns the user's primary group ID number"""
        return int(self.__attrs["gidNumber"][0])

    def _set_gidNumber(self, gidNumber):
        """Sets the user's primary group ID number"""
        self.modifyEntries({'gidNumber': gidNumber})

    gidNumber = property(
        _get_gidNumber, _set_gidNumber, None, "The user's primary group ID number")

    # login permissions
    def get_chLocal(self):
        return "sshd@ch" in self.authorizedServices
    chLocal = property(get_chLocal)

    def get_ankLocal(self):
        return "sshd@ank" in self.authorizedServices
    ankLocal = property(get_ankLocal)

    def get_ankSamba(self):
        return "samba@ank" in self.authorizedServices
    ankSamba = property(get_ankSamba)

    def _get_authorizedServices(self):
        if 'authorizedservice' in self.__attrs:
            return self.__attrs["authorizedService"]
        return []
    authorizedServices = property(_get_authorizedServices)

    def addAuthorizedService(self, service):
        self.addEntries({'authorizedService': service})

    def removeAuthorizedService(self, service):
        self.removeEntries({'authorizedService': service})

    def _get_homeDirCH(self):
        return self.__attrs["homeDirectoryCH"][0]

    def _set_homeDirCH(self, newHomeDir):
        newAction = action.Add('moveHomeDir', 'ch.chnet', self.dn,
                               'Move ch home directory from ' + self.homeDirectoryCH + ' to ' + newHomeDir + ' for user ' + self.uid)
        newAction.arguments = self.homeDirectoryCH
        self.modifyEntries({'homeDirectoryCH': newHomeDir})
        newAction.locked = False
    homeDirectoryCH = property(_get_homeDirCH, _set_homeDirCH)

    def _get_homeDir(self):
        return self.__attrs["homeDirectory"][0]

    def _set_homeDir(self, newHomeDir):
        newAction = action.Add('moveHomeDir', 'ank.chnet', self.dn,
                               'Move ank home directory from ' + self.homeDirectoryAnk + ' to ' + newHomeDir + ' for user ' + self.uid)
        newAction.arguments = self.homeDirectoryAnk
        self.modifyEntries({'homeDirectory': newHomeDir})
        newAction.locked = False

    homeDirectoryAnk = property(_get_homeDir, _set_homeDir)

    def _get_toBeDeleted(self):
        actions = action.GetAllActions(
            {'actionName': 'warnRemove', 'affectedDN': self.dn}, self)
        if actions:
            newdate = datetime.datetime(
                *(time.strptime(actions[0].arguments,  "%Y-%m-%d %H:%M:%S")[0:6]))
            return newdate
        return False

    def _set_toBeDeleted(self, newdate):
        actions = action.GetAllActions(
            {'actionName': 'warnRemove', 'affectedDN': self.dn})
        if actions:
            if newdate:
                actions[0].arguments = newdate.strftime("%Y-%m-%d %H:%M:%S")
                actions[0].locked = False
            else:
                actions[0].remove()
        else:
            newaction = action.Add(
                'warnRemove', 'ch.chnet', self.dn, "Send removal warning")
            newaction.arguments = newdate.strftime("%Y-%m-%d %H:%M:%S")
            newaction.locked = False

    toBeDeleted = property(_get_toBeDeleted, _set_toBeDeleted)

    def createHomeDir(self, host):
        return action.Add('createHomeDir', host, self.dn, 'Create home directory on ' + host + ' for ' + self.uid)

    def removeMailbox(self, host, parent):
        return action.Add('removeMailbox', host, self.dn, 'Remove mailbox on ' + host + ' for ' + self.uid, parent)

    def removeHomedir(self, host, parent):
        return action.Add('removeHomeDir', host, self.dn, 'Remove home directory on ' + host + ' for ' + self.uid, parent)

    def removeProfile(self, host, parent=False):
        return action.Add('removeProfile', host, self.dn, 'Remove profile on ' + host + ' for ' + self.uid, parent)

    # def generateLogonScript(self, host):
        # return action.Add('generateLogonScript', host, self.dn, 'Generate
        # logonscript on ' + host + ' for ' + self.uid)

    def get_ldif(self):
        out = StringIO()
        ldif_out = ldif.LDIFWriter(out)
        ldif_out.unparse(self.dn, dict(self.__attrs))
        return out.getvalue()
    ldif = property(get_ldif)

    def remove(self):
        file = open(settings.GRAVEYARD_DIR + '/' +
                    self.uid + '_' + str(time.time()) + '.ldif', 'w')
        file.write(self.ldif)

        # Remove self from aliases/groups
        for secGroupCN in self.getSecondaryGroups():
            curGroup = group.FromCN(secGroupCN)
            curGroup.removeMember(self.uid)
        for aliasCN in self.getDirectAliases():
            curAlias = alias.fromCN(aliasCN, ld=self)
            curAlias.removeMember(self.uid)

        # Create removal tree
        removeAction = action.Add(
            'removeUser', 'frans.chnet', self.dn, 'Remove user ' + self.uid)
        removeHomedirAnk = self.removeHomedir('ank.chnet', removeAction)
        removeProfileAnk = self.removeProfile('ank.chnet', removeHomedirAnk)
        removeHomedirRob = self.removeHomedir('rob.chnet', removeAction)
        removeMailboxCh = self.removeMailbox('ch.chnet', removeAction)

        # Unlock removal tree
        removeProfileAnk.locked = False
        removeHomedirAnk.locked = False
        removeMailboxCh.locked = False
        removeHomedirRob.locked = False
        removeAction.locked = False

    def getSecondaryGroups(self):
        return group.GetCnForUid(self.uid)

    def getDirectAliases(self):
        return alias.getCnForUid(self.uid, ld=self)

    def getIndirectAliases(self):
        return alias.getIndirectCnForUid(self.uid, ld=self)

    def resetPassword(self):
        password = GeneratePassword()
        retcode = subprocess.call('sudo ' + os.path.join(settings.ROOT_PATH, 'scripts/changesambapasswd')
                                  + ' ' + re.escape(self.uid) + ' ' + re.escape(password), shell=True)
        if retcode != 0:
            raise Exception, "Child failed"
        mailAdmin('Password reset: ' + self.uid,
                  'A new password was created for ' + self.uid + ' with password ' + password)

    def changePassword(self, password):
        retcode = subprocess.call('sudo ' + os.path.join(settings.ROOT_PATH, 'scripts/changesambapasswd')
                                  + ' ' + re.escape(self.uid) + ' ' + re.escape(password), shell=True)
        if retcode != 0:
            raise Exception, "Child failed"

    def __str__(self):
        return "User: [ dn:'" + self.dn + ", uid:'" + self.uid + "', cn:'" + self.cn + "' ]"


def FromUID(uid):
    try:
        return User("uid=" + uid + "," + settings.LDAP_USERDN)
    except ldap.LDAPError, e:
        raise Exception, "Error finding user " + uid


def GetAllUserNames():
    ld = LDAPConn()
    ld.connectAnon()
    res = ld.l.search_s(settings.LDAP_USERDN, ldap.SCOPE_ONELEVEL)
    res.sort()
    return [attrs['uid'][0] for (dn, attrs) in res]


def GetAllUsers(filter_data=False):
    ld = LDAPConn()
    ld.connectRoot()
    if filter_data:
        filter_string = "(&"
        if filter_data['uid']:
            filter_string += "(uid=*" + filter_data['uid'] + "*)"
        if filter_data['cn']:
            filter_string += "(cn=*" + filter_data['cn'] + "*)"
        if filter_data['uidnumber']:
            filter_string += "(uidNumber=" + str(
                filter_data['uidnumber']) + ")"
        if filter_data['chlocal']:
            filter_string += "(authorizedService=sshd@ch)"
        if filter_data['nochlocal']:
            filter_string += "(!(authorizedService=sshd@ch))"
        if filter_data['anklocal']:
            filter_string += "(authorizedService=sshd@ank)"
        if filter_data['noanklocal']:
            filter_string += "(!(authorizedService=sshd@ank))"
        if filter_data['anksamba']:
            filter_string += "(authorizedService=samba@ank)"
        if filter_data['noanksamba']:
            filter_string += "(!(authorizedService=samba@ank))"
        filter_string += ")"
        res = ld.l.search_s(
            settings.LDAP_USERDN, ldap.SCOPE_ONELEVEL, filter_string)
    else:
        res = ld.l.search_s(settings.LDAP_USERDN, ldap.SCOPE_ONELEVEL)
    res.sort()
    ret = [User(dn, attrs) for (dn, attrs) in res]
    return ret


def GetPrimaryMembersForGid(gid):
    ld = LDAPConn()
    ld.connectRoot()
    res = ld.l.search_s(
        settings.LDAP_USERDN, ldap.SCOPE_ONELEVEL, 'gidNumber=' + str(gid))
    return [attribs["uid"][0] for dn, attribs in res]


def Exists(uid):
    ld = LDAPConn()
    ld.connectAnon()
    res = ld.l.search_s(settings.LDAP_USERDN, ldap.SCOPE_SUBTREE, "uid=" + uid)
    return len(res) != 0


def GetFreeUIDNumber():
    ld = LDAPConn()
    ld.connectAnon()
    for i in range(settings.MIN_USER_ID, settings.MAX_USER_ID):
        res = ld.l.search_s(
            settings.LDAP_USERDN, ldap.SCOPE_SUBTREE, "uidNumber=" + str(i))
        if len(res) == 0:
            return i

    raise Exception, "No more free user IDs"


def GeneratePassword(length=10):
    chars = string.letters + string.letters + string.digits
    return ''.join([random.choice(chars) for i in range(length)])


def Add(uid, fullname):
    ld = LDAPConn()
    ld.connectRoot()

    password = GeneratePassword()

    dn = 'uid=' + uid + ',' + settings.LDAP_USERDN
    entry = {'uid': uid}
    entry['objectClass'] = ['account', 'chbakAccount']
    entry['uidNumber'] = str(GetFreeUIDNumber())
    entry['userPassword'] = '!disabled'
    entry['cn'] = fullname
    entry['displayName'] = fullname
    entry['gecos'] = fullname + ",,,"
    entry['gidNumber'] = str(settings.USER_GIDNUMBER)
    entry['homeDirectory'] = settings.ANK_HOME_BASE + entry['uid']
    entry['homeDirectoryCH'] = settings.CH_HOME_BASE + entry['uid']
    entry['loginShell'] = settings.DEFAULT_SHELL
    entry['shadowLastChange'] = str(int(time.time() / 86400))
    entry['shadowMax'] = str(99999)
    entry['shadowWarning'] = str(7)

    ld.addObject(dn, entry)

    retcode = subprocess.call('sudo ' + os.path.join(settings.ROOT_PATH, 'scripts/createsambauser')
                              + ' ' + re.escape(uid) + ' ' + re.escape(password), shell=True)
    if retcode != 0:
        raise Exception, "Child failed"

    mailAdmin('Account created: ' + uid, 'A new account was created for ' +
              uid + ' (' + entry['displayName'] + ') with password ' + password)

    return FromUID(entry['uid'])

# def GenerateAllLogonscripts(host):
    # return action.Add('generateAllLogonScripts', host, '', 'Regenerate all
    # logon scripts')
