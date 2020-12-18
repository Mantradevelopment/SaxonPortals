from datetime import datetime
from portal import LOG
from portal.models import db
from portal.models.users import Users
from portal.models.member_view import MemberView
from portal.models.employer_view import EmployerView
from portal.models.roles import *
from portal.models.status import *
from tasks.worker import app

@app.task(name='create_employer_accounts')
def create_employer_accounts():
    LOG.info("job:create_employer_accounts:started")
    employers = EmployerView.query.all()
    LOG.info("job:create_employer_accounts: %s employers fetched", len(employers))

    for employer in employers:
        try:
            _upsert_employer(employer)
        except Exception as e:
            db.session.rollback()
            LOG.warning(e)
            continue
    LOG.info("job:create_employer_accounts:done")


def _upsert_employer(employer):
    user = Users.query.filter_by(Username=employer.ERNO).scalar()
    if user is None:
        LOG.debug("job:create_employer_accounts:Employer with username '%s' does not exist. Inserting...", employer.ERNO)
        user = Users(UserID=employer.ERKEY,
                        Username=employer.ERNO,
                        Email=employer.EMAIL,
                        DisplayName=employer.ENAME,
                        Role=ROLES_EMPLOYER,
                        Status=_get_status(employer))
        db.session.add(user)
    else:
        LOG.debug("job:create_employer_accounts:Employer with username '%s' found. Updating...", employer.ERNO)
        user.Email = employer.EMAIL
        user.DisplayName = employer.ENAME
        user.Role = ROLES_EMPLOYER
        user.Status = _get_status(employer)
    db.session.commit()


def _get_status(employer):
    return STATUS_INACTIVE \
        if (employer.TERMDATE is not None and employer.TERMDATE < datetime.utcnow()) \
        else STATUS_ACTIVE
