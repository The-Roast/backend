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

    configure_blueprints(app)
    configure_extensions(app)

    return app


def configure_extensions(app):

    db.init_app(app)
    migrate.init_app(app, db)
    lm.init_app(app)
    
    @lm.user_loader
    def load_user(id):
        return Users.query.filter_by(id = id)

def configure_blueprints(app):

    from theroast.api.v1.auth import auth

    app.register_blueprint(auth)