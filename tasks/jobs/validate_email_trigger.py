from datetime import datetime
from tasks.jobs.send_email import send_email
from tasks.worker import app, flask_app
from portal.helpers import isProd
from portal import LOG
from portal.services.mail import _send_mail_via_gmail_backup

DISABLE_SENDING_EMAIL_TEMPORARILY = False

@app.task(name='validate_email_trigger')
def validate_email_trigger():
    # Try sending email
    if isProd() != True:
        return False
    today = str(datetime.now())
    LOG.info("job:validate_email_trigger:started")
    to_address = ['shaik.farooq@manomay.biz','shaik.farooq@manomay.biz']
    subject = "Email Trigger Check"
    body = f'''<p>Emails trigger - Check O.K</p><p>{today}</p>'''
    status = send_email(to_address, subject, body)
    if status is True:
        LOG.info("job:validate_email_trigger:Email triggers working Fine")
    else:
        LOG.info("job:validate_email_trigger:Email Trigger")
        to_address = ['aramos@saxon.ky','mwright@saxon.ky','neetha.pasham@manomay.biz','shaik.farooq@manomay.biz']
        subject = "Email Trigger Check- Failed"
        body = f'''<p>Emails trigger - Check Failed</p>
                    <p>{today}</p>
                    <p>Causes of email</p>
                    <p>{status}</p>
                    '''
        _send_mail_via_gmail_backup(to_address=to_address,body=body,subject=subject)
        LOG.info("job:validate_email_trigger:Handled the error of triggering emails,%s",status)