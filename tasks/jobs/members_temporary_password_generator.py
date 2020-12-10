import os
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


STATE_FILE_PATH = os.path.join(flask_app.config['DATA_DIR'], '.members_temporary_password_generator.state')
DISABLE_SENDING_EMAIL_TEMPORARILY = False
DEFAULT_LIMIT = 6000

@app.task(name='members_temporary_password_generator')
def members_temporary_password_generator(limit=DEFAULT_LIMIT):
    offset = _get_offset()
    LOG.info("job:members-tmp-pass-gen:started:offset=%s,limit=%s", offset, limit)
    try:
        _send_to_members(offset, limit)
    finally:
        _update_state(offset+limit)
    LOG.info("job:members-tmp-pass-gen:done")



def _send_to_members(offset, limit):
    # query should be without semicolon
    members = MemberView.query.with_entities(MemberView.MKEY).filter(MemberView.PSTATUS != "Terminated").order_by(MemberView.MEMNO.desc()).offset(offset).limit(limit).all()
    LOG.info('job:members-tmp-pass-gen:members:Fetched %s from MemberView', len(members))
    _member_counter = 0

    for emkey2 in members:
        emkey = emkey2[0]
        user = Users.query.filter_by(UserID=emkey).first()
        if user is None:
            LOG.info('job:members-tmp-pass-gen:members: User for emkey=%s notfound', emkey)
            continue
        if EmailTrack.query.filter_by(UserID=user.UserID, EmailType='temporary_password').count() != 0:
            LOG.info('job:members-tmp-pass-gen:members: Ignore user emkey=%s, email has been sent before', emkey)
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
    LOG.info('job:members-tmp-pass-gen:members:%s users got checked.', _member_counter)
    return True



def _track_email(email, user_id):
    t = EmailTrack(
        Email=email,
        UserID=str(user_id),
        EmailType='temporary_password',
        CreatedDate=datetime.utcnow(),
    )
    db.session.add(t)
    db.session.commit()
    LOG.info('job:members-tmp-pass-gen:members:scheduled email for %s', user_id)
    return



def 
(email, name, username, password, user_id, user_type):
    if DISABLE_SENDING_EMAIL_TEMPORARILY:
        return True

    # if isProd() != True:
    #     return False

    if email is None:
        return False

    # subject = "Silver Thatch Pensions Member Portal"
    subject = "Silver Thatch Pensions Member Portal - Testing"
    body = render_template(f'emails/send_temporary_passwords/{user_type}.html',
            frontend_url=flask_app.config["FRONTEND_URL"],username=username,password=password)

    sent = send_email(to_address=email,subject=subject,body=body)
    if sent is True:
        # _track_email(email, user_id)
        pass
    else:
        LOG.error('job:members-tmp-pass-gen:Unable to send email')
    return True




def _get_offset():
    offset = 0
    try:
        with open(STATE_FILE_PATH, 'r') as f:
            content = f.read().strip()
            if content != "":
                offset = int(content)
    except FileNotFoundError:
        with open(STATE_FILE_PATH, 'w+') as f:
            f.write('0')
    return offset


def _update_state(offset):
    count = MemberView.query.count()
    if offset > count:
        LOG.info('job:members-tmp-pass-gen:members: members count(%s) is less than new offset:%s : Updating offset to count', count, offset)
        offset = count
    with open(STATE_FILE_PATH, 'w') as f:
        LOG.info('job:members-tmp-pass-gen:members:Updating state file(%s) with new offset:%s', STATE_FILE_PATH, offset)
        f.write(str(offset))
