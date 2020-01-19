#!/usr/bin/env python3

import os


def mailAdmin(subject, message):
    userman_subject = "[Userman] " + subject
    try:
        from django.conf import settings
        from django.core.mail import send_mail

        email = settings.ADMIN_MAIL
        send_mail(userman_subject, message, email, [email])

    except ImportError:
        import config
        from email.mime.text import MIMEText

        email = config.adminMail
        msg = MIMEText(message)
        msg["Subject"] = userman_subject
        msg["From"] = email
        msg["To"] = email

        sendmail_location = "/usr/sbin/sendmail"  # sendmail location
        p = os.popen("%s -t" % sendmail_location, "w")
        p.write(msg.as_string())
        status = p.close()
        if status is not None:
            print("Sendmail exit status ", status)
