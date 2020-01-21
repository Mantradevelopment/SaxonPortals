from . import db


class Terminationform(db.Model):
    __bind_key__ = 'writeonly'

    TerminationID = db.Column(db.Integer, primary_key=True, nullable=False)

    Employername = db.Column(db.String(255))
    Date = db.Column(db.DateTime)
    MemberName = db.Column(db.String(255))
    Employernumber = db.Column(db.String(255))
    Email = db.Column(db.String(255))
    Finaldateofemployment = db.Column(db.DateTime)
    ReasonforTermination = db.Column(db.String(255))
    LastDeduction = db.Column(db.String(255))
    Address = db.Column(db.String(255))
    AddressLine2 = db.Column(db.String(255))
    District = db.Column(db.String(255))
    Postalcode = db.Column(db.String(255))
    Country = db.Column(db.String(255))
    Incomerange = db.Column(db.String(255))
    Status = db.Column(db.String(255))
    EmployerID = db.Column(db.String(255))
    PendingFrom = db.Column(db.String(255))


#  {'address': '503, Cherry Street Apartment',
#   'addressLine2': '118',
#   'comments': 'term',
#   'country': 'AF',
#   'district': 'k',
#   'email': 'helloo@gmail.com',
#   'employername': 'Saxon Pensions',
#   'employernumber': 'saxon',
#   'finalDateofEmployement': DatetimeWithNanoseconds(2019, 12, 5, 18, 30, tzinfo=<UTC>),
#   'formCreatedDate': DatetimeWithNanoseconds(2019, 12, 6, 8, 4, 22, 565843, tzinfo=<UTC>),
#   'formType': 'termination',
#   'incomerange': '20',
#   'lastDeductionPeriod': DatetimeWithNanoseconds(2019, 12, 5, 18, 30, tzinfo=<UTC>),
#   'member_id': '28634',
#   'memberfirstName': 'Member124',
#   'pendingFrom': 'member',
#   'phoneNumber': '9866989999',
#   'postalcode': '77844',
#   'reasonForTermination': 'Left Employment',
#   'status': 'pending'},
