import jwt
import json
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Blueprint, jsonify, request, abort
from flask_cors import cross_origin
from flask_restplus import Resource, reqparse
from werkzeug.exceptions import NotFound, BadRequest, Unauthorized
from ...helpers import randomStringwithDigitsAndSymbols, token_verify
from ...encryption import Encryption
from ...models import db
from ...models.users import Users
from ...models.security_question import SecurityQuestion
from . import ns


getParser = reqparse.RequestParser()
getParser.add_argument('Username', type=str, location='json', required=True)

postParser = reqparse.RequestParser()
postParser.add_argument('SecurityQuestionID', type=int, location='json', required=True)
postParser.add_argument('SecurityAnswer', type=str, location='json', required=True)
postParser.add_argument('Authorization', type=str, location='headers', required=True)
postParser.add_argument('IpAddress', type=str, location='headers', required=True)
postParser.add_argument('Username', type=str, location='headers', required=True)

@ns.route("/security-question")
class SecurityQuestion(Resource):
    @ns.doc(parser=getParser,
        description='Get security question of a user',
        responses={
            200: 'OK',
            400: 'Bad Request',
            401: 'Unauthorized',
            404: 'Not Found',
            500: 'Internal Server Error'})

    @ns.expect(getParser)
    def get(self):
        args = getParser.parse_args(strict=True)

        user = Users.query.get(args['Username'])
        if user is None:
            raise NotFound('User not found')

        question = user.SecurityQuestion.Question
        return {
            "Question": question,
            "Email": user.Email
        }, 200



    @ns.doc(parser=postParser,
        description='Set Security Question',
        responses={200: 'OK', 400: 'Bad Request', 401: 'Unauthorized', 500: 'Internal Server Error'})

    @ns.expect(postParser, validate=True)
    def post(self):
        args = postParser.parse_args(strict=False)
        token = args["Authorization"]
        if not token_verify(token=token, ip=args["IpAddress"], user=args["Username"]):
            raise Unauthorized()

        user = Users.query.get(args["Username"])
        if not user:
            raise NotFound()

        user.SecurityQuestionID = args["SecurityQuestionID"]
        user.SecurityAnswer = Encryption().encrypt(args["SecurityAnswer"])
        try:
            db.session.commit()
            return { "result": "success" }

        except KeyError as e:
            print(str(e))
            raise BadRequest
        except jwt.DecodeError:
            raise Unauthorized
        except jwt.ExpiredSignatureError:
            raise Unauthorized('Please refresh the token')