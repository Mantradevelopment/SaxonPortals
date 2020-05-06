from datetime import datetime
from portal import LOG
from portal.models import db
from portal.models.users import Users
from portal.models.member_view import MemberView
from portal.models.roles import *
from portal.models.status import *
from tasks.worker import app


DEFAULT_LIMIT = 5000

@app.task(name='create_member_accounts')
def create_member_accounts(limit=DEFAULT_LIMIT):
    LOG.info("job:create_member_accounts:started")
    offset_ = 0
    count = MemberView.query.count()
    count = int(count / limit) + 1
    for i in range(count):
        try:
            LOG.debug("job:create_member_accounts:Going to fetch %s members from offset %s", count, offset_)
            members = MemberView.query.offset(offset_).limit(limit).all()
            LOG.info("job:create_member_accounts:%s members fetched successfully from offset %s", len(members), offset_)
            for member in members:
                try:
                    _upsert_member(member)
                except Exception as e:
                    db.session.rollback()
                    LOG.warning("job:create_member_accounts:There was an unexpected error while upserting a member: %s", e)

        except Exception as e:
            LOG.warning("job:create_member_accounts:There was an unexpected error while processing MembersView items. %s", e)
        finally:
            offset_ += (limit -  1)
    LOG.info("job:create_member_accounts:done:offset_: %s", offset_)


def _upsert_member(member):
    user = Users.query.filter_by(Username=member.MEMNO).scalar()
    if user is None:
        LOG.debug("job:create_member_accounts:Member with username '%s' does not exist. Inserting...", member.MEMNO)
        user = Users(UserID=member.MKEY,
                        Username=member.MEMNO,
                        Email=member.EMAIL,
                        DisplayName=_get_display_name(member),
                        Role=ROLES_MEMBER,
                        Status=STATUS_ACTIVE)
        db.session.add(user)
    else:
        LOG.debug("job:create_member_accounts:Member with username '%s' found. Updating...", member.MEMNO)
        user.Email = member.EMAIL
        user.DisplayName = _get_display_name(member)
        user.Role = ROLES_MEMBER
        user.Status = STATUS_ACTIVE

    db.session.commit()


def _get_display_name(member):
    return (member.FNAME if member.FNAME is not None else "") + \
        " " + \
        (member.LNAME if member.LNAME is not None else "")
