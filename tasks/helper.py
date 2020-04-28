import os
from celery.schedules import crontab
from celery import Celery


def create_celery_app(flask_app):
    broker_url = flask_app.config['CELERY_BROKER_URL']
    broker_dir = flask_app.config['CELERY_BROKER_FOLDER']

    app = Celery('portal-jobs')
    app.conf.update({
        'broker_url': broker_url,
        'broker_transport_options': {
            'data_folder_in': os.path.join(broker_dir, 'out'),
            'data_folder_out': os.path.join(broker_dir, 'out'),
            'data_folder_processed': os.path.join(broker_dir, 'processed')
        },
        'result_persistent': False,
        'task_serializer': 'json',
        'result_serializer': 'json',
        'accept_content': ['json'],
        'imports': (
            'tasks.jobs.dummy_job',
            'tasks.jobs.send_email',
            'tasks.jobs.send_form_reminder',
            'tasks.jobs.create_employer_accounts',
            'tasks.jobs.create_member_accounts',
            'tasks.jobs.send_temporary_passwords',
        ),
        'beat_schedule': {
            'dummy_job': {
                'task': 'dummy_job',
                # Once every hour
                'schedule': crontab(minute='0', hour='*', day_of_week='*', day_of_month='*', month_of_year='*'),
                # 'schedule': 5, # every second
            },
            'send_form_reminder': {
                'task': 'send_form_reminder',
                # At 04:00
                'schedule': crontab(minute='0', hour='4', day_of_week='*', day_of_month='*', month_of_year='*'),
            },
            'create_employer_accounts': {
                'task': 'create_employer_accounts',
                # At minute 0 past every 4th hour (00:00:00, 04:00:00, 08:00:00, ...)
                'schedule': crontab(minute='0', hour='*/4', day_of_week='*', day_of_month='*', month_of_year='*'),
            },
            'create_member_accounts': {
                'task': 'create_member_accounts',
                # At minute 30 past every 4th hour (00:30:00, 04:30:00, 08:30:00, ...)
                'schedule': crontab(minute='30', hour='*/4', day_of_week='*', day_of_month='*', month_of_year='*'),
            },
            'send_temporary_passwords': {
                'task': 'send_temporary_passwords',
                # At minute 30 past 8AM UTC (=3:30AM Cayman Time), every day  (00:59:00, 04:59:00, 08:59:00, ...)
                'schedule': crontab(minute='30', hour='8', day_of_week='*', day_of_month='*', month_of_year='*'),
            },
        },
    })

    TaskBase = app.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    app.Task = ContextTask
    return app
