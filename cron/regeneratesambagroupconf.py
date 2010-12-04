#!/usr/bin/env python
import config
import os


def regenSambaGroupConf():
    outFile='/etc/samba/shares_auto.conf'

    output = "# Automatically generated. Do Not Edit!"

    for parent in ("commissies", "besturen", "overig"):
	for dir in os.listdir(os.path.join(config.groupDirBase, parent)):
	    dirname = os.path.join(config.groupDirBase, parent, dir)
	    if not os.path.isdir(dirname):
		continue
	    if dir == "generator":
		continue
	    output += "\n"
	    output += "[" + dir + "]\n"
	    output += "path = " + dirname + "\n"
	    output += "browseable = no\n"
	    output += "readonly = no\n"
	    output += "hide files = /desktop.ini/Desktop.ini/$RECYCLE.BIN/Thumbs.db/~$*/\n"

    f = open(outFile, "w")
    f.write(output)
    f.close()
