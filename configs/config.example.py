localHostname = "hendrik.chnet"
adminMail = "pccom@ch.tudelft.nl"

# LDAP Settings
ldapServername = "ldaps://ank.chnet"
ldapUsername = "cn=admin,dc=ank,dc=chnet"
f = open("/etc/ldap.secret")
ldapPass = f.read().strip()
f.close()

ldapActionsOU = "ou=Actions,dc=ank,dc=chnet"
ldapGroupOU = "ou=Group,dc=ank,dc=chnet"
ldapUserOU = "ou=People,dc=ank,dc=chnet"

# Users & Groups
enableUserRemoval = True
enableGroupRemoval = True

# Group directories
enableGroupDirCreation = False
enableGroupDirRemoval = False
enableSambaShareRegen = False
groupDirBase = "/export/groepen/userman_test/"
groupLocations = {"Commissies": "commissies", "Overig": "overig"}

# Home directories
enableHomeDirCreation = False
enableHomeDirMove = False
enableHomeDirRemoval = False
enableProfileRemoval = False
enableQuotas = False
homeDirBase = "/export/gebruikers/"
profileDir = "/export/gebruikers/ntprofile/"
skelDir = "/etc/skel/"
graveyardDir = "/var/local/graveyard/"
mailDir = "/var/mail/"
quotaString = "30000 32500 0 0 -a /dev/sdc3"

# Mailboxes
enableMailboxCreation = False
enableMailboxRemoval = True
enableMailboxRename = True
