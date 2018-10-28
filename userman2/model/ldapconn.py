#!/usr/bin/env python3
import logging

from django.conf import settings
import ldap

auditlog = logging.getLogger("userman2.audit")


class LDAPConn(object):
    def __init__(self):
        self.connected = False
        self.dn = None

    def connectAnon(self):
        if self.connected:
            return
        auditlog.debug("LDAP connected as anonymous.")
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_HARD)
        self.l = ldap.initialize(settings.LDAP_HOST)
        self.connected = True

    def connectRoot(self):
        if self.connected:
            return
        auditlog.debug("LDAP connected as root.")
        self.l = ldap.initialize(settings.LDAP_HOST)
        self.l.simple_bind_s(settings.LDAP_USER, settings.LDAP_PASSWORD)
        self.connected = True

    def disconnect(self):
        if not self.connected:
            return
        auditlog.info("LDAP disconnected as anon.")
        self.l.unbind()
        self.connected = False

    def modifyEntries(self, changes):
        if not self.dn:
            raise Exception("The object you are modifying has no dn")
        if not self.connected:
            self.connectRoot()
        auditlog.info("Modify dn '%s' entries %s", self.dn, changes)
        mod_attrs = [(ldap.MOD_REPLACE, k, v.encode()) for (k, v) in changes.items()]
        self.l.modify_s(self.dn, mod_attrs)

    def addEntries(self, changes):
        if not self.dn:
            raise Exception("The object you are modifying has no dn")
        if not self.connected:
            self.connectRoot()
        auditlog.info("Add to dn '%s' entries %s", self.dn, changes)
        mod_attrs = [(ldap.MOD_ADD, k, v.encode()) for (k, v) in changes.items()]
        try:
            self.l.modify_s(self.dn, mod_attrs)
        except ldap.TYPE_OR_VALUE_EXISTS:
            auditlog.error("FAILED (TYPE_OR_VALUE_EXISTS): Add to dn '%s' entries %s", self.dn, changes)
            raise LDAPError("Attribute already exists.")

    def addObject(self, dn, changes):
        if not self.connected:
            self.connectRoot()
        mod_attrs = []
        for (k, v) in changes.items():
            if isinstance(v, str):
                mod_attrs.append((k, v.encode()))
            elif isinstance(v, list):
                mod_attrs.append((k, list(map(lambda s: s.encode(), v))))
            else:
                mod_attrs.append((k, v))
        print(mod_attrs)
        auditlog.info("Add object dn '%s' with entries %s", dn, mod_attrs)
        self.l.add_s(dn, mod_attrs)

    def delObject(self):
        if not self.dn:
            raise Exception("The object you are removing has no dn")
        if not self.connected:
            self.connectRoot()
        auditlog.info("Delete object with dn '%s'", self.dn)
        self.l.delete_s(self.dn)

    def removeEntries(self, changes):
        if not self.dn:
            raise Exception("The object you are modifying has no dn")
        if not self.connected:
            self.connectRoot()
        mod_attrs = []
        for (k, v) in changes.items():
            if isinstance(v, str):
                mod_attrs.append((ldap.MOD_DELETE, k, v.encode()))
            elif isinstance(v, list):
                mod_attrs.append((ldap.MOD_DELETE, k, list(map(lambda s: s.encode(), v))))
            else:
                mod_attrs.append((ldap.MOD_DELETE, k, v))

        auditlog.info("Remove from dn '%s' entries %s", self.dn, mod_attrs)
        self.l.modify_s(self.dn, mod_attrs)


class LDAPError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return repr(self.message)