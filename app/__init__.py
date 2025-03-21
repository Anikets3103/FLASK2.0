from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# new line

from flask_login import LoginManager

login = LoginManager(app)
login.login_view = "login"

from app import routes,models

# Set-ExecutionPolicy Unrestricted -Scope Process
# venv\Scripts\activate
# venv\Scripts\Activate.ps1
