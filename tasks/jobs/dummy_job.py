from portal import LOG
from tasks.worker import app, flask_app


@app.task(name='dummy_job')
def dummy_job():
    LOG.info("A scheduled dummy background job was executed: %s", flask_app.config['FRONTEND_URL'])

