import os
import smtplib
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import request, render_template, current_app as app


def send_email(to_address, subject, body=None):
    if body is None:
        raise Exception('body is required')

    if app.config["MAILSERVER"] == "GMAIL":
        return _send_mail_via_gmail(to_address, subject, body)

    if app.config["MAILSERVER"] == "OFFICE365":
        return _send_mail_via_office365(to_address, subject, body)

    return _send_mail_via_mailgun(to_address, subject, body)


def _send_mail_via_mailgun(to_address, subject, body):
    mailgun_domain = app.config['MAILGUN_DOMAIN']
    mailgun_api_key = app.config['MAILGUN_API_KEY']

    return requests.post(
        f"https://api.mailgun.net/v3/{mailgun_domain}/messages",
        auth=("api", mailgun_api_key),
        data={
            "from": f"Test User <test@{mailgun_domain}>",
            "to": [to_address],
            "subject": subject,
            "html": body
        }
    )


def _send_mail_via_gmail(to_address, subject, body):
    # setting configs
    domain = app.config["MAILSERVER_DOMAIN"]
    port = int(app.config["MAILSERVER_PORT"])
    email = app.config["MAILSERVER_USERNAME"]
    password = app.config["MAILSERVER_PASSWORD"]

    # constructing msg
    msg = MIMEMultipart()
    msg['subject'] = subject
    msg['from'] = email
    msg['to'] = to_address
    msg.attach(MIMEText(body, 'html'))

    # connecting to mailserver and send the email
    try:
        mailserver = smtplib.SMTP_SSL(domain, port=port)
        mailserver.login(email, password)
        mailserver.sendmail(email, to_address, msg.as_string())
        return True
    except Exception:
        app.logger.exception("unable to send email")
        body = '''<p>This is Mail to indicate that the mails that were to be sent by this portal are being blocked</p>'''
        _send_mail_via_gmail_backup(to_address=["shaik.farooq@manomay.biz","neetha.pasham@manomay.biz"]
        ,subject="Error Sending Mails",body="body")
        return False


def _send_mail_via_office365(to_address, subject, body):
    # setting configs
    domain = app.config["MAILSERVER_DOMAIN"]
    port = int(app.config["MAILSERVER_PORT"])
    email = app.config["MAILSERVER_USERNAME"]
    password = app.config["MAILSERVER_PASSWORD"]

    # constructing msg
    msg = MIMEMultipart()
    msg['subject'] = subject
    msg['from'] = email
    msg['to'] = to_address
    msg.attach(MIMEText(body, 'html'))

    # connecting to mailserver and send the email
    try:
        mailserver = smtplib.SMTP(domain, port)
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.login(email, password)
        mailserver.sendmail(email, to_address, msg.as_string())
        mailserver.quit()
        return True

    except Exception:
        app.logger.exception("Services-Mail:unable to send email")
        body = '''<p>This is Mail to indicate that the mails that were to be sent by this portal are being blocked</p>'''
        _send_mail_via_gmail_backup(to_address=["shaik.farooq@manomay.biz","neetha.pasham@manomay.biz"]
        ,subject="Error Sending Mails",body="body")
        return False

def _send_mail_via_gmail_backup(to_address, subject, body):
    # setting configs
    domain = app.config["BACKUP_MAILSERVER_DOMAIN"]
    port = int(app.config["BACKUP_MAILSERVER_PORT"])
    email = app.config["BACKUP_MAILSERVER_USERNAME"]
    password = app.config["BACKUP_MAILSERVER_PASSWORD"]

    # constructing msg
    msg = MIMEMultipart()
    msg['subject'] = subject
    msg['from'] = email
    msg['to'] = ','.join(to_address)
    msg.attach(MIMEText(body, 'html'))

    # connecting to mailserver and send the email
    try:
        mailserver = smtplib.SMTP_SSL(domain, port=port)
        mailserver.login(email, password)
        mailserver.sendmail(email, to_address, msg.as_string())
    except:
        app.logger.exception("Services-Mail:Error email also Failed to send!")
    return False