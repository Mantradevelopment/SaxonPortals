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
    LOG.debug("Employers fetched: %s", len(employers))
    for employer in employers:
        try:
            # employer_valid = MemberView.query.filter(MemberView.MEMNO == employer.ERNO).scalar()
            # if employer_valid is not None:
            #     continue
            user = Users(UserID=employer.ERKEY,
                            Username=employer.ERNO,
                            Email=employer.EMAIL,
                            DisplayName=employer.ENAME,
                            Role=ROLES_EMPLOYER,
                            Status=
                                STATUS_INACTIVE if employer.TERMDATE is not None and employer.TERMDATE < datetime.utcnow()
                                else STATUS_ACTIVE)
            db.session.merge(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            LOG.warning(e)
            continue
    LOG.info("job:create_employer_accounts:done")
