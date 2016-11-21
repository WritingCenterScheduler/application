import json, string, random, datetime, pprint
import numpy as np
from flask import jsonify, Response, request, render_template, url_for
from flask_login import current_user, login_required
# import from init
from app import schedule_app, load_user, load_location
# import Mongo Exceptions
from mongoengine import MultipleObjectsReturned, DoesNotExist, NotUniqueError
# import local libraries
from .. import models, responses, decorators, config

from app.engine.scheduleManager import ScheduleManager
from app.engine.user import User
from app.engine.employee import Employee
from app.engine.location import Location

@schedule_app.route("/api/schedules", methods=["GET", "DELETE"])
@login_required
@decorators.requires_admin
def view_schedules():
    """
    Returns a view with all currently known schedules.
    """
    all_schedules = models.Schedule.objects()
    return Response(all_schedules.to_json(), mimetype='application/json')

@schedule_app.route("/api/schedule/<path:code>", methods=["GET", "DELETE"])
@login_required
@decorators.requires_admin
def schedule(code):
    """
    Displays the schedule referred to by SID.
    """
    s = models.Schedule.objects().get(sid=str(code))
    if s:
        if request.method == "DELETE":
            s.delete()
            return responses.success(request.url, "Schedule DELETED")

        elif request.method == "GET":
            return render_template("schedule_display.html",
                user=current_user,
                users = models.User.objects())

        else:
            return responses.invalid(url_for("schedule", code=code), "METHOD not supported.")

    else:
        return responses.invalid(url_for("schedule", code=code), "Schedule ID not found")

def index2time(i):
    """
    Helper function for converting matrix index to readable military (24-hour) time.
    """
    if ((i * 30) % 60) == 0:
        return (str(int((i*30)/60)) + ":" + str((i * 30) % 60) + "0")
    return (str(int((i*30)/60)) + ":" + str((i * 30) % 60))

@schedule_app.route("/api/schedule/<path:code>/data", methods=["GET"])
@login_required
@decorators.requires_admin
def schedule_data(code):
    """
    Modifies the schedule referred to by SID
    """
    # TODO: Give users/locations a unique color

    s = models.Schedule.objects().get(sid=code)
    if s:
        events = []
        id_counter = 1
        if request.method == "GET":
            schedule_data = json.loads(s.to_json())
            # print (schedule_data['data'])
            for d in schedule_data['data']:
                for day, timeslots in d["schedule"].items():
                    for i in range(len(timeslots)):
                        for pid in timeslots[i]:
                            if pid != None:
                                u = load_user(pid)
                                l = load_location(d['code'])
                                if u and l:
                                    events.append(
                                        {
                                            '_id':id_counter,
                                            'title': str(u.first_name + " " + u.last_name),
                                            'pid': pid,
                                            'location': str(l.name),
                                            'start': index2time(i),
                                            'end': index2time(i+1),
                                            'dow': [{"sun":0,"mon":1,"tue":2,"wed":3,"thu":4,"fri":5,"sat":6}[day]],
                                            'textColor' : '#000000'
                                        }
                                    )
                                    id_counter += 1

            return Response(json.dumps(events), mimetype='application/json')

        else:
            return responses.invalid(url_for("schedule", code=code), "METHOD not supported.")
    else:
        return responses.invalid(url_for("schedule", code=code), "Schedule ID not found")

@schedule_app.route("/admin/runschedule", methods=["GET"])
@login_required
@decorators.requires_admin
def engine_run():
    """
    Runs engine for the objects in the db
    """

    all_users = models.User.objects()

    # Get all schedulable users in a list
    schedulable_users = []

    for user in all_users:

        np_arr = user.to_np_arr()

        if np_arr is not None:
            candidate = Employee(np_arr,
                typecode="010",
                pid=user.pid)
            schedulable_users.append(candidate)

    # get all locations that require scheduling
    sm = ScheduleManager()

    # iterate over the locations
    all_locations = models.Location.objects()

    for loc in all_locations:
        l = Location(
            typecode=1,
            scalarWeight=2,
            requirements=loc.to_np_arr())
        l.name = loc.code
        sm.add_location(l)

    for candidate in schedulable_users:
        sm.add_candidate(candidate)

    sm.run_schedule()

    loc_return_list = []

    for s in sm.locations:
        loc_return_list.append({
            "schedule": models.global_np_to_json_dict(s.schedule.astype(int)),
            "code": s.name
        })

    # TODO: Store the schedule as an object
    new_schedule = models.Schedule()
    new_schedule.created_on = datetime.datetime.utcnow()
    new_schedule.data = loc_return_list
    new_schedule.sid = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(4))
    new_schedule.save()

    return jsonify(loc_return_list)
