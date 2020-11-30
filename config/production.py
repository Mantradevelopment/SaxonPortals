import os
import logging
from urllib.parse import quote_plus


LOG_LEVEL = logging.INFO

ROOT_DIR = os.path.abspath(os.path.join(os.path.abspath(__file__), '..', '..'))
DATA_DIR = os.path.join(ROOT_DIR, 'data')

LOG_DIR = os.path.join(DATA_DIR, 'log')
ZIP_DATA_DIR = os.path.join(DATA_DIR, 'zip')
EXCEL_TEMPLATE_DIR = os.path.join(DATA_DIR, 'excel')

DIRECTORIES = [
    'termination', 'Statements', 'rev_inbox', 'Resources', 'pensioninfo',
    'Monthly', 'member_resources', 'enrollment', 'Employers', 'emp_inbox',
    'contribution', 'batch', 'Annual',
]

DBAAS_READONLY_CONNECTION_STRING = "oracle+cx_oracle://SAXON_PORTAL:C_dsr7xXB3cEJ#HH@10.147.0.19:1521/?service_name=prod.app.saxon.oraclevcn.com"
DBAAS_WRITEONLY_CONNECTION_STRING = "oracle+cx_oracle://manomaysaxonapp:A93#pqj4MZ__23@SAXON2.PRD"


SERVER_ADDRESS = "0.0.0.0"
SERVER_PORT = 90
SERVER_WEB_URL = 'https://portal.silverthatch.org.ky/'
FRONTEND_URL = 'https://portal.silverthatch.org.ky/'
MAIL_ENROLLMENT_URL = 'https://silverthatch.org.ky/guides-handbooks/'

CELERY_BROKER_URL = 'filesystem://'
CELERY_BROKER_FOLDER = os.path.join(DATA_DIR, 'broker')

SECRET_KEY = 'zXP-H@x4AYjD%w4rRzZW7dVyur^Y$5'
JWT_SECRET = '8ERW&e=ay_fU@#G6VkQb2A+c2-sm3#'

CORS_HEADERS = [
    'Ipaddress', 'Authorization', 'username',
    'Content-Type'
]

CORS_ORIGIN_WHITELIST = [
    "http://editor.swagger.io",
    "https://editor.swagger.io",
    "http://generator.swagger.io",
    "https://generator.swagger.io",

    "http://127.0.0.1",
    "https://127.0.0.1",
    "http://127.0.0.1:5000",
    "https://127.0.0.1:5000",
    "http://127.0.0.1:4200",
    "https://127.0.0.1:4200",

    "http://localhost",
    "https://localhost",
    "http://localhost:5000",
    "https://localhost:5000",
    "http://localhost:4200",
    "https://localhost:4200",

    "http://10.147.1.101",
    "https://10.147.1.101",

    "http://10.147.1.101:4200",
    "https://10.147.1.101:4200",

    "http://132.145.107.163",
    "https://132.145.107.163",
    "http://192.168.2.146:8080",
    "http://192.168.2.146:812",
    "http://192.168.2.132:812",

    "http://portal.silverthatch.org.ky",
    "https://portal.silverthatch.org.ky"
]

MAILSERVER = 'OFFICE365'
MAILSERVER_DOMAIN = 'smtp.office365.com'
MAILSERVER_PORT = 587
MAILSERVER_USERNAME = 'support@silverthatch.org.ky'
MAILSERVER_PASSWORD = 'Tod73455'

BACKUP_MAILSERVER = 'GMAIL'
BACKUP_MAILSERVER_DOMAIN = 'smtp.gmail.com'
BACKUP_MAILSERVER_PORT = 465
BACKUP_MAILSERVER_USERNAME = 'SaxonPensions@gmail.com'
BACKUP_MAILSERVER_PASSWORD = 'SaxPen2017'