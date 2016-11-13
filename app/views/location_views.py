import json
# necessary flask libraries
from flask import jsonify, Response, request, redirect, url_for, render_template
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
def api_location(code):
    """
    GET - Get the location corresponded to by code
    PUT - Update the location with the data in the payload
    """
    loc = load_location(code)
    if loc:
        if request.method == "PUT":
            payload = None
            
            try:
                payload = json.loads(request.data.decode("utf-8"))
            except Exception as e:
                return responses.invalid(request.url, e)

            if payload:
                success = loc.update(payload);
                if success:
                    return responses.loc_updated(request.url, current_user.pid)
                else:
                    return responses.invalid(request.url, "Could not update location")
            else:
                return responses.invalid(request.url, "No data")
        else:
            return Response(loc.to_json(), mimetype='application/json')
    else:
        return responses.invalid(request.url, "Location does not exist")


@schedule_app.route("/api/locations", methods=['GET', 'POST'])
@login_required
@decorators.requires_admin
def api_locations():
    """
    GET - Return a JSON list of all locations in the system
    POST - Create a new location 
    """
    if request.method == "POST":
        # user is trying to create a new location...
        try:
            print(request.data)
            data = json.loads(request.data.decode("utf-8"))
        except Exception as e:
            return responses.invalid(request.url, e)
        
        l = models.Location()

        try:
            l.init(**data)
            l.save()
        except KeyError as e:
            return responses.invalid(request.url, e)
        except NotUniqueError as e:
            return responses.invalid(request.url, "Location already exists")

        return responses.loc_created(request.url, current_user.pid, l.code)
    
    else:
        # ELSE GET
        locs = models.Location.objects()
        return Response(locs.to_json(), mimetype='application/json')

#
# UI Views
#

@schedule_app.route("/admin/location/<loc_id>", methods=['GET'])
@login_required
@decorators.requires_admin
def location(loc_id):
    loc = load_location(loc_id)
    return render_template("location_settings.html",
            user=current_user,
            location=loc)


@schedule_app.route("/admin/location", methods=['GET'])
def location_default():
    locations = models.Location.objects()
    try:
        return redirect(url_for("location", loc_id=locations[0].code))
    except:
        return redirect(url_for("location", loc_id='0'))