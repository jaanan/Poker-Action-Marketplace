from flask import Flask
app = Flask(__name__)



from flask_sqlalchemy import SQLAlchemy

import os

if os.environ.get('HEROKU'):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tournaments.db'
    app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


#login

from application.auth.models import User
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager, current_user
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please login to use this functionality"

# roles in login_required
from functools import wraps

def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user:
                return login_manager.unauthorized()

            if not current_user.is_authenticated:
                return login_manager.unauthorized()

            unauthorized = False

            if role != "ANY":
                unauthorized = True

                for user_role in current_user.role():
                    if user_role == role:
                        unauthorized = False
                        break

            if unauthorized:
                return login_manager.unauthorized()

            return fn(*args, **kwargs)

        return decorated_view

    return wrapper

from application import views

from application.auth import models
from application.auth import views

from application.tournamentPackages import models
from application.tournamentPackages import views

from application.auth.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

try:
    db.create_all()

    exists = User.query.filter_by(name = 'admin').first()

    if not exists:
        admin = User("admin", "admin", "admin")
        db.session().add(admin)
        db.session().commit()
except:
    pass