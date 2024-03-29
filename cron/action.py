#!/usr/bin/env python3

import os
import tarfile
from os.path import abspath, exists
from shutil import copy2, rmtree
from time import time

import config
import ldap

from user import User


class Action:
    def __init__(self, l, dn):
        self.l = l
        self.dn = dn

    def getChildren(self):
        # Process Sub-actions
        res = self.l.search_s(self.dn, ldap.SCOPE_ONELEVEL)
        ret = [Action(self.l, dn) for (dn, attrs) in res]
        return ret

    def getDescription(self):
        res = self.l.search_s(self.dn, ldap.SCOPE_BASE)
        (_, attrs) = res[0]
        return attrs["description"][0].decode()

    def getArguments(self):
        res = self.l.search_s(self.dn, ldap.SCOPE_BASE)
        (_, attrs) = res[0]
        return attrs["arguments"][0].decode()

    def getHost(self):
        res = self.l.search_s(self.dn, ldap.SCOPE_BASE)
        (_, attrs) = res[0]
        return attrs["host"][0].decode()

    def getAffectedDN(self):
        res = self.l.search_s(self.dn, ldap.SCOPE_BASE)
        (_, attrs) = res[0]
        return attrs["affectedDN"][0].decode()

    def getActionName(self):
        res = self.l.search_s(self.dn, ldap.SCOPE_BASE)
        (_, attrs) = res[0]
        return attrs["actionName"][0].decode()

    def isLocked(self):
        res = self.l.search_s(self.dn, ldap.SCOPE_BASE)
        (_, attrs) = res[0]
        return attrs["actionLocked"][0].decode() != "FALSE"

    def lock(self):
        self.l.modify_s(self.dn, [(ldap.MOD_REPLACE, "actionLocked", "TRUE".encode())])

    def unlock(self):
        self.l.modify_s(self.dn, [(ldap.MOD_REPLACE, "actionLocked", "FALSE".encode())])

    def delete(self):
        self.l.delete_s(self.dn)

    def __str__(self):
        return "Action: " + self.dn + ", " + self.getDescription()

    def execute(self):
        actionName = self.getActionName()
        if actionName == "removeMailbox":
            return self.removeMailbox()
        elif actionName == "removeHomeDir":
            return self.removeHomeDir()
        elif actionName == "removeUser":
            return self.removeUser()
        else:
            raise Exception("unknown actionName: " + actionName)

    def removeMailbox(self):
        if not config.enableMailboxRemoval:
            raise Exception("Mailbox removal not enabled on host " + self.getHost())

        user = User(self.l, self.getAffectedDN())
        mailbox = os.path.join(config.mailDir, user.getUID())

        if exists(mailbox):
            tar = tarfile.open(
                os.path.join(config.graveyardDir, "MAILBOX_" + user.getUID() + "-" + str(int(time())) + ".tar.gz"),
                "w:gz",
            )
            tar.add(mailbox)
            tar.close()
            rmtree(mailbox)

        return True

    def removeHomeDir(self):
        if not config.enableHomeDirRemoval:
            raise Exception("Home directory removal not enabled on host " + self.getHost())

        user = User(self.l, self.getAffectedDN())
        homedir = abspath(user.getHomeDirectory())

        if not homedir.startswith(config.homeDirBase):
            raise Exception("Home directories must be created in " + config.homeDirBase)

        if exists(homedir):
            tar = tarfile.open(
                os.path.join(config.graveyardDir, "HOMEDIR_" + user.getUID() + "-" + str(int(time())) + ".tar.gz"),
                "w:gz",
            )
            tar.add(homedir)
            tar.close()
            rmtree(homedir)

        return True

    def removeUser(self):
        if not config.enableUserRemoval:
            raise Exception("User removal not enabled on host " + self.getHost())

        self.l.delete_s(self.getAffectedDN())
        return True

    def chmodTree(self, dest, mode, dirmode):
        os.chmod(dest, dirmode)
        for root, dirs, files in os.walk(dest):
            for name in files:
                os.chmod(os.path.join(root, name), mode)
            for name in dirs:
                os.chmod(os.path.join(root, name), dirmode)

    def chownTree(self, dest, uidNumber, gidNumber):
        os.chown(dest, uidNumber, gidNumber)
        for root, dirs, files in os.walk(dest):
            for name in files:
                os.chown(os.path.join(root, name), uidNumber, gidNumber)
            for name in dirs:
                os.chown(os.path.join(root, name), uidNumber, gidNumber)

    def copyTree(self, src, dest):
        for root, dirs, files in os.walk(src):
            for name in files:
                destname = os.path.join(dest + "/" + root[len(src) :], name)
                srcname = os.path.join(root, name)
                copy2(srcname, destname)
            for name in dirs:
                destname = os.path.join(dest + "/" + root[len(src) :], name)
                os.mkdir(destname)
