from flask import Flask
from flask_cors import CORS
from theroast.db.schemas import *
from theroast.extensions import *

def create_app(testing = False):

    app = Flask("theroast")
    app.config.from_object("theroast.config")
    if testing:
        app.config["TESTING"] = True
    CORS(app)

    configure_blueprints(app)
    configure_extensions(app)
    return app


def configure_extensions(app):

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

def configure_blueprints(app):

    from theroast.api.v1.auth import auth
    from theroast.api.v1.core import core

    app.register_blueprint(auth)
    app.register_blueprint(core)