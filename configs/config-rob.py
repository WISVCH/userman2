localHostname = "rob.chnet"
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
groupDirBase = "/export/groepen/userman_test/"
groupLocations = {"Commissies": "commissies", "Overig": "overig"}

# Home directories
enableHomeDirCreation = True
enableHomeDirMove = True
enableHomeDirRemoval = True
homeDirBase = "/home/"
skelDir = "/etc/skel/"
graveyardDir = "/var/local/graveyard/"

# Mailboxes
enableMailboxCreation = False
enableMailboxRemoval = False
enableMailboxRename = False
