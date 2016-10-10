import json

from flask import jsonify
from flask import Response
from flask import request

from app import schedule_app
from app import load_user, load_location

# import Mongo Exceptions
from mongoengine import MultipleObjectsReturned, DoesNotExist, NotUniqueError

from .. import models
from .. import responses

#
# API Views
#

@schedule_app.route("/api/location/<path:code>", methods=['GET', 'PUT'])
def location(code):
    """
    Get the location corresponded to by code
    Update the location with the data in the payload
    """
    loc = load_location(code)
    if loc:
        return Response(loc.to_json(), mimetype='application/json')
    else:
        return responses.invalid(request.url, "Location does not exist")

@schedule_app.route("/api/locations", methods=['GET'])
def locations():
    """
    Return a JSON list of all locations in the system
    """
    locs = models.Location.objects()
    return Response(locs.to_json(), mimetype='application/json')