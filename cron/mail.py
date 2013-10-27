#!/usr/bin/env python

import smtplib
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

    s = smtplib.SMTP()
    s.connect()
    s.sendmail(email, [email], msg.as_string())
    s.close()
