# import python native
import json

# import flask
from flask import Flask
from flask import jsonify
from flask import request
from flask import redirect
from flask import url_for

# import Login manager
from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_login import current_user

# import Mongo Exceptions
from mongoengine import MultipleObjectsReturned, DoesNotExist

# import local
from . import config
from . import models

login_manager = LoginManager()
schedule_app = Flask(__name__)
login_manager.init_app(schedule_app)

# configure the app
schedule_app.config["SECRET_KEY"] = config.SECRET_KEY
schedule_app.config["DEBUG"] = True
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(pid):
    try:
        return models.User.objects.get(pid=pid)
    except MultipleObjectsReturned as e:
        return None
    except DoesNotExist as e:
        return None


def user_from_sso(headers):
    """
    Given a header string, return the associated user.
    """
    print("----SSO---")
    pid = headers.get("Pid", default=None)
    onyen = headers.get("Uid", default=None)
    email = headers.get("Eppn", default=None)

    if pid and onyen and email:
        # return load_user(pid)
        return None
    else:
        return None


def load_location(code):
    try:
        return models.Location.objects.get(code=code)
    except MultipleObjectsReturned as e:
        return None
    except DoesNotExist as e:
        return None


@schedule_app.route("/login", methods=['GET'])
def login():
    print("----LOGIN-----")
    # print(request.headers)
    user = user_from_sso(request.headers)
    login_user(user)
    return redirect(url_for("index"))


@schedule_app.route("/")
@login_required
def index():
    """
    Dump the headers
    """
    return(str(request.headers))


# Import app views
from .views import user_views
from .views import location_views