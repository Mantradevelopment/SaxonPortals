import jwt
import json
from datetime import datetime
from flask import Blueprint, jsonify, request, abort, current_app as app
from flask_restx import Resource, reqparse, fields
from ...helpers import randomStringwithDigitsAndSymbols, token_verify, token_verify_or_raise
from ...encryption import Encryption
from ...models import db, status, roles
from ...models.users import Users
from werkzeug.exceptions import Unauthorized, BadRequest, UnprocessableEntity, InternalServerError
from . import ns
from ... import APP, LOG

parser = reqparse.RequestParser()
parser.add_argument('Authorization', type=str, location='headers', required=True)
parser.add_argument('username', type=str, location='headers', required=True)
parser.add_argument('Ipaddress', type=str, location='headers', required=True)
parser.add_argument('language', type=str, location='json', required=True)
parser.add_argument('timezone', type=str, location='json', required=True)

post_response_model = ns.model('PostProfileDetails', {
    'result': fields.String,
})

@ns.route("/profile/update")
class UpdateProfileDetails(Resource):
    @ns.doc(description='Get profile details',
            responses={200: 'OK', 400: 'Bad Request', 401: 'Unauthorized', 500: 'Internal Server Error'})
    @ns.expect(parser, validate=True)
    @ns.marshal_with(post_response_model)
    def post(self):
        args = parser.parse_args(strict=False)
        username = args['username']
        token = args["Authorization"]
        ip = args['Ipaddress']
        language = args['language']
        timezone = args['timezone']
        decoded_token = token_verify_or_raise(token, username, ip)
        try:
            users = Users.query.filter_by(Username=username).first()

            users.Language = language
            users.Timezone = timezone
            db.session.commit()
            return {"result": "success"}, 200
        except Exception as e:
            LOG.error("Exception while updating profile details", e)
            raise InternalServerError("Can't update profile details")
