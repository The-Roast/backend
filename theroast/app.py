from flask import Flask
from flask_cors import CORS
from .extensions import *

def create_app(testing = False):

    app = Flask("theroast")
    app.config.from_object("theroast.config")
    if testing:
        app.config["TESTING"] = True
    CORS(app)

    configure_extensions(app)

    return app


def configure_extensions(app):

    sql.init_app(app)
    migrate.init_app(app, sql)
