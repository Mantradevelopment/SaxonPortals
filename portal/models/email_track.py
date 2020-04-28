from sqlalchemy import Sequence

from . import db


class EmailTrack(db.Model):
    __bind_key__ = 'writeonly'

    EmailTrackID = db.Column(db.Integer, Sequence('emailtrack_id_seq'), primary_key=True, nullable=False)
    UserID = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), nullable=False)
    EmailType = db.Column(db.String(255), nullable=False)
    CreatedDate = db.Column(db.DateTime, nullable=False)


