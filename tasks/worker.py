import os
import time
from celery import Celery
from portal import create_app
from .helper import create_celery_app


flask_app = create_app()
app = create_celery_app(flask_app)
