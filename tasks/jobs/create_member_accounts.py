from datetime import datetime
from portal import LOG
from portal.models import db
from portal.models.users import Users
from portal.models.member_view import MemberView
from portal.models.roles import *
from portal.models.status import *
from tasks.worker import app


@app.task(name='create_member_accounts')
def create_member_accounts():
    LOG.debug("Starting creating member accounts")
    offset_ = 0
    count = MemberView.query.count()
    count = int(count / 100) + 1
    for i in range(count):
        try:
            LOG.debug("Going to fetch %s members from offset %s", count, offset_)
            members = MemberView.query.offset(offset_).limit(100).all()
            LOG.debug("%s members fetched successfully from offset %s", len(members), offset_)
            for member in members:
                try:
                    # userExists = Users.query.filter_by(Username=member.MEMNO).scalar()
                    # if userExists is not None:
                    #     LOG.debug("Member with username '%s' exists. Skip adding...", member.MEMNO)
                    #     continue

                    LOG.debug("Member with username '%s' does not exist. Inserting...", member.MEMNO)
                    user = Users(UserID=member.MKEY,
                                    Username=member.MEMNO,
                                    Email=member.EMAIL,
                                    DisplayName=(member.FNAME if member.FNAME is not None else "") + " " + (
                                        member.LNAME if member.LNAME is not None else ""),
                                    Role=ROLES_MEMBER,
                                    Status=STATUS_ACTIVE)
                    db.session.merge(user)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    LOG.warning("There was an unexpected error while creating new user from MembersView. %s", e)

        except Exception as e:
            LOG.warning("There was an unexpected error while processing MembersView items. %s", e)
        finally:
            offset_ += 99
