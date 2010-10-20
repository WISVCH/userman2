localHostname = "rob.chnet"
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

# Group directories
enableGroupDirCreation = False
enableGroupDirRemoval = False
enableSambaShareRegen = False
groupDirBase = "/export/groepen/userman_test/"
groupLocations = { 'Commissies': 'commissies', 'Overig' : 'overig' }

# Home directories
enableHomeDirCreation = True
enableHomeDirMove = True
enableHomeDirRemoval = True
enableProfileRemoval = False
enableQuotas = False
homeDirBase = "/home/"
profileDir = "/home/ntprofile/"
skelDir = "/etc/skel/"
graveyardDir = "/var/graveyard/"
quotaString = "30000 32500 0 0 -a /dev/sdc3"

# Mailboxes
enableMailboxCreation = False
enableMailboxRemoval = False
enableMailboxRename = False
