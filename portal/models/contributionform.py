from . import db


class Contributionform(db.Model):
    FormID = db.Column(db.Integer, primary_key=True, nullable=False)

    EmployerName = db.Column(db.String(255))
    StartDate = db.Column(db.String(255))
    EndDate = db.Column(db.String(255))
    Comments = db.Column(db.String(255))
    Status = db.Column(db.String(255))
    Date = db.Column(db.String(255))
    PendingFrom = db.Column(db.String(255))
    EmployerID = db.Column(db.String(255))
