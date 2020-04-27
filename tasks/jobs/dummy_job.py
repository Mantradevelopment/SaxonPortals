from portal import LOG
from tasks.worker import app


@app.task(name='dummy_job')
def dummy_job():
    LOG.debug("job:dummy_job:Yo, I am still alive.")

