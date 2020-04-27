from . import db


class HistoryView(db.Model):
    __bind_key__ = 'readonly'
    __tablename__ = 'CV$IF_MEM_EMP_HIS'

    CLNT = db.Column(db.String(255), primary_key=True, Nullable=False)
    MKEY = db.Column(db.String(255), primary_key=True, Nullable=False)
    ERKEY = db.Column(db.String(255), primary_key=True, Nullable=False)
    EMPLOYER_SNAME = db.Column(db.String(255), primary_key=True, Nullable=False)
    EDATE = db.Column(db.DateTime, primary_key=True, Nullable=False)
    EMP_STATUS = db.Column(db.String(255), primary_key=True, Nullable=False)
