#!/usr/bin/env python3

import os
import tarfile
from os import makedirs
from os.path import abspath, exists
from shutil import copy2, rmtree
from time import time

# local imports
import config
import ldap
from group import Group
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
        return attrs["description"][0]

    def getArguments(self):
        res = self.l.search_s(self.dn, ldap.SCOPE_BASE)
        (_, attrs) = res[0]
        return attrs["arguments"][0]

    def getHost(self):
        res = self.l.search_s(self.dn, ldap.SCOPE_BASE)
        (_, attrs) = res[0]
        return attrs["host"][0]

    def getAffectedDN(self):
        res = self.l.search_s(self.dn, ldap.SCOPE_BASE)
        (_, attrs) = res[0]
        return attrs["affectedDN"][0]

    def getActionName(self):
        res = self.l.search_s(self.dn, ldap.SCOPE_BASE)
        (_, attrs) = res[0]
        return attrs["actionName"][0]

    def isLocked(self):
        res = self.l.search_s(self.dn, ldap.SCOPE_BASE)
        (_, attrs) = res[0]
        return attrs["actionLocked"][0] == "TRUE"

    def lock(self):
        self.l.modify_s(self.dn, [(ldap.MOD_REPLACE, "actionLocked", "TRUE")])

    def unlock(self):
        self.l.modify_s(self.dn, [(ldap.MOD_REPLACE, "actionLocked", "FALSE")])

    def delete(self):
        self.l.delete_s(self.dn)

    def __str__(self):
        return "Action: " + self.dn + ", " + self.getDescription()

    def execute(self):
        res = self.l.search_s(self.dn, ldap.SCOPE_BASE)
        (_, attrs) = res[0]

        if attrs["actionName"][0] == "createGroupDir":
            return self.createGroupDir(attrs)
        elif attrs["actionName"][0] == "removeGroupDir":
            return self.removeGroupDir(attrs)
        elif attrs["actionName"][0] == "removeGroup":
            return self.removeGroup(attrs)
        elif attrs["actionName"][0] == "removeMailbox":
            return self.removeMailbox(attrs)
        elif attrs["actionName"][0] == "createHomeDir":
            return self.createHomeDir(attrs)
        elif attrs["actionName"][0] == "removeHomeDir":
            return self.removeHomeDir(attrs)
        elif attrs["actionName"][0] == "removeUser":
            return self.removeUser(attrs)
        else:
            raise Exception("unknown actionName: " + attrs["actionName"][0])

    def removeMailbox(self, attrs):
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

    def removeGroupDir(self, attrs):
        if not config.enableGroupDirRemoval:
            raise Exception("Group directory removal not enabled on host " + self.getHost())

        group = Group(self.l, self.getAffectedDN())
        homedir = abspath(os.path.join(config.groupDirBase, config.groupLocations[group.getParent()], group.getCN()))

        if not exists(homedir):
            raise Exception("Group directory " + homedir + " doesn't exist!")
        if not homedir.startswith(config.groupDirBase):
            raise Exception("Group directories must be created in " + config.groupDirBase)

        tar = tarfile.open(
            os.path.join(config.graveyardDir, "GROUP_" + group.getCN() + "-" + str(int(time())) + ".tar.gz"), "w:gz"
        )
        tar.add(homedir)
        tar.close()
        rmtree(homedir)

        return True

    def createGroupDir(self, attrs):
        if not config.enableGroupDirCreation:
            raise Exception("Group directory creation not enabled on host " + self.getHost())

        group = Group(self.l, self.getAffectedDN())
        homedir = abspath(os.path.join(config.groupDirBase, config.groupLocations[group.getParent()], group.getCN()))

        if exists(homedir):
            raise Exception("Group directory " + homedir + " already exists!")
        if not homedir.startswith(config.groupDirBase):
            raise Exception("Group directories must be created in " + config.homeDirBase)

        makedirs(homedir)
        self.chownTree(homedir, 0, group.getGIDNumber())
        os.system(
            "setfacl -R --set u::rwx,g::rwx,o:---,d:o:---,d:g::---,d:u::rwx,d:g:vc:rx,g:vc:rx,d:g:bestuur:rx,g:bestuur:rx,d:g:"
            + group.getCN()
            + ":rwx,g:"
            + group.getCN()
            + ":rwx "
            + homedir
        )

        return True

    def removeGroup(self, attrs):
        if not config.enableGroupRemoval:
            raise Exception("Group removal not enabled on host " + self.getHost())

        self.l.delete_s(self.getAffectedDN())
        return True

    def createHomeDir(self, attrs):
        if not config.enableHomeDirCreation:
            raise Exception("Home directory creation not enabled on host " + self.getHost())

        user = User(self.l, self.getAffectedDN())
        homedir = abspath(user.getHomeDirectory(self.getHost()))

        if exists(homedir):
            raise Exception("Home directory " + homedir + " already exists!")
        if not homedir.startswith(config.homeDirBase):
            raise Exception("Home directories must be created in " + config.homeDirBase)

        makedirs(homedir)
        self.copyTree(config.skelDir, homedir)
        self.chmodTree(homedir, 0o600, 0o700)
        self.chownTree(homedir, user.getUIDNumber(), user.getGIDNumber())

        return True

    def removeHomeDir(self, attrs):
        if not config.enableHomeDirRemoval:
            raise Exception("Home directory removal not enabled on host " + self.getHost())

        user = User(self.l, self.getAffectedDN())
        homedir = abspath(user.getHomeDirectory(self.getHost()))

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

    def removeUser(self, attrs):
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
