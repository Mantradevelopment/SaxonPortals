from . import db


class Comments(db.Model):
    __bind_key__ = 'writeonly'

    CommentsID = db.Column(db.Integer, primary_key=True, nullable=False)
    FormID = db.Column(db.Integer)

    Role = db.Column(db.String(255))
    Comment = db.Column(db.String(255))
    Date = db.Column(db.String(255))
