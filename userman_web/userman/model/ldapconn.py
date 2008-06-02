#!/usr/bin/env python
from django.conf import settings
import ldap

class LDAPConn (object):
    def __init__(self):
        self.connected = False

    def connectAnon(self):
        if self.connected:
            return
        self.l = ldap.initialize(settings.LDAP_HOST)
        self.connected = True

    def connectRoot(self):
        if self.connected:
            return
        self.l = ldap.initialize(settings.LDAP_HOST)
        self.l.simple_bind_s(settings.LDAP_USER, settings.LDAP_PASS)
        self.connected = True

    def disconnect(self):
        if not self.connected:
            return
        self.l.unbind()
        self.connected = False

    def modifyEntries(self, changes):
        if not self.dn:
            raise Exception, "The object you are modifying has no dn"
        mod_attrs = [ (ldap.MOD_REPLACE, k, v) for (k, v) in changes.items() ]
        self.l.modify_s(self.dn, mod_attrs)

    def addEntries(self, changes):
        if not self.dn:
            raise Exception, "The object you are modifying has no dn"
        mod_attrs = [ (ldap.MOD_ADD, k, v) for (k, v) in changes.items() ]
        self.l.modify_s(self.dn, mod_attrs)

    def removeEntries(self, changes):
        if not self.dn:
            raise Exception, "The object you are modifying has no dn"
        mod_attrs = [ (ldap.MOD_DELETE, k, v) for (k, v) in changes.items() ]
        self.l.modify_s(self.dn, mod_attrs)
							    