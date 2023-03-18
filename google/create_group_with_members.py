import os
from groups import *
import datetime


def createGoogleGroupWithMembers(group_name: str, group_domain: str, logfile: str, domains=[], users=[], groups = None, execute=False):
    """
    Creates a Google Group with the given name and email [group_name]@[group_domain] and adds the given users to the group.
    If the group already exists, the users are added to the group.
    If the user is already in the group, they are not added again.
    If the user is already in the group with a different company email, they are not added again.

    :param group_name: The name of the group
    :param group_domain: The domain of the group
    :param domains: The search domains for company emails
    :param users: The users to add to the group, this has to be a list of emails
    """
    # Check if group already exists for a different domain
    if not groups:
        groups = getGoogleGroups()

    # Get the part before the @
    group_names = [group["email"].split("@")[0] for group in groups]

    # Check if group already exists
    group = None

    if group_name in group_names:
        group_index = group_names.index(group_name)
        group = groups[group_index]
        print("- Group with alias {} already exists: {}".format(group_name, group["email"]), file=logfile)

        # Get the group members
        group = getGoogleGroup(group["email"])
        for user in users:
            # Check if user is already in group with their company email
            if any(user.endswith(domain) for domain in domains):
                group_member_aliases = [member_email.split("@")[0] for member_email in group["members"]]
                # Check if user is already in group
                if user.split("@")[0] in group_member_aliases:
                    print("-- User {} is already a member of group {}".format(user, group_name), file=logfile)
                    continue
            else:
                # Check if user is already in group with their personal email
                if user in group["members"]:
                    print("-- User {} is already a member of group {}".format(user, group_name), file=logfile)
                    continue

            # Add domain if user does not have an @
            if "@" not in user:
                user += "@" + group_domain

            # Add user to group
            if execute:
                addMemberToGoogleGroup(user, group["email"])
            print("-- Added {} to group {}".format(user, group_name), file=logfile)
    else:
        # Create group
        group_email = "{}@{}".format(group_name, group_domain)
        print("- Creating group {}".format(group_email), file=logfile)
        if execute:
            createGoogleGroup(group_email, group_name)

        # Add users to group
        for user in users:
            # Add domain if user does not have an @
            if "@" not in user:
                user += "@" + group_domain

            if execute:
                addMemberToGoogleGroup(user, group_email)
            print("-- Added {} to group {}".format(user, group_name), file=logfile)


if __name__ == "__main__":
    logfile_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/logs")
    logfile_name = "export"+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+".log"

    # Create logfile directory if it does not exist

    if not os.path.exists(logfile_path):
        os.makedirs(logfile_path)

    with open(os.path.join(logfile_path, logfile_name), "w") as logfile:
        createGoogleGroupWithMembers(
            "test",
            "ch.tudelft.nl",
            logfile,
            ["ch.tudelft.nl", "wisv.ch"],
            ["joepj@ch.tudelft.nl", "testje", "beheer@wisv.ch"],
        )
