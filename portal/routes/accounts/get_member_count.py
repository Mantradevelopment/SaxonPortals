import jwt
import json
from datetime import datetime
from flask import Blueprint, jsonify, request, abort, current_app as app
from flask_restx import Resource, reqparse, fields
from sqlalchemy import or_

from ...helpers import randomStringwithDigitsAndSymbols, token_verify, token_verify_or_raise
from ...encryption import Encryption
from ...models import db, status, roles
from ...models.employer_view import EmployerView
from ...models.member_view import MemberView
from werkzeug.exceptions import Unauthorized, BadRequest, UnprocessableEntity, InternalServerError
from . import ns
from ... import APP, LOG
from ...models.history_view import HistoryView

parser = reqparse.RequestParser()
parser.add_argument('Authorization', type=str, location='headers', required=True)
parser.add_argument('username', type=str, location='headers', required=True)
parser.add_argument('Ipaddress', type=str, location='headers', required=True)

response_model = ns.model('GetGetMembers', {
    "members": fields.Integer
})


@ns.route("/members/count/get/<EmployerID>")
class GetMembersForEmployer(Resource):
    @ns.doc(description='Get all members in b/w min and max',
            responses={200: 'OK', 400: 'Bad Request', 401: 'Unauthorized', 500: 'Internal Server Error'})
    @ns.expect(parser, validate=True)
    @ns.marshal_with(response_model)
    def get(self, EmployerID):
        args = parser.parse_args(strict=False)
        username = args['username']
        token = args["Authorization"]
        ip = args['Ipaddress']
        decoded_token = token_verify_or_raise(token, username, ip)

        if decoded_token["role"] not in [roles.ROLES_EMPLOYER, roles.ROLES_HR, roles.ROLES_REVIEW_MANAGER]:
            raise Unauthorized()

        if EmployerID is None:
            raise UnprocessableEntity("Not a valid employerid")
        employer_ = EmployerView.query.filter(EmployerView.ERNO == EmployerID, or_(EmployerView.TERMDATE >= datetime.utcnow(), EmployerView.TERMDATE.is_(None))).first()
        if employer_ is None:
            raise UnprocessableEntity("Not a valid employerid")
        employer_sname = employer_.SNAME
        try:
            members_count = db.session.query(HistoryView, EmployerView, MemberView) \
                .filter(HistoryView.ERKEY == EmployerView.ERKEY, HistoryView.MKEY == MemberView.MKEY,
                        EmployerView.ERKEY == employer_.ERKEY,
                        HistoryView.EMP_STATUS != "Terminated",
                        MemberView.PSTATUS.ilike("%active%")).count()
            return {"members": members_count}, 200
        except Exception as e:
            LOG.error(e)
            raise InternalServerError("Can't get members")
