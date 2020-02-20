import os
import jwt
import json
import xlrd
import shutil
import threading
import zipfile
from datetime import datetime
from flask import Blueprint, jsonify, request, send_file, current_app as app
from flask_restplus import Resource, reqparse, fields
from werkzeug.utils import secure_filename
from xlutils.copy import copy
from werkzeug.exceptions import Unauthorized, BadRequest, UnprocessableEntity, InternalServerError
from ... import APP
from ...helpers import token_verify, delete_excel, token_verify_or_raise, crossdomain
from ...models import db, roles
from ...models.settings import Settings
from . import ns

parser = reqparse.RequestParser()
parser.add_argument('Authorization', type=str, location='headers', required=True)
parser.add_argument('username', type=str, location='headers', required=True)
parser.add_argument('Ipaddress', type=str, location='headers', required=True)

response_model = {
    "NotificationEmail": fields.String,
    "ArchiveDays": fields.String,
    "ReviewIP": fields.String,
    "RMIP": fields.String,
    "LastRun": fields.String,
    "Sync": fields.String
}


@ns.route("/settings/get")
class GetSettings(Resource):
    @crossdomain(whitelist=APP.config['CORS_ORIGIN_WHITELIST'], headers=APP.config['CORS_HEADERS'])
    def options(self):
        pass

    @crossdomain(whitelist=APP.config['CORS_ORIGIN_WHITELIST'], headers=APP.config['CORS_HEADERS'])
    @ns.doc(parser=parser,
            description='Add settings',
            responses={200: 'OK', 400: 'Bad Request', 401: 'Unauthorized', 500: 'Internal Server Error'})
    @ns.expect(parser, validate=True)
    @ns.marshal_with(response_model)
    def get(self):
        args = parser.parse_args(strict=False)
        username = args['username']
        token = args["Authorization"]
        ip = args['Ipaddress']
        decoded_token = token_verify_or_raise(token, username, ip)
        if decoded_token["role"] == roles.ROLES_ADMIN:
            settings = Settings.query.order_by(Settings.SettingID.desc()).first()
            return {
                "NotificationEmail": settings.NotificationEmail,
                "ArchiveDays": settings.ArchiveDays,
                "ReviewIP": settings.ReviewIP,
                "RMIP": settings.RMIP,
                "LastRun": settings.LastRun,
                "Sync": settings.Sync
            }, 200
        else:
            raise Unauthorized()
