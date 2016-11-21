import json
# import flask
from flask import jsonify, Response, request, render_template, url_for
from flask_login import current_user, login_required
# import from init
from app import schedule_app, load_user
# import Mongo Exceptions
from mongoengine import MultipleObjectsReturned, DoesNotExist, NotUniqueError
# import local libraries
from .. import models, responses, decorators, config

#
# API Views
#

@schedule_app.route("/api/config", methods=['GET', 'POST'])
@login_required
@decorators.requires_admin
def api_config():
    gc = models.GlobalConfig.get()

    if request.method == 'GET':
        return Response(gc.to_json())

    elif request.method == "POST":
        success = gc.update(request.data.decode("utf-8"))
        if success:
            return responses.success(request.url, "UPDATED Config")
        else:
            return responses.invalid(request.url, "Could not update config")