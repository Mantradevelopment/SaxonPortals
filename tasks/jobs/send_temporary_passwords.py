from sqlalchemy import text
from datetime import datetime
from flask import render_template
from portal import LOG
from portal.models import db
from portal.models.users import Users
from portal.models.email_track import EmailTrack
from portal.models.member_view import MemberView
from portal.helpers import randomStringwithDigitsAndSymbols, isProd
from portal.encryption import Encryption
from tasks.jobs.send_email import send_email
from tasks.worker import app, flask_app


DISABLE_SENDING_EMAIL_TEMPORARILY = False

@app.task(name='send_temporary_passwords')
def send_temporary_passwords():
    LOG.info("job:send_temporary_passwords:started")
    LOG.info("job:send_temporary_passwords:employers:started")
    _send_to_employers()
    LOG.info("job:send_temporary_passwords:employers:done")
    LOG.info("job:send_temporary_passwords:members:started")
    _send_to_members()
    LOG.info("job:send_temporary_passwords:members:done")
    LOG.info("job:send_temporary_passwords:done")


def _send_to_employers():
    # query should be without semicolon
    employers_sql_query='select erkey from CV$IF_EMPLOYER where termdate is null or termdate >= sysdate'
    employers_result = db.get_engine(bind='readonly').execute(text(employers_sql_query))
    employers_erkeys = [row[0] for row in employers_result]
    LOG.info('job:send_temporary_passwords:debug:Fetched %s number of ERKEYS from EmployerView', len(employers_erkeys))
    _employer_counter = 0
    for erkey in employers_erkeys:
        user = Users.query.filter_by(UserID=erkey).first()
        if user is None:
            LOG.info('job:send_temporary_passwords:debug: User for erkey=%s notfound', erkey)
            continue
        if EmailTrack.query.filter_by(UserID=user.UserID, EmailType='temporary_password').count() != 0:
            LOG.info('job:send_temporary_passwords:debug: Ignore user erkey=%s, email has been sent before', erkey)
            continue
        try:
            random_password = randomStringwithDigitsAndSymbols()
            enc_random_pass = Encryption().encrypt(random_password)
            user.Password = enc_random_pass
            user.TemporaryPassword = True
            user.UserCreatedTime = datetime.utcnow()
            db.session.commit()
            _send_email(user.Email, user.DisplayName, user.Username, random_password, user.UserID, 'employers')
            _employer_counter += 1
        except Exception as e:
            LOG.error(e)
            continue

    LOG.info('job:send_temporary_passwords:debug:Sent email to %s employers', _employer_counter)
    return True

def _send_to_members():
    # query should be without semicolon
    members_sql="select mkey from CV$IF_MEM_EMP_HIS where erkey in ('021',	'025',	'038',	'039',	'040',	'045',	'046',	'053',	'058',	'059',	'062',	'101',	'112',	'121',	'177',	'178',	'179',	'215',	'234',	'236',	'241',	'251',	'259',	'267',	'281',	'312',	'381',	'460',	'522',	'567',	'584',	'619',	'650',	'665',	'845',	'886',	'922',	'928',	'941',	'962',	'AAX',	'ABL',	'ACX',	'ADT',	'AFH',	'AGA',	'AIZ',	'BDA',	'BEQ',	'BFH') and emp_status = 'Full-Time'"
    members_result = db.get_engine(bind='readonly').execute(text(members_sql))
    members_emkeys = [row[0] for row in members_result]
    LOG.info('job:send_temporary_passwords:members:Fetched %s number of EMKEYS from MemberView', len(members_emkeys))
    _member_counter = 0

    for emkey in members_emkeys:
        user = Users.query.filter_by(UserID=emkey).first()
        if user is None:
            LOG.info('job:send_temporary_passwords:members: User for emkey=%s notfound', emkey)
            continue
        if EmailTrack.query.filter_by(UserID=user.UserID, EmailType='temporary_password').count() != 0:
            LOG.info('job:send_temporary_passwords:members: Ignore user emkey=%s, email has been sent before', emkey)
            continue
        try:
            random_password = randomStringwithDigitsAndSymbols()
            enc_random_pass = Encryption().encrypt(random_password)
            user.Password = enc_random_pass
            user.TemporaryPassword = True
            user.UserCreatedTime = datetime.utcnow()
            db.session.commit()
            _send_email(user.Email, user.DisplayName, user.Username, random_password, user.UserID, 'members')
            _member_counter += 1
        except Exception as e:
            LOG.error(e)
            continue
    LOG.info('job:send_temporary_passwords:members:Scheduled to send email to %s members', len(_member_counter))
    return True



def _track_email(email, user_id):
    t = EmailTrack(
        Email=email,
        UserID=user_id,
        EmailType='temporary_password',
        CreatedDate=datetime.utcnow(),
    )
    db.session.add(t)
    db.session.commit()
    return



def _send_email(email, name, username, password, user_id, user_type):
    if DISABLE_SENDING_EMAIL_TEMPORARILY:
        return True

    if isProd() != True:
        return False

    if email is None:
        return False

    subject = "Silver Thatch Pensions Member Portal"
    body = render_template(f'emails/send_temporary_passwords/{user_type}.html',
            frontend_url=flask_app.config["FRONTEND_URL"],username=username,password=password)

    sent = send_email(to_address=email,subject=subject,body=body)
    if sent is True:
        _track_email(email, user_id)
    else:
        LOG.error('job:members-tmp-pass-gen:Unable to send email,%s',status)

    return True
