import os
import logging


LOG_LEVEL = logging.WARNING

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

DBAAS_READONLY_CONNECTION_STRING = "sqlite:///../data/readonly.sqlite"
DBAAS_WRITEONLY_CONNECTION_STRING = "sqlite:///../data/writeonly.sqlite"

SERVER_ADDRESS = "0.0.0.0"
SERVER_PORT = 8080
SERVER_WEB_URL = f'http://{SERVER_ADDRESS}:{SERVER_PORT}/static/'

CELERY_BROKER_URL = 'filesystem://'
CELERY_BROKER_FOLDER = os.path.join(DATA_DIR, 'broker')

SECRET_KEY = 'z6lajn4@#vsedg'
JWT_SECRET = 'N23tn@#$G"__0a'

CORS_HEADERS = [
    'Ipaddress', 'Authorization', 'username',
    'Content-Type'
]

CORS_ORIGIN_WHITELIST = [
    "http://127.0.0.1",
    "https://127.0.0.1",
    "http://127.0.0.1:5000",
    "https://127.0.0.1:5000",
    "http://127.0.0.1:4200",
    "https://127.0.0.1:4200",
    "http://192.168.2.146:8080",
    "http://192.168.2.146:812",
    "http://localhost",
    "https://localhost",
    "http://localhost:5000",
    "https://localhost:5000",
    "http://localhost:4200",
    "https://localhost:4200",
    "http://192.168.2.132:812"
]

MAILSERVER = 'GMAIL'
MAILSERVER_DOMAIN = 'smtp.gmail.com'
MAILSERVER_PORT = 465
MAILSERVER_USERNAME = ''
MAILSERVER_PASSWORD = ''

BACKUP_MAILSERVER = 'GMAIL'
BACKUP_MAILSERVER_DOMAIN = 'smtp.gmail.com'
BACKUP_MAILSERVER_PORT = 465
BACKUP_MAILSERVER_USERNAME = ''
BACKUP_MAILSERVER_PASSWORD = ''