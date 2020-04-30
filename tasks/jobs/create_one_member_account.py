from datetime import datetime
from portal import LOG
from portal.models import db
from portal.models.users import Users
from portal.models.member_view import MemberView
from portal.models.roles import *
from portal.models.status import *
from tasks.worker import app


@app.task(name='create_one_member_account')
def create_one_member_account(mid):
    LOG.info("job:create_one_member_account:started:mid=%s", mid)
    member = MemberView.query.filter_by(MKEY=mid).first()
    if not member:
        LOG.warning("job:create_one_member_account:member %s not found", mid)
        return
    LOG.debug("job:create_one_member_account:member fetched successfully")
    try:
        _upsert_member(member)
    except Exception as e:
        db.session.rollback()
        LOG.warning("job:create_one_member_account:There was an unexpected error while upserting a member: %s", e)
    LOG.info("job:create_one_member_account:done:mid=%s", mid)


def _upsert_member(member):
    user = Users.query.filter_by(Username=member.MEMNO).scalar()
    if user is None:
        LOG.debug("job:create_one_member_account:Member with username '%s' does not exist. Inserting...", member.MEMNO)
        user = Users(UserID=member.MKEY,
                        Username=member.MEMNO,
                        Email=member.EMAIL,
                        DisplayName=_get_display_name(member),
                        Role=ROLES_MEMBER,
                        Status=STATUS_ACTIVE)
        db.session.add(user)
    else:
        LOG.debug("job:create_one_member_account:Member with username '%s' found. Updating...", member.MEMNO)
        user.Email = member.EMAIL
        user.DisplayName = _get_display_name(member)
        user.Role = ROLES_MEMBER
        user.Status = STATUS_ACTIVE
    db.session.commit()


def _get_display_name(member):
    return (member.FNAME if member.FNAME is not None else "") + \
        " " + \
        (member.LNAME if member.LNAME is not None else "")
