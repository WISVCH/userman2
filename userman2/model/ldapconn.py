#!/usr/bin/env python
from django.conf import settings
import ldap

class LDAPConn (object):
    def __init__(self):
        self.connected = False

    def connectAnon(self):
        if self.connected:
            return
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)
        self.l = ldap.initialize(settings.LDAP_HOST)
        self.connected = True

    def connectRoot(self):
        if self.connected:
            return
        self.l = ldap.initialize(settings.LDAP_HOST)
        self.l.simple_bind_s(settings.LDAP_USER, settings.LDAP_PASSWORD)
        self.connected = True

    def disconnect(self):
        if not self.connected:
            return
        self.l.unbind()
        self.connected = False

    def modifyEntries(self, changes):
        if not self.dn:
            raise Exception, "The object you are modifying has no dn"
        if not self.connected:
            self.connectRoot()
        mod_attrs = [ (ldap.MOD_REPLACE, k, v) for (k, v) in changes.items() ]
        self.l.modify_s(self.dn, mod_attrs)

    def addEntries(self, changes):
        if not self.dn:
            raise Exception, "The object you are modifying has no dn"
        if not self.connected:
            self.connectRoot()
        mod_attrs = [ (ldap.MOD_ADD, k, v) for (k, v) in changes.items() ]
        self.l.modify_s(self.dn, mod_attrs)

    def addObject(self, dn, changes):
        if not self.connected:
            self.connectRoot()
        mod_attrs = []
        for (k, v) in changes.items():
            if isinstance(v, unicode):
                mod_attrs.append((k, str(v)))
            else:
                mod_attrs.append((k, v))
        self.l.add_s(dn, mod_attrs)

    def delObject(self):
        if not self.dn:
            raise Exception, "The object you are removing has no dn"
        if not self.connected:
            self.connectRoot()
        self.l.delete_s(self.dn)

    def removeEntries(self, changes):
        if not self.dn:
            raise Exception, "The object you are modifying has no dn"
        if not self.connected:
            self.connectRoot()
        mod_attrs = []
        for (k, v) in changes.items():
            if isinstance(v, unicode):
                mod_attrs.append((ldap.MOD_DELETE, k, str(v)))
            else:
                mod_attrs.append((ldap.MOD_DELETE, k, v))

        self.l.modify_s(self.dn, mod_attrs)