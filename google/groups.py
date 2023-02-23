import ldap
import ldapconn as settings

import local as env
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def getGoogleService(scopes=[]):
    """Returns a Google Directory API service object"""
    credentials = service_account.Credentials.from_service_account_file(env.GOOGLE_SERVICE_ACCOUNT, scopes=scopes)
    delegated_credentials = credentials.with_subject(env.GOOGLE_ADMIN_EMAIL)
    return build("admin", "directory_v1", credentials=delegated_credentials)


def getGoogleGroups(domains=["wisv.ch", "ch.tudelft.nl"]):
    """Returns all Google Groups"""
    service = getGoogleService(
        [
            "https://www.googleapis.com/auth/admin.directory.group.readonly",
            "https://www.googleapis.com/auth/admin.directory.group.member.readonly",
        ]
    )

    groups = []
    for domain in domains:
        data = service.groups().list(domain=domain).execute()
        if "groups" in data:
            groups += data["groups"]
    return groups


def getGoogleGroup(group_name):
    """Returns a Google Group object with the members"""
    service = getGoogleService(
        [
            "https://www.googleapis.com/auth/admin.directory.group.readonly",
            "https://www.googleapis.com/auth/admin.directory.group.member.readonly",
        ]
    )

    group = service.groups().get(groupKey=group_name).execute()
    members = service.members().list(groupKey=group_name).execute()

    output = {}
    output["name"] = group["name"]
    output["email"] = group["email"]
    output["directMembersCount"] = group["directMembersCount"]
    output["description"] = group["description"]
    output["members"] = []
    if members and "members" in members:
        for member in members["members"]:
            output["members"] += [member["email"]]
    return output


def createGoogleGroup(email, name, description=""):
    """Creates a Google Group"""
    service = getGoogleService(["https://www.googleapis.com/auth/admin.directory.group"])
    group = {"email": email, "name": name, "description": description}

    try:
        service.groups().insert(body=group).execute()
    except HttpError as e:
        if e.resp.status == 409:
            print("- Group {} already exists".format(email))
        else:
            raise e


def addMemberToGoogleGroup(email, group_name, role="MEMBER"):
    """Adds a member to a Google Group"""
    service = getGoogleService(["https://www.googleapis.com/auth/admin.directory.group.member"])
    member = {"email": email, "role": role}

    try:
        service.members().insert(groupKey=group_name, body=member).execute()
    except HttpError as e:
        if e.resp.status == 409:
            print("- Member {} already exists in group {}".format(email, group_name))
        else:
            raise e


def getAllLdapGroups(filter_data=False):
    """Returns all groups under LDAP_GROUPDN, in a dictionary sorted by their ou"""
    ld = ldap.initialize(settings.LDAP_HOST)

    if filter_data:
        filter_string = "(&"
        if filter_data["uid"]:
            filter_string += "(memberUid=*" + filter_data["uid"] + "*)"
        if filter_data["cn"]:
            filter_string += "(cn=*" + filter_data["cn"] + "*)"
        filter_string += "(objectClass=posixGroup))"
    else:
        filter_string = "(objectClass=posixGroup)"

    res = ld.search_s(settings.LDAP_GROUPDN, ldap.SCOPE_SUBTREE, filter_string)

    res.sort()
    ret = {}
    for dn, attrs in res:
        # TODO: finish
        print(dn, attrs)
        # group = Group(dn, attrs)
        # if not group.parent in ret:
        #     ret[group.parent] = []
        # ret[group.parent] += [group]
    return ret


if __name__ == "__main__":
    print(getAllLdapGroups())
