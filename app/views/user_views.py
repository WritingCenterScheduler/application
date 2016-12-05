# Writing Center Scheduler
# Fall 2016
# 
# Written by
# * Brandon Davis (davisba@cs.unc.edu)
# * Ryan Court (ryco@cs.unc.edu)

import json
from copy import deepcopy
import numpy as np
import csv
# import flask
from flask import jsonify, Response, request, render_template, url_for
from flask_login import current_user, login_required
# import from init
from app import schedule_app, load_user
# import Mongo Exceptions
from mongoengine import MultipleObjectsReturned, DoesNotExist, NotUniqueError, ValidationError
# import local libraries
from .. import models, responses, decorators

#
# API views
#

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
            email=data['email'],
            typecode=data['typecode'])
        u.save()
    except KeyError as e:
        return responses.invalid(request.url, e)
    except NotUniqueError as e:
        return responses.invalid(request.url, "User already exists")

    return responses.user_created(request.url, data['pid'])

@schedule_app.route("/api/user/<path:pid>", methods=["GET", "PUT", "DELETE"])
@login_required
def user(pid):
    """
    GET - gets the user with pid
    PUT - updates the user with pid
    DELETE - removes the user with pid
    """
    user = load_user(pid)
    print(current_user.pid)
    print(current_user.pid == pid)

    if user:

        if request.method == "DELETE" and current_user.is_admin:
            user.delete()
            return responses.success(url_for("user", pid=pid), "USER DELETED")

        elif request.method == "PUT" \
            and ( current_user.is_admin or current_user.pid == int(pid) ):

            # Allow user updates
            payload = None

            try:
                payload = json.loads(request.data.decode("utf-8"))
            except Exception as e:
                return responses.invalid(request.url, e)

            if not current_user.is_admin:
                keys = deepcopy(list(payload.keys()))
                for key in keys:
                    if key not in user.updatable_fields:
                        payload.pop(key)


            if payload:
                success = user.update(payload);
                if success:
                    return responses.user_updated(request.url, user.pid)
                else:
                    return responses.invalid(request.url, "Could not update user")
            else:
                return responses.invalid(request.url, "No data")

        elif request.method == "GET":
            return Response(user.to_json(), mimetype='application/json')

        else:
            responses.invalid(request.url, "Method not supported")
    else:
        return responses.invalid(request.url, "User does not exist")


@schedule_app.route("/api/user/bulkcreate", methods=["POST"])
@login_required
@decorators.requires_admin
def csv_create():
    csv_data = request.data.decode("utf-8")

    reader = csv.reader(csv_data.split('\n'),
        skipinitialspace=True,
        delimiter=',',
        quotechar='"')

    for row in reader:
        try:
            # first, last, pid, email, is_returner

            u = models.User()
            typecode = "0" + row[4] + "0"
            u.init(
                first_name=row[0],
                last_name=row[1],
                pid=row[2],
                email=row[3],
                typecode=typecode)
            u.save()

        except ValidationError:
            return responses.invalid(request.url, "Data failed to validate")
        except NotUniqueError:
            return responses.invalid(request.url, "Duplicates detected")
        except:
            return responses.invalid(request.url, "Bad CSV Payload")

    return responses.success(request.url, "BULK CREATE DONE")


def users():
    """
    GET - get all users in the system
    """
    users = models.User.objects().order_by("typecode", "last_name")
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

    TODO: Found bug.  Admin can see all users.
    """
    user = load_user(pid)
    if user:
        return render_template("user_availability.html",
            user=user,
            active_schedule = models.GlobalConfig.get().active_schedule)
    else:
        return responses.invalid(request.url, "User does not exist")

@schedule_app.route("/user/<pid>/schedule")
@login_required
def user_schedule(pid):
    user = load_user(pid)
    if user:
        return render_template("user_schedule.html",
            user=user,
            active_schedule = models.GlobalConfig.get().active_schedule)
    else:
        return responses.invalid(request.url, "User does not exist")
    pass

@schedule_app.route("/admin")
@login_required
@decorators.requires_admin
def admin():
    return render_template("admin.html",
        user=current_user,
        all_users = models.User.objects(),
        all_schedules = models.Schedule.objects(),
        active_schedule = models.GlobalConfig.get().active_schedule)

@schedule_app.route("/user/help")
@login_required
def help():
    """
    View for a user to set their own availability
    Method:
        1) Generate the UI
        2) POST the updates to /api/user/<id>

    TODO: Found bug.  Admin can see all users.
    """

    return render_template("user_help.html",
            user=user,
            active_schedule = models.GlobalConfig.get().active_schedule)
#<<<<<<< HEAD
#    return render_template("user_help.html",
#            user=user)
@schedule_app.route("/admin/help")
@login_required
def adminhelp():
    """
    View for a user to set their own availability
    Method:
        1) Generate the UI
        2) POST the updates to /api/user/<id>

    TODO: Found bug.  Admin can see all users.
    """
    return render_template("admin_help.html",
            user=user)
#=======
