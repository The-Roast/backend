from flask import Flask
from flask_cors import CORS
from .db.schemas import *
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

    db.init_app(app)
    migrate.init_app(app, db)
