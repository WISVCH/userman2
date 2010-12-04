localHostname = "ank.chnet"
adminMail = 'pccom@ch.tudelft.nl'

# LDAP Settings
ldapServername = "ldaps://frans.chnet"
ldapUsername = "cn=admin,dc=ank,dc=chnet"
f = open("/etc/ldap.secret")
ldapPass = f.read().strip()
f.close()

ldapActionsOU = "ou=Actions,dc=ank,dc=chnet"
ldapGroupOU = "ou=Group,dc=ank,dc=chnet"
ldapUserOU = "ou=People,dc=ank,dc=chnet"
ldapMachineOU = "ou=Computers,dc=ank,dc=chnet"

# Users & Groups
enableUserRemoval = True
enableGroupRemoval = True

# generation of loginscripts
enableLoginScriptGen = True
loginScriptDir = "/export/netlogon/"
loginScriptTemplate = loginScriptDir + "logintemplate"
loginScriptKixTemplate = loginScriptDir + "loginkixtemplate"
loginScriptKixEndTemplate = loginScriptDir + "loginkixendtemplate"

# Group directories
enableGroupDirCreation = True
enableGroupDirRemoval = True
enableSambaShareRegen = True
groupDirBase = "/export/groepen/"
groupLocations = { 'Commissies': 'commissies', 'Overig' : 'overig' }

# Home directories
enableHomeDirCreation = True
enableHomeDirMove = True
enableHomeDirRemoval = True
enableProfileRemoval = True
enableQuotas = False
homeDirBase = "/export/gebruikers/"
profileDir = "/export/gebruikers/ntprofile/"
skelDir = "/etc/skel/"
graveyardDir = "/var/local/graveyard/"
quotaString = "30000 32500 0 0 -a /dev/sdc3"

# Mailboxes
enableMailboxCreation = False
enableMailboxRemoval = False
enableMailboxRename = False

