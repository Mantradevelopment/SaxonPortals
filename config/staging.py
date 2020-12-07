import os
import logging


LOG_LEVEL = logging.DEBUG

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

DBAAS_READONLY_CONNECTION_STRING = "oracle+cx_oracle://SAXON_PORTAL:SAxon0123$$$@10.147.0.2:1521/?service_name=dtq.app.saxon.oraclevcn.com"
DBAAS_WRITEONLY_CONNECTION_STRING = "oracle+cx_oracle://system:BL_H#iP3EzA9Nx#m@portal-db-test.app.primary.oraclevcn.com:1521/?service_name=test.app.primary.oraclevcn.com"

SERVER_ADDRESS = "0.0.0.0"
SERVER_PORT = 90
SERVER_WEB_URL = 'https://portal.silverthatch.org.ky/'
FRONTEND_URL = 'http://portal-uat.silverthatch.org.ky/'
MAIL_ENROLLMENT_URL = 'https://silverthatch.org.ky/guides-handbooks/'

CELERY_BROKER_URL = 'filesystem://'
CELERY_BROKER_FOLDER = os.path.join(DATA_DIR, 'broker')

SECRET_KEY = 'f^I7q!(S(O]|"]%<+,Hz&vyQ^"exx9'
JWT_SECRET = 'H7|=1fq[:`.;MtY02Me]w9_XPRqt^S'

CORS_HEADERS = [
    'Ipaddress', 'Authorization', 'username',
    'Content-Type'
]

CORS_ORIGIN_WHITELIST = [
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
    "https://portal.silverthatch.org.ky",
    "http://portal-uat.silverthatch.org.ky",
    "https://portal-uat.silverthatch.org.ky"
]

MAILSERVER = 'GMAIL'
MAILSERVER_DOMAIN = 'smtp.gmail.com'
MAILSERVER_PORT = 465
MAILSERVER_USERNAME = 'SaxonPensions@gmail.com'
# Remove "-" in the password for the email to work
MAILSERVER_PASSWORD = 'gaxfalasmyoohlwb-'

BACKUP_MAILSERVER = 'GMAIL'
BACKUP_MAILSERVER_DOMAIN = 'smtp.gmail.com'
BACKUP_MAILSERVER_PORT = 465
BACKUP_MAILSERVER_USERNAME = 'SaxonPensions@gmail.com'
BACKUP_MAILSERVER_PASSWORD = 'gaxfalasmyoohlwb'