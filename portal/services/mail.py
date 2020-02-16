import os
import smtplib
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import request, render_template, current_app as app


def send_email(to_address, subject, body=None, template=None):
    if template is None and body is None:
        raise Exception('One of body/template is required')

    if template:
        body = render_template(os.path.join('emails', template))

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
