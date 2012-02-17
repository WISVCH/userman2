#!/usr/bin/env python

import smtplib
from email.MIMEText import MIMEText

def mailAdmin(subject, message):
    msg = MIMEText(message)
    msg['Subject'] = '[Userman] ' + subject
    msg['From'] = config.adminMail
    msg['To'] = config.adminMail

    s = smtplib.SMTP()
    s.connect()
    s.sendmail(config.adminMail, [config.adminMail], msg.as_string())
    s.close()