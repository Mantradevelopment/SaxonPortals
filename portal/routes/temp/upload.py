import os
from flask import request, send_file, render_template, Response
from flask_restx import Resource
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequest, InternalServerError
from . import ns
from ... import APP, LOG
from ...helpers import RESPONSE_OK



@ns.route("/upload")
class TempUpload(Resource):
    def get(self):
        data = render_template('emails/send_temporary_passwords/members.html',
        frontend_url=APP.config['FRONTEND_URL'],username="rahman",password=1232132)

        response = Response(data, mimetype='text/html')
        response.status_code = 200
        return response

    def post(self):
        file = request.files['file']
        filename = secure_filename(file.filename)
        path = os.path.join(APP.config['DATA_DIR'], 'tmp')

        if not os.path.exists(path):
            os.mkdir(path)

        try:
            file.save(os.path.join(path, filename))
        except Exception as e:
            LOG.error("===server err", e)
            raise InternalServerError("server error")

        return RESPONSE_OK
