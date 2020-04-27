from datetime import datetime
from portal import LOG
from portal.models import db
from portal.helpers import randomStringwithDigitsAndSymbols
from portal.encryption import Encryption
from portal.models.users import Users
from tasks.worker import app, flask_app


@app.task(name='send_temporary_passwords')
def send_temporary_passwords():
    LOG.info("job:send_temporary_passwords:started")
    users = Users.query.filter(Users.Password.is_(None)).all()
    for user in users:
        try:
            random_password = randomStringwithDigitsAndSymbols()
            enc_random_pass = Encryption().encrypt("test")
            user.Password = enc_random_pass
            user.TemporaryPassword = True
            user.UserCreatedTime = datetime.utcnow()
            db.session.commit()
        except Exception as e:
            LOG.error(e)
            continue
        # msg_text = f'<p>Dear {user.DisplayName}</p>' + \
        #            f'<p>Your account has been created</p>' + \
        #            f'<p>Username is {user.Username}</p>' + \
        #            f'<p> please use this password {"test"} to log in</p>' + \
        #            f'<p> Please ensure that you are not copying any extra spaces</p>' \
        #            f'<p>Please use below link to login</p>' \
        #            f'<p>{APP.config["FRONTEND_URL"]}/login</p>'
        # if user.Email is not None:
        #     send_email(user.Email, "Welcome to Pension Management portal", body=msg_text)
    LOG.info("job:send_temporary_passwords:done")
