# import python native
import json

# import flask
from flask import Flask
from flask import jsonify
from flask_login import LoginManager

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


@login_manager.user_loader
def load_user(pid):
    try:
        return models.User.objects.get(pid=pid)
    except MultipleObjectsReturned as e:
        return None
    except DoesNotExist as e:
        return None

@schedule_app.route("/")
def index():
    return "It works"

@schedule_app.route("/db/test")
def db_test():
    u = models.User()
    u.init(pid=6)
    u.save()
    return u.to_json()

# Import app views
from .api import user_views