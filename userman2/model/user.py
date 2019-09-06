#!/usr/bin/env python3
from userman2.scripts import execute_script
from userman2.model import group
from userman2.model import alias
from userman2.model import action
import datetime
import logging
import time
import secrets
import string
from io import StringIO

import ldap
from django.conf import settings
from ldap.cidict import cidict

from cron.mail import mailAdmin
from .ldapconn import LDAPConn

auditlog = logging.getLogger("userman2.audit")
logger = logging.getLogger(__name__)


class User(LDAPConn):
    """Represents a user in the ldap tree."""

    def __init__(self, dn, attrs=False):
        LDAPConn.__init__(self)
        self.dn = dn

        if attrs:
            self.__attrs = cidict(attrs)
            return

        self.connectAnon()
        res = self.l.search_s(self.dn, ldap.SCOPE_BASE)
        (_, attrs) = res[0]
        self.__attrs = cidict(attrs)

    def _get_uid(self):
        return self.__attrs["uid"][0].decode()

    uid = property(_get_uid)

    def _get_uidNumber(self):
        return int(self.__attrs["uidNumber"][0])

    uidNumber = property(_get_uidNumber)

    # gecos, cn, displayName attributes
    def _get_gecos(self):
        """Returns a dictionary describing the gecos attribute, consisting of full_name, room_number, work_phone, and home_phone"""
        if not "gecos" in self.__attrs:
            gecos = self.__attrs["cn"][0].decode()
        else:
            gecos = self.__attrs["gecos"][0].decode().split(",")

        if len(gecos) == 4:
            return {"full_name": gecos[0], "room_number": gecos[1], "work_phone": gecos[2], "home_phone": gecos[3]}
        return {"full_name": gecos[0], "room_number": "", "work_phone": "", "home_phone": ""}

    def _set_gecos(self, gecos):
        """Sets the gecos, displayName, and cn attributes according to the values specified in the dictionary"""
        newgecos = ",".join((gecos["full_name"], gecos["room_number"], gecos["work_phone"], gecos["home_phone"]))
        self.modifyEntries(
            {"cn": str(gecos["full_name"]), "displayName": str(gecos["full_name"]), "gecos": str(newgecos)}
        )

    gecos = property(_get_gecos, _set_gecos, None, "Dictionary containing the user gecos information")

    # description attribute
    def _get_description(self):
        """Returns the user description"""
        if not "description" in self.__attrs:
            return ""
        return self.__attrs["description"][0]

    def _set_description(self, description):
        """Sets the user description, or removes it for an empty string"""
        if description == "":
            description = None
        self.modifyEntries({"description": description})

    description = property(_get_description, _set_description, None, "The user's description")

    # loginShell attribute
    def _get_loginShell(self):
        """Returns the user's shell"""
        return self.__attrs["loginShell"][0]

    def _set_loginShell(self, loginShell):
        """Sets the user's shell"""
        self.modifyEntries({"loginShell": loginShell})

    loginShell = property(_get_loginShell, _set_loginShell, None, "The user's login shell")

    # gidNumber attribute
    def _get_gidNumber(self):
        """Returns the user's primary group ID number"""
        return int(self.__attrs["gidNumber"][0])

    def _set_gidNumber(self, gidNumber):
        """Sets the user's primary group ID number"""
        self.modifyEntries({"gidNumber": gidNumber})

    gidNumber = property(_get_gidNumber, _set_gidNumber, None, "The user's primary group ID number")

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
        if "authorizedservice" in self.__attrs:
            return list(map(lambda b: b.decode(), self.__attrs["authorizedService"]))
        return []

    authorizedServices = property(_get_authorizedServices)

    def addAuthorizedService(self, service):
        self.addEntries({"authorizedService": service})

    def removeAuthorizedService(self, service):
        self.removeEntries({"authorizedService": service})

    def _get_homeDirCH(self):
        return self.__attrs["homeDirectoryCH"][0]

    def _set_homeDirCH(self, newHomeDir):
        newAction = action.Add(
            "moveHomeDir",
            "ch.chnet",
            self.dn,
            "Move ch home directory from " + self.homeDirectoryCH + " to " + newHomeDir + " for user " + self.uid,
        )
        newAction.arguments = self.homeDirectoryCH
        self.modifyEntries({"homeDirectoryCH": newHomeDir})
        newAction.locked = False

    homeDirectoryCH = property(_get_homeDirCH, _set_homeDirCH)

    def _get_homeDir(self):
        return self.__attrs["homeDirectory"][0]

    def _set_homeDir(self, newHomeDir):
        newAction = action.Add(
            "moveHomeDir",
            "ank.chnet",
            self.dn,
            "Move ank home directory from " + self.homeDirectoryAnk + " to " + newHomeDir + " for user " + self.uid,
        )
        newAction.arguments = self.homeDirectoryAnk
        self.modifyEntries({"homeDirectory": newHomeDir})
        newAction.locked = False

    homeDirectoryAnk = property(_get_homeDir, _set_homeDir)

    def _get_toBeDeleted(self):
        actions = action.GetAllActions({"actionName": "warnRemove", "affectedDN": self.dn}, self)
        if actions:
            newdate = datetime.datetime(*(time.strptime(actions[0].arguments, "%Y-%m-%d %H:%M:%S")[0:6]))
            return newdate
        return False

    def _set_toBeDeleted(self, newdate):
        actions = action.GetAllActions({"actionName": "warnRemove", "affectedDN": self.dn})
        if actions:
            if newdate:
                actions[0].arguments = newdate.strftime("%Y-%m-%d %H:%M:%S")
                actions[0].locked = False
            else:
                actions[0].remove()
        else:
            newaction = action.Add("warnRemove", "ch.chnet", self.dn, "Send removal warning")
            newaction.arguments = newdate.strftime("%Y-%m-%d %H:%M:%S")
            newaction.locked = False

    toBeDeleted = property(_get_toBeDeleted, _set_toBeDeleted)

    def createHomeDir(self, host):
        return action.Add("createHomeDir", host, self.dn, "Create home directory on " + host + " for " + self.uid)

    def removeMailbox(self, host, parent):
        return action.Add("removeMailbox", host, self.dn, "Remove mailbox on " + host + " for " + self.uid, parent)

    def removeHomedir(self, host, parent):
        return action.Add(
            "removeHomeDir", host, self.dn, "Remove home directory on " + host + " for " + self.uid, parent
        )

    def removeProfile(self, host, parent=False):
        return action.Add("removeProfile", host, self.dn, "Remove profile on " + host + " for " + self.uid, parent)

    def remove(self):
        # Remove self from aliases/groups
        for secGroupCN in self.getSecondaryGroups():
            curGroup = group.FromCN(secGroupCN)
            curGroup.removeMember(self.uid)
        for aliasCN in self.getDirectAliases():
            curAlias = alias.fromCN(aliasCN, ld=self)
            curAlias.removeMember(self.uid)

        # Create removal tree
        removeAction = action.Add("removeUser", "ank.chnet", self.dn, "Remove user " + self.uid)
        removeHomedirAnk = self.removeHomedir("ank.chnet", removeAction)
        removeProfileAnk = self.removeProfile("ank.chnet", removeHomedirAnk)
        removeHomedirRob = self.removeHomedir("rob.chnet", removeAction)
        removeMailboxCh = self.removeMailbox("ch.chnet", removeAction)

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
        auditlog.info("Reset password for dn '%s'", self.dn)
        alphabet = string.ascii_letters + string.digits
        password = "".join(secrets.choice(alphabet) for i in range(20))
        res = self.l.passwd_s(self.dn, None, password)
        if res != (None, None):
            msg = "Unexpected response from modify password request"
            logger.error(msg, res)
            raise Exception(msg)
        return password

    def __str__(self):
        return "User: [ dn:'" + self.dn + ", uid:'" + self.uid + "', cn:'" + self.cn + "' ]"


def FromUID(uid):
    try:
        return User("uid=" + uid + "," + settings.LDAP_USERDN)
    except ldap.LDAPError as e:
        raise Exception("Error finding user " + uid)


def GetAllUserNames():
    ld = LDAPConn()
    ld.connectAnon()
    res = ld.l.search_s(settings.LDAP_USERDN, ldap.SCOPE_ONELEVEL)
    res.sort()
    return [attrs["uid"][0].decode() for (dn, attrs) in res]


def GetAllUsers(filter_data=False):
    ld = LDAPConn()
    ld.connectAnon()
    if filter_data:
        filter_string = "(&"
        if filter_data["uid"]:
            filter_string += "(uid=*" + filter_data["uid"] + "*)"
        if filter_data["cn"]:
            filter_string += "(cn=*" + filter_data["cn"] + "*)"
        if filter_data["uidnumber"]:
            filter_string += "(uidNumber=" + str(filter_data["uidnumber"]) + ")"
        if filter_data["chlocal"]:
            filter_string += "(authorizedService=sshd@ch)"
        if filter_data["nochlocal"]:
            filter_string += "(!(authorizedService=sshd@ch))"
        if filter_data["anklocal"]:
            filter_string += "(authorizedService=sshd@ank)"
        if filter_data["noanklocal"]:
            filter_string += "(!(authorizedService=sshd@ank))"
        if filter_data["anksamba"]:
            filter_string += "(authorizedService=samba@ank)"
        if filter_data["noanksamba"]:
            filter_string += "(!(authorizedService=samba@ank))"
        filter_string += ")"
        res = ld.l.search_s(settings.LDAP_USERDN, ldap.SCOPE_ONELEVEL, filter_string)
    else:
        res = ld.l.search_s(settings.LDAP_USERDN, ldap.SCOPE_ONELEVEL)
    res.sort()
    ret = [User(dn, attrs) for (dn, attrs) in res]
    return ret


def GetPrimaryMembersForGid(gid):
    ld = LDAPConn()
    ld.connectAnon()
    res = ld.l.search_s(settings.LDAP_USERDN, ldap.SCOPE_ONELEVEL, "gidNumber=" + str(gid))
    return [attribs["uid"][0] for dn, attribs in res]


def Exists(uid):
    ld = LDAPConn()
    ld.connectAnon()
    res = ld.l.search_s(settings.LDAP_USERDN, ldap.SCOPE_SUBTREE, "uid=" + uid)
    return len(res) != 0


def GetFreeUIDNumber():
    ld = LDAPConn()
    ld.connectAnon()
    for i in reversed(range(settings.MIN_USER_ID, settings.MAX_USER_ID + 1)):
        res = ld.l.search_s(settings.LDAP_USERDN, ldap.SCOPE_SUBTREE, "uidNumber=" + str(i))
        if len(res) > 0:
            if i == settings.MAX_USER_ID:
                raise Exception("No more free user IDs")
            else:
                return i + 1

    # This should never happen: if MAX_USER_ID is not taken we should have a free UID
    raise AssertionError("Failure in finding free user ID")


def Add(uid, fullname):
    ld = LDAPConn()
    ld.connectRoot()

    dn = "uid=" + uid + "," + settings.LDAP_USERDN
    entry = {
        "uid": uid,
        "objectClass": ["account", "chbakAccount"],
        "uidNumber": str(GetFreeUIDNumber()),
        "userPassword": "!disabled",
        "cn": fullname,
        "displayName": fullname,
        "gecos": fullname + ",,,",
        "gidNumber": str(settings.USER_GIDNUMBER),
        "homeDirectory": settings.ANK_HOME_BASE + uid,
        "homeDirectoryCH": settings.CH_HOME_BASE + uid,
        "loginShell": settings.DEFAULT_SHELL,
        "shadowLastChange": str(int(time.time() / 86400)),
        "shadowMax": str(99999),
        "shadowWarning": str(7),
    }
    ld.addObject(dn, entry)

    execute_script("sudo /usr/local/userman/scripts/createsambauser %s" % uid)

    mailAdmin("Account created: %s" % uid, "A new account was created for %s (%s)" % (uid, fullname))

    return FromUID(uid)
