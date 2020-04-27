from . import db


class HistoryView(db.Model):
    __bind_key__ = 'readonly'
    __tablename__ = 'CV$IF_MEM_EMP_HIS'

    CLNT = db.Column(db.String(255), primary_key=True)
    MKEY = db.Column(db.String(255), primary_key=True)
    ERKEY = db.Column(db.String(255), primary_key=True)
    EMPLOYER_SNAME = db.Column(db.String(255), primary_key=True)
    EDATE = db.Column(db.DateTime, primary_key=True)
    EMP_STATUS = db.Column(db.String(255), primary_key=True)
