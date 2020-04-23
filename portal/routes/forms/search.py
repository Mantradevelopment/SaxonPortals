import json
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request
from flask_restx import Resource, reqparse, inputs, fields
from sqlalchemy import or_, and_
from werkzeug.exceptions import NotFound, BadRequest, Unauthorized, UnprocessableEntity, InternalServerError
from ...helpers import token_verify_or_raise, RESPONSE_OK
from ...models import db, status, roles
from ...models.enrollmentform import Enrollmentform
from ...models.terminationform import Terminationform
from ...models.token import Token, TOKEN_FORMTYPE_TERMINATION, TOKEN_FORMTYPE_ENROLLMENT, TOKEN_FORMTYPE_CONTRIBUTION, \
    TOKEN_FORMTYPE_DOCUMENT
from ...models.contributionform import Contributionform
from ...models.documents import Documents
from ...models.comments import Comments
from ...models.roles import *
from ...services.mail import send_email
from . import ns
from ... import APP, LOG

parser = reqparse.RequestParser()
parser.add_argument('Authorization', type=str, location='headers', required=True)
parser.add_argument('username', type=str, location='headers', required=True)
parser.add_argument('Ipaddress', type=str, location='headers', required=True)
parser.add_argument('FormType', type=str, location='json', required=True)
parser.add_argument('Employer', type=str, location='json', required=False)
parser.add_argument('Member', type=str, location='json', required=False)
parser.add_argument('FormStatus', type=str, location='json', required=True)
parser.add_argument('PendingFrom', type=str, location='json', required=True)
parser.add_argument('SubmittedFrom', type=inputs.date_from_iso8601, location='json', required=False,
                    help='iso8601 format. eg: 2012-11-25')
parser.add_argument('SubmittedTo', type=inputs.date_from_iso8601, location='json', required=False,
                    help='iso8601 format. eg: 2012-11-25')

response_model_child = ns.model('PostSearchFormsChild', {
    "Token": fields.String,
    "FormID": fields.String,
    "EmployerID": fields.String,
    "MemberName": fields.String,
    "EmployerName": fields.String,
    "FormType": fields.String,
    "FormStatus": fields.String,
    "LastModifiedDate": fields.DateTime,
    "FileName": fields.String,
    "PendingFrom": fields.String,
    "EmailID": fields.String
})

response_model = ns.model('PostSearchForms', {
    "forms": fields.List(fields.Nested(response_model_child))
})


@ns.route("/search")
class SearchForms(Resource):
    @ns.doc(description='Get my forms',
            responses={200: 'OK', 400: 'Bad Request', 401: 'Unauthorized', 500: 'Internal Server Error'})
    @ns.expect(parser, validate=True)
    @ns.marshal_with(response_model)
    def post(self):
        args = parser.parse_args(strict=False)
        token = token_verify_or_raise(token=args["Authorization"], user=args["username"], ip=args["Ipaddress"])
        if token["role"] not in [ROLES_REVIEW_MANAGER, ROLES_EMPLOYER]:
            raise Unauthorized()
        forms_data = []
        parameters = ["FormType", "FormStatus", "Employer", "Member", "SubmittedFrom", "SubmittedTo", "PendingFrom",
                      "FormType"]
        parameters_dict = {}
        for arg in parameters:
            if args[arg] is None:
                parameters_dict[arg] = ""
            else:
                parameters_dict[arg] = args[arg]
        try:
            if parameters_dict["SubmittedFrom"] == "":
                parameters_dict["SubmittedFrom"] = datetime(year=1, month=1, day=1)
            if parameters_dict["SubmittedTo"] == "":
                parameters_dict["SubmittedTo"] = datetime(year=9999, month=1, day=1)
            form_status = parameters_dict["FormStatus"]
            submitted_from = parameters_dict["SubmittedFrom"]
            submitted_to = parameters_dict["SubmittedTo"]
            print("submittedfrom", submitted_from)
            print("parameters_dict", parameters_dict)
            if parameters_dict["FormType"] == TOKEN_FORMTYPE_TERMINATION or parameters_dict["FormType"] == "":
                print("Member Name", parameters_dict["Member"], "___End")
                termination_form_data = db.session.query(Token, Terminationform).filter(
                    Token.FormID == Terminationform.FormID,
                    Token.FormType == TOKEN_FORMTYPE_TERMINATION,
                    Token.TokenStatus == status.STATUS_ACTIVE,
                    or_(Token.EmployerID.ilike("%" + parameters_dict["Employer"] + "%"),
                        Terminationform.EmployerName.ilike("%" + parameters_dict["Employer"] + "%")),
                    Terminationform.MemberName.ilike("%" + parameters_dict["Member"] + "%"),
                    Terminationform.PendingFrom.ilike("%" + parameters_dict["PendingFrom"] + "%"),
                    Token.FormStatus.ilike("%" + form_status + "%"),
                    Token.FormStatus != status.STATUS_DELETE)
                if submitted_from == submitted_to:
                    termination_form_data = termination_form_data.filter(Token.InitiatedDate >= submitted_to,
                                                                         Token.InitiatedDate < submitted_to + timedelta(
                                                                             days=1))
                else:
                    termination_form_data = termination_form_data.filter(Token.InitiatedDate <= submitted_to,
                                                                         Token.InitiatedDate >= submitted_from)
                termination_form_data = termination_form_data.order_by(Token.LastModifiedDate.desc()).all()
                # print(termination_form_data)
                for tokens_data, terminations in termination_form_data:
                    print("termination Employer name", terminations.EmployerName)
                    forms_data.append({
                        "Token": tokens_data.TokenID,
                        "EmployerID": tokens_data.EmployerID,
                        "EmployerName": terminations.EmployerName,
                        "MemberName": terminations.MemberName,
                        "FormType": tokens_data.FormType,
                        "FormStatus": tokens_data.FormStatus,
                        "LastModifiedDate": tokens_data.LastModifiedDate,
                        "EmailID": terminations.EmailAddress,
                        "PendingFrom": tokens_data.PendingFrom
                    })
                    print("type(tokens_data.InitiatedDate)", type(tokens_data.InitiatedDate))
                # print(forms_data)
            if parameters_dict["FormType"] == TOKEN_FORMTYPE_ENROLLMENT or parameters_dict["FormType"] == "":
                name = parameters_dict["Member"]
                if " " in name:
                    firstname, lastname = name.split(" ")
                    print("firstname if", firstname, "--End")
                    print("lastname if", lastname, "--End")
                    if (lastname is None or lastname == ""):
                        lastname = firstname
                    if (firstname is None or firstname == ""):
                        firstname = lastname
                    enrollment_form_data = db.session.query(Token, Enrollmentform).filter(
                        Token.FormID == Enrollmentform.FormID,
                        Token.FormType == TOKEN_FORMTYPE_ENROLLMENT,
                        Enrollmentform.PendingFrom.ilike("%" + parameters_dict["PendingFrom"] + "%"),
                        and_(Enrollmentform.FirstName.ilike("%" + str(firstname) + "%"),
                             Enrollmentform.LastName.ilike("%" + str(lastname) + "%")),
                        or_(Token.EmployerID.ilike("%" + parameters_dict["Employer"] + "%"),
                            Enrollmentform.EmployerName.ilike("%" + parameters_dict["Employer"] + "%")),
                        Token.TokenStatus == status.STATUS_ACTIVE,
                        Token.FormStatus.ilike("%" + form_status + "%"),
                        Token.FormStatus != status.STATUS_DELETE
                    )
                else:
                    print("name else", name, "--End")
                    enrollment_form_data = db.session.query(Token, Enrollmentform).filter(
                        Token.FormID == Enrollmentform.FormID,
                        Token.FormType == TOKEN_FORMTYPE_ENROLLMENT,
                        Enrollmentform.PendingFrom.ilike("%" + parameters_dict["PendingFrom"] + "%"),
                        or_(Enrollmentform.FirstName.ilike("%" + str(name) + "%"),
                            Enrollmentform.LastName.ilike("%" + str(name) + "%")),
                        or_(Token.EmployerID.ilike("%" + parameters_dict["Employer"] + "%"),
                            Enrollmentform.EmployerName.ilike("%" + parameters_dict["Employer"] + "%")),
                        Token.TokenStatus == status.STATUS_ACTIVE,
                        Token.FormStatus.ilike("%" + form_status + "%"),
                        Token.FormStatus != status.STATUS_DELETE
                    )
                if submitted_from == submitted_to:
                    enrollment_form_data = enrollment_form_data.filter(Token.InitiatedDate >= submitted_to,
                                                                       Token.InitiatedDate < submitted_to + timedelta(
                                                                           days=1)
                                                                       )
                else:
                    enrollment_form_data = enrollment_form_data.filter(Token.InitiatedDate <= submitted_to,
                                                                       Token.InitiatedDate >= submitted_from)
                enrollment_form_data = enrollment_form_data.order_by(Token.LastModifiedDate.desc()).all()
                for tokens_data, enrollments in enrollment_form_data:
                    forms_data.append({
                        "Token": tokens_data.TokenID,
                        "EmployerID": tokens_data.EmployerID,
                        "EmployerName": enrollments.EmployerName,
                        "MemberName": str(
                            enrollments.FirstName if enrollments.FirstName is not None else "") + " " + str(
                            enrollments.LastName if enrollments.LastName is not None else ""),
                        "FormType": tokens_data.FormType,
                        "FormStatus": tokens_data.FormStatus,
                        "LastModifiedDate": tokens_data.LastModifiedDate,
                        "EmailID": enrollments.EmailAddress,
                        "PendingFrom": tokens_data.PendingFrom
                    })
            if token["role"] == ROLES_REVIEW_MANAGER and \
                    (parameters_dict["FormType"] == TOKEN_FORMTYPE_CONTRIBUTION or parameters_dict["FormType"] == "") \
                    and (parameters_dict["Member"] is None or parameters_dict["Member"] == ""):
                contribution_forms = Contributionform.query \
                    .filter(Contributionform.PendingFrom.ilike("%" + parameters_dict["PendingFrom"] + "%"),
                            Contributionform.Status.ilike("%" + form_status + "%"),
                            or_(Contributionform.EmployerID.ilike("%" + parameters_dict["Employer"] + "%"),
                                Contributionform.EmployerName.ilike("%" + parameters_dict["Employer"] + "%")),
                            Contributionform.Status != status.STATUS_DELETE)
                if submitted_from == submitted_to:
                    contribution_forms = contribution_forms.filter(Contributionform.Date >= submitted_to,
                                                                   Contributionform.Date < submitted_to + timedelta(
                                                                       days=1)
                                                                   )
                else:
                    contribution_forms = contribution_forms.filter(Contributionform.Date <= submitted_to,
                                                                   Contributionform.Date >= submitted_from)
                    contribution_forms = contribution_forms.order_by(Contributionform.LastModifiedDate.desc()).all()
                for contributions in contribution_forms:
                    forms_data.append({
                        "FormID": contributions.FormID,
                        "EmployerID": contributions.EmployerID,
                        "EmployerName": contributions.EmployerName,
                        "FormType": "Contribution",
                        "FormStatus": contributions.Status,
                        "PendingFrom": contributions.PendingFrom,
                        "LastModifiedDate": contributions.LastModifiedDate,
                        "FileName": str(contributions.FilePath).replace("/", "\\").split("\\")[
                            len(str(contributions.FilePath).replace("/", "\\").split(
                                "\\")) - 1] if contributions.FilePath is not None else ""
                    })

            if token["role"] == ROLES_REVIEW_MANAGER and \
                    (parameters_dict["FormType"] == TOKEN_FORMTYPE_DOCUMENT or parameters_dict[
                        "FormType"] == "") \
                    and (parameters_dict["Member"] is None or parameters_dict["Member"] == ""):
                documents = Documents.query \
                    .filter(Documents.PendingFrom.ilike("%" + parameters_dict["PendingFrom"] + "%"),
                            Documents.Status.ilike("%" + form_status + "%"),
                            or_(Documents.EmployerID.ilike("%" + parameters_dict["Employer"] + "%"),
                                Documents.EmployerName.ilike("%" + parameters_dict["Employer"] + "%")),
                            Documents.Status != status.STATUS_DELETE)
                if submitted_from == submitted_to:
                    documents = documents.filter(Documents.Date >= submitted_to,
                                                 Documents.Date < submitted_to + timedelta(
                                                     days=1)
                                                 )
                else:
                    documents = documents.filter(Documents.Date <= submitted_to,
                                                 Documents.Date >= submitted_from)
                    documents = documents.order_by(Documents.LastModifiedDate.desc()).all()

                for document in documents:
                    forms_data.append({
                        "FormID": document.FormID,
                        "EmployerID": document.EmployerID,
                        "EmployerName": document.EmployerName,
                        "FormType": "Document",
                        "FormStatus": document.Status,
                        "LastModifiedDate": document.LastModifiedDate,
                        "PendingFrom": document.PendingFrom,
                        "FileName": str(document.FilePath).replace("/", "\\").split("\\")[len(
                            str(document.FilePath).replace("/", "\\").split(
                                "\\")) - 1] if document.FilePath is not None else ""
                    })
                    print("form_data", forms_data)

            return {"forms": forms_data}, 200
        except Exception as e:
            LOG.error("Exception while adding employer to member", e)
            raise InternalServerError("Search failed")
