import os
import datetime

from groups import getGoogleGroups
from create_group_with_members import createGoogleGroupWithMembers


if __name__ == "__main__":
    
    logfile_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/logs")
    logfile_name = "export"+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+".log"

    # Create logfile directory if it does not exist

    if not os.path.exists(logfile_path):
        os.makedirs(logfile_path)

    filename = "aliassenLDAPExport.xlsx - Sheet1.csv"


    groups = getGoogleGroups()

    with open(os.path.join(logfile_path, logfile_name), "w") as logfile:

        # Read CSV file
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", filename), "r") as csv_file:
            lines = csv_file.readlines()
            for line in lines:
                line = line.strip()
                if line:
                    # Split line
                    parts = line.split(",")
                    group_name = parts[0].strip()
                    used = parts[1].strip()
                    member_string = parts[2].strip()
                    item_type = parts[17].strip()

                    # Skip all aliases that are not used since 2022-05-23
                    if used != "TRUE":
                        continue

                    # Only import aliases that are of type "Group"
                    if item_type != "Group":
                        continue

                    members = member_string.split("|")

                    # Create group
                    createGoogleGroupWithMembers(group_name=group_name, group_domain="ch.tudelft.nl", logfile=logfile, domains=["ch.tudelft.nl", "wisv.ch"], users=members, groups=groups)