
![Deploying Application](https://github.com/mousavian/backend-0/workflows/Deploying%20Application/badge.svg)


## How To Run

Create virtual environment:
```bash
virtualenv venv -p "$(which python3)"
source venv/bin/activate
```

Install required packages
```bash
pip install -r requirements.txt
```

For development:
```bash
# for Windows:
BACKEND_ENV=development FLASK_ENV=development  flask run

# for Unix:
BACKEND_ENV=dev-unix FLASK_ENV=development  flask run
```

http://127.0.0.1:5000/v1/health/status


## How to run background jobs

```
BACKEND_ENV=development FLASK_ENV=development celery worker --app=tasks.worker.app --concurrency=1 --loglevel=INFO -E -B
```
