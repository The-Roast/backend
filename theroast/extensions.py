from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


sql = SQLAlchemy()
migrate = Migrate()
lm = LoginManager()
