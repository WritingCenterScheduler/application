import json

from flask import jsonify
from flask import Response
from flask import request
from flask import render_template
from flask_login import current_user

from app import schedule_app
from app import load_user

# import Mongo Exceptions
from mongoengine import MultipleObjectsReturned, DoesNotExist, NotUniqueError

from .. import models
from .. import responses

#
# API views
#

@schedule_app.route("/api/user", methods=["POST"])
def add_user():
    """
    Create a new user with details specified in request body
    """
    try:
        print(request.data)
        data = json.loads(request.data.decode("utf-8"))
    
    except Exception as e:
        return responses.invalid(request.url, e)

    u = models.User()

    try:
        u.init(
            pid=data['pid'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            onyen=data['onyen'],
            typecode=data['typecode'])
        u.save()
    except KeyError as e:
        return responses.invalid(request.url, e)
    except NotUniqueError as e:
        return responses.invalid(request.url, "User already exists")

    return responses.user_created(request.url, data['pid'])

@schedule_app.route("/api/user/<path:pid>", methods=["GET"])
def user(pid):
    """
    Get or update the user specified by PID
    """
    user = load_user(pid)
    if user:
        return Response(user.to_json(), mimetype='application/json')
    else:
        return responses.invalid(request.url, "User does not exist")

@schedule_app.route("/api/users", methods=["GET"])
def users():
    """
    Get all users in the system
    """
    users = models.User.objects()
    return Response(users.to_json(), mimetype='application/json')

#
# UI Views
#

@schedule_app.route("/user/<pid>/settings/availability")
def set_availability(pid):
    """
    View for a user to set their own availability
    Method:
        1) Generate the UI
        2) POST the updates to /api/user/<id>
    """
    user = load_user(pid)
    if user:
        return render_template("user_availability.html",
            user=user)
    else: 
        return responses.invalid(request.url, "User does not exist")