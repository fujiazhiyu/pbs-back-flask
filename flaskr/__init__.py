import os
from flask import Flask
# from werkzeug.contrib.fixers import ProxyFix
from flask_cors import CORS


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        JSON_AS_ASCII=False
    )
    # app.wsgi_app = ProxyFix(app.wsgi_app)
    CORS(app, support_credentials=True)

    with app.app_context():
        from flaskr.db import db
        from flaskr import router
        db.init_app(app)
        app.register_blueprint(router.datasets)
        app.register_blueprint(router.areas)
        app.register_blueprint(router.infos)
        app.register_blueprint(router.keywords)
        app.register_blueprint(router.time)
        app.register_blueprint(router.messages)
        app.register_blueprint(router.paths)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
