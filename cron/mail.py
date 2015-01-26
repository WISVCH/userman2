#!/usr/bin/env python

import smtplib
import os
from email.MIMEText import MIMEText


def mailAdmin(subject, message):
    msg = MIMEText(message)
    try:
        from django.conf import settings
        email = settings.ADMIN_MAIL
    except ImportError:
        import config
        email = config.adminMail

    msg['Subject'] = '[Userman] ' + subject
    msg['From'] = email
    msg['To'] = email

    sendmail_location = "/usr/sbin/sendmail" # sendmail location
    p = os.popen("%s -t" % sendmail_location, "w")
    p.write(msg.as_string())
    status = p.close()
    if status != None:
           print "Sendmail exit status ", status
