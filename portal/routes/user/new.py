import jwt
import json
import smtplib
from datetime import datetime
from flask import Blueprint, jsonify, request, abort, current_app as app
from flask_restx import Resource, reqparse, cors, fields

from ...helpers import randomStringwithDigitsAndSymbols, token_verify
from ...encryption import Encryption
from ...models import db
from ...models.users import Users
from ...models.security_question import SecurityQuestion
from . import ns
from ... import APP, LOG
from ...services.mail import send_email

parser = reqparse.RequestParser()
parser.add_argument('Authorization', type=str, location='headers', required=True)
parser.add_argument('username', type=str, location='headers', required=True)
parser.add_argument('Ipaddress', type=str, location='headers', required=True)


response_model = ns.model('PostUserNew', {
    'result': fields.String,
    'error': fields.String,
})

@ns.route("/new")
class UserNew(Resource):
    @ns.doc(description='Create New User',
        responses={200: 'OK', 400: 'Bad Request', 401: 'Unauthorized', 500: 'Internal Server Error'})

    @ns.doc(description='Create New User',
            responses={200: 'OK', 400: 'Bad Request', 401: 'Unauthorized', 500: 'Internal Server Error'})
    @ns.expect(parser, validate=True)
    @ns.marshal_with(response_model)
    def post(self):
        try:
            if "Authorization" in request.headers.keys() and token_verify(token=request.headers["Authorization"],
                                                                          ip=request.headers["Ipaddress"],
                                                                          user=request.headers["User"]):
                auth = request.headers["Authorization"]
                auth1 = jwt.decode(auth, key=app.config['JWT_SECRET'])
                if auth1["role"] == "Admin" and token_verify(token=request.headers["Authorization"],
                                                             ip=request.headers["Ipaddress"],
                                                             user=request.headers["User"]):
                    data = json.loads(str(request.data, encoding='utf-8'))
                    username = data["username"]
                    displayname = data["DisplayName"]
                    email = data["Email"]
                    session_duration = data["SessionDuration"]
                    password = randomStringwithDigitsAndSymbols(10)
                    enc_pass = Encryption().encrypt(password)
                    userexist = Users.query.filter_by(Username=username).first()
                    if userexist is None:
                        new_user = Users(Username=username,
                                         Email=email,
                                         Password=enc_pass,
                                         Role=data["role"],
                                         Status="ACTIVE",
                                         TemporaryPassword=True,
                                         DisplayName=displayname,
                                         SessionDuration=session_duration,
                                         UserCreatedTime=datetime.utcnow())
                        db.session.add(new_user)
                        db.session.commit()
                        msg_text = f'<p>Dear {displayname}</p>' + \
                                    f'<p>Your account is created please use this password {password} to log in</p>'

                        send_email(to_address=email, body=msg_text, subject="Welcome to Pension Management portal")
                        return jsonify({"result": "Success"}), 200
                    else:
                        return jsonify({"error": "Username already exists"}), 409
            else:
                return jsonify({"error": "Not Authorized"}), 401
        except jwt.DecodeError:
            return jsonify({"error": "Not Authorized"}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Not Authorized"}), 401
        except Exception as e:
            LOG.error(e)
            return jsonify({"error": "Not Authorized"}), 401
