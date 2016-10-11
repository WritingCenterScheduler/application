import json
# necessary flask libraries
from flask import jsonify, Response, request
from flask_login import login_required, current_user
# load from init
from app import schedule_app, load_user, load_location
# import Mongo Exceptions
from mongoengine import MultipleObjectsReturned, DoesNotExist, NotUniqueError
# import local libraries
from .. import models, responses, decorators

#
# API Views
#

@schedule_app.route("/api/location/<path:code>", methods=['GET', 'PUT'])
@login_required
@decorators.requires_admin
def location(code):
    """
    GET - Get the location corresponded to by code
    PUT - Update the location with the data in the payload
    """
    loc = load_location(code)
    if loc:
        return Response(loc.to_json(), mimetype='application/json')
    else:
        return responses.invalid(request.url, "Location does not exist")

@schedule_app.route("/api/locations", methods=['GET', 'POST'])
@login_required
@decorators.requires_admin
def locations():
    """
    GET - Return a JSON list of all locations in the system
    POST - Create a new location 
    """
    locs = models.Location.objects()
    return Response(locs.to_json(), mimetype='application/json')