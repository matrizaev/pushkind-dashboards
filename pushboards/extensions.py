from authlib.integrations.flask_client import OAuth
from dynaconf import FlaskDynaconf
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

oauth_client = OAuth()
login_manager = LoginManager()
migrate = Migrate()
db = SQLAlchemy()
bootstrap = Bootstrap5()
config = FlaskDynaconf()
