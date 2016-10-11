import json
# import flask
from flask import jsonify, Response, request, render_template
from flask_login import current_user, login_required
# import from init
from app import schedule_app, load_user
# import Mongo Exceptions
from mongoengine import MultipleObjectsReturned, DoesNotExist, NotUniqueError
# import local libraries
from .. import models, responses, decorators

#
# API views
#

@schedule_app.route("/api/user/me", methods=["GET", "PUT"])
@login_required
def me():
    """
    Allow any user to get or update itselfs
    ---
    GET - get myself
    PUT - update myself
    """
    if request.method == "GET":
        return Response(current_user.to_json(), mimetype='application/json')
    elif request.method == "PUT":
        # Allow the user to update itself
        return responses.not_implemented(request.url)
    else:
        return responses.bad_method(request.url, request.method)

@schedule_app.route("/api/user", methods=["POST"])
@login_required
@decorators.requires_admin
def add_user():
    """
    POST - Create a new user with details specified in the post data body
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

@schedule_app.route("/api/user/<path:pid>", methods=["GET", "PUT", "DELETE"])
@login_required
@decorators.requires_admin
def user(pid):
    """
    GET - gets the user with pid
    PUT - updates the user with pid
    DELETE - removes the user with pid
    """
    user = load_user(pid)
    if user:
        return Response(user.to_json(), mimetype='application/json')
    else:
        return responses.invalid(request.url, "User does not exist")

@schedule_app.route("/api/users", methods=["GET"])
@login_required
@decorators.requires_admin
def users():
    """
    GET - get all users in the system
    """
    users = models.User.objects()
    return Response(users.to_json(), mimetype='application/json')

#
# UI Views
#

@schedule_app.route("/user/<pid>/settings")
@login_required
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