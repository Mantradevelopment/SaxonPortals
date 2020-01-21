import os
from flask import Flask
from gevent.pywsgi import WSGIServer


def create_app(config=None):
    from . import routes, models, services, helpers
    app = Flask(__name__)
    models.init_app(app)
    routes.init_app(app)
    services.init_app(app)
    helpers.init_cors(app)


    app.secret_key = 'random string'
    app.debug = True

    if config is not None:
        if isinstance(config, dict):
            app.config.update(config)
        elif config.endswith('.py'):
            app.config.from_pyfile(config)

    http_server = WSGIServer(('0.0.0.0', 811), app)
    http_server.serve_forever()
    return app

