# Writing Center Scheduler
# Fall 2016
# 
# Written by
# * Brandon Davis (davisba@cs.unc.edu)
#

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
from flask_login import logout_user
from flask_login import current_user

# import Mongo Exceptions
from mongoengine import MultipleObjectsReturned, DoesNotExist

# import local
from . import config
from . import models

# import moment
from flask_moment import Moment

login_manager = LoginManager()
moment = Moment()
schedule_app = Flask(__name__)
login_manager.init_app(schedule_app)
moment.init_app(schedule_app)


# configure the app
schedule_app.config["SECRET_KEY"] = config.SECRET_KEY
schedule_app.config["DEBUG"] = config.LOCAL
login_manager.login_view = "login"


def sanity_checks():
    # Check to make sure there is at least one administrative user.
    users = models.User.objects()
    locations = models.Location.objects()
    
    admins = any([user.is_admin for user in users])
    if not admins:
        new_admin = models.User()
        new_admin.init(
            first_name="Admin",
            last_name="Heel",
            pid=config.ADMIN_PID, # -1 should never happen
            email="scheduler_admin@unc.edu",
            typecode="100"
        )
        new_admin.save()
        print(" * Added admin user with PID " + str(config.ADMIN_PID))

    for user in users:

        if user.color == None:
            user.randomizeColor()
            print(" * Colorized user with PID " + str(user.pid))

        if user.desired_hours == None:
            user.desired_hours = config.DEFAULT_DESIRED_HOURS
        user.save()

    for loc in locations:
        pass

    print(" * Sanity checks complete! ")


@login_manager.user_loader
def load_user(pid):
    try:
        return models.User.objects.get(pid=pid)
    except MultipleObjectsReturned as e:
        print(str(pid) + " ---Primary Key Violated---")
        return None
    except DoesNotExist as e:
        print(str(pid) + " ---Does not exist---")
        return None


def user_from_sso(headers):
    """
    Given a header string, return the associated user.
    """
    pid = headers.get("Pid", default=None)
    onyen = headers.get("Uid", default=None)
    email = headers.get("Eppn", default=None)

    if pid and onyen and email:
        # update the user every time they log in with SSO
        # TODO: ask ITS for more information about the user
        user = load_user(pid)

        if user:
            user.email = email
            user.save()
        return user
    else:
        return None

def get_shib_cookie(cookies):
    for c in cookies:
        if c.startswith("_shib"):
            return c
    return None


def load_location(code):
    try:
        return models.Location.objects.get(code=code)
    except MultipleObjectsReturned as e:
        return None
    except DoesNotExist as e:
        return None

def time_to_index(timestring):
    try:
        hour_min = timestring.split(':')
        hour = int(hour_min[0]) * 2
        hour = hour + 1 if hour_min[1] == "30" else hour
        return hour
    except IndexError:
        return 0

@schedule_app.route("/login", methods=['GET'])
def login():

    user = None

    if config.LOCAL:
        print("---LOCAL DEV---")
        user = load_user(config.ADMIN_PID)
    else:
        user = user_from_sso(request.headers)

    if user:
        # The user exists and was in the database.
        login_user(user)
        nxt = request.args.get('next')
        return redirect(nxt or flask.url_for('index'))
    else:
        # The user did not exist or was not in the database.
        return redirect(url_for("login_failed"))


@schedule_app.route("/login_failed")
def login_failed():
    return "Login Failed.  Please contact the system manager."

@schedule_app.route("/logout")
@login_required
def logout():
    logout_user()
    cookie_name = get_shib_cookie(request.cookies)

    resp = redirect(config.SSO_LOGOUT_URL)

    if cookie_name:
        resp.set_cookie(cookie_name, expires=0)

    return resp


@schedule_app.route("/")
@login_required
def index():
    """
    Dump the headers
    """
    if current_user.is_admin:
        return redirect(url_for("admin"))
    else:
        return redirect(url_for("set_availability", pid=current_user.pid))


# Import app views
from .views import user_views
from .views import location_views
from .views import schedule_views
from .views import config_views
