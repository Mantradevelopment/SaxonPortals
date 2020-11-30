from portal import LOG
from portal.services.mail import send_email as send_email_sync
from tasks.worker import app


@app.task(name='send_email')
def send_email(to_address, subject, body):
    LOG.info('job:send_email:started')
    return send_email_sync(to_address, subject, body)
    LOG.info('job:send_email:done')
