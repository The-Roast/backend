from flask import Flask
from flask_cors import CORS
from theroast.db.schemas import *
from theroast.extensions import *
from flask_mail import Mail, Message

def create_app(testing = False):

    app = Flask("theroast")
    app.config.from_object("theroast.config")
    if testing:
        app.config["TESTING"] = True
    CORS(app)

    configure_blueprints(app)
    configure_extensions(app)
    app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'apikey'
    app.config['MAIL_PASSWORD'] = "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"
    return app


def configure_extensions(app):

    db.init_app(app)
    migrate.init_app(app, db)

def configure_blueprints(app):

    from theroast.api.v1.auth import auth
    from theroast.api.v1.core import core

    app.register_blueprint(auth)
    app.register_blueprint(core)