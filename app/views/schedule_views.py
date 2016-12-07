# Writing Center Scheduler
# Fall 2016
#
# Written by
# * Brandon Davis (davisba@cs.unc.edu)
# * Ryan Court (ryco@cs.unc.edu)

import json, string, random, datetime, pprint
import numpy as np
import math
from copy import deepcopy
from itertools import combinations, permutations
from flask import jsonify, Response, request, render_template, url_for
from flask_login import current_user, login_required
# import from init
from app import schedule_app, load_user, load_location, time_to_index
# import Mongo Exceptions
from mongoengine import MultipleObjectsReturned, DoesNotExist, NotUniqueError
# import local libraries
from .. import models, responses, decorators, config

from app.engine.scheduleManager import ScheduleManager
from app.engine.user import User
from app.engine.employee import Employee
from app.engine.location import Location

#
# API Views
#

def schedule_data_to_events(s):

    events = []
    userColors = dict()
    id_counter = 1

    schedule_data = json.loads(s.to_json())
    # print (schedule_data['data'])
    for d in schedule_data['data']:
        for day, timeslots in d["schedule"].items():
            for i in range(len(timeslots)):
                for pid in timeslots[i]:
                    if pid != None:
                        # if not pid in userColors:
                        #     userColors[pid] = HSVtoRGB(random.random(), 0.5, 0.95)
                        u = load_user(pid)
                        l = load_location(d['code'])
                        if u and l:
                            events.append(
                                {
                                    '_id':id_counter,
                                    'title': str(u.first_name + " " + u.last_name[0] + "."),
                                    'pid': pid,
                                    'location': str(l.name),
                                    'lcode': l.code,
                                    '_index': i,
                                    'start': index2time(i),
                                    'end': index2time(i+1),
                                    'dow': [{"sun":0,"mon":1,"tue":2,"wed":3,"thu":4,"fri":5,"sat":6}[day]],
                                    'textColor' : '#000000',
                                    'backgroundColor' : u.color
                                }
                            )
                            id_counter += 1
    return events

@schedule_app.route("/api/schedule/<code>/csv/<fname>", methods=["GET"])
@login_required
@decorators.requires_admin
def schedule_to_csv(code, fname):
    schedule = models.Schedule.objects().get(sid=str(code))

    if schedule == None:
        return responses.invalid(request.url, "No such schedule")

    events = schedule_data_to_events(schedule)

    locations = {}

    for item in events:
        if not item['location'] in locations.keys():
            locations[item['location']] = [ \
                [None for j in range(config.TIMESLOTS_PER_DAY)] \
                for i in range(7)]

    for item in events:
        start = time_to_index(item['start'])
        end = time_to_index(item['end'])
        for i in range(start, end):
            cell = locations[item['location']][item['dow'][0]][i]
            if cell:
                locations[item['location']][item['dow'][0]][i] = cell + " " + item['title']
            else:
                locations[item['location']][item['dow'][0]][i] = item['title']
    # Now build the CSV

    outstring = ""


    # return jsonify(locations)

    for loc in locations.keys():
        rows = ["" for i in range(config.TIMESLOTS_PER_DAY)]
        outstring += loc + "\r\n"
        for i in range(config.TIMESLOTS_PER_DAY):
                rows[i] +=  "\"" + str(math.floor(i/2)) + ":" + ("30" if i % 2 != 0 else "00") + "\","
        for col in locations[loc]:
            for dex, cell in enumerate(col):
                rows[dex] += "\"" + cell + "\"," if cell else ","
        rows = [row[:-1] for row in rows]
        outstring += "\r\n".join(rows)
        outstring += "\r\n"

    return Response(outstring, mimetype="text/csv")

@schedule_app.route("/api/schedule", methods=["POST"])
@login_required
@decorators.requires_admin
def new_schedule():
    """
    POST - Create a new schedule with details specified in the post data body
    """
    new_schedule_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(4))
    try:
        # print(request.data)
        data = json.loads(request.data.decode("utf-8"))
    except Exception as e:
        return responses.invalid(request.url, e)

    new_schedule = models.Schedule()
    try:
        new_schedule.init(
            created_on = datetime.datetime.utcnow(),
            data = data['data'],
            sid = new_schedule_id)
        new_schedule.save()
    except KeyError as e:
        return responses.invalid(request.url, e)
    except NotUniqueError as e:
        return responses.invalid(request.url, "Schedule ID already exists.")
    print(new_schedule_id)
    return responses.schedule_created(request.url, new_schedule_id)

@schedule_app.route("/api/schedules", methods=["GET", "DELETE"])
@login_required
@decorators.requires_admin
def view_schedules():
    """
    Returns a view with all currently known schedules.
    """
    all_schedules = models.Schedule.objects()
    return Response(all_schedules.to_json(), mimetype='application/json')


@schedule_app.route("/api/schedule/active", methods=["GET"])
@login_required
def active_schedule():
    # Returns the active schedule
    active_id = models.GlobalConfig.get().active_schedule
    try:
        s = models.Schedule.objects().get(sid=active_id)
        return Response(s.to_json())
    except DoesNotExist:
        return responses.invalid(request.url, "No active schedule")

@schedule_app.route("/api/schedule/<code>/activate", methods=["GET"])
@login_required
@decorators.requires_admin
def toggle_active_schedule(code):
    """
    Toggles the current active schedule.
    """
    if request.method == "GET":
        gc = models.GlobalConfig.objects().get()
        gc.active_schedule = code
        gc.save()
        # print(models.GlobalConfig.get().active_schedule)
        return responses.success(request.url, "SUCCESS. Active schedule is now: " + code)
    else:
        return responses.invalid(request.url, "METHOD not supported.")

@schedule_app.route("/api/schedule/<code>", methods=["GET","PUT","DELETE"])
@login_required
@decorators.requires_admin
def schedule(code):
    """
    Displays the schedule referred to by SID.
    """
    try:
        s = models.Schedule.objects().get(sid=str(code))
    except:
        return responses.invalid(url_for("schedule", code=code), "Schedule NOT FOUND.")
    if s:
        if request.method == "DELETE":
            # print ("Deleting a schedule with SID: " + str(s.sid) + "\nThe Active schedule is: " + str(models.GlobalConfig.get().active_schedule))
            if str(models.GlobalConfig.get().active_schedule) == str(s.sid):
                gc = models.GlobalConfig.objects().first()
                gc.active_schedule = "None"
                gc.save()
            s.delete()
            return responses.success(request.url, "Schedule DELETED")

        elif request.method == "GET":
            return render_template("schedule_display.html",
                user=current_user,
                users = models.User.objects(),
                locations = models.Location.objects(),
                active_schedule = models.GlobalConfig.get().active_schedule,
                schedule_name = s.sid)
        elif request.method == "PUT":
            payload = None
            try:
                payload = json.loads(request.data.decode("utf-8"))
            except Exception as e:
                return responses.invalid(request.url, e)
            if payload:
                print(payload)
                success = s.update(payload)
                if success:
                    return responses.schedule_updated(request.url, s.sid)
                else:
                    return responses.invalid(request.url, "Could not update schedule")
            else:
                return responses.invalid(request.url, "No data")

        else:
            return responses.invalid(url_for("schedule", code=code), "METHOD not supported.")

def index2time(i):
    """
    Helper function for converting matrix index to readable military (24-hour) time.
    """
    if ((i * 30) % 60) == 0:
        return (str(int((i*30)/60)) + ":" + str((i * 30) % 60) + "0")
    return (str(int((i*30)/60)) + ":" + str((i * 30) % 60))

def findOverlap(events):
    """
    Checks all combinations of events to find an overlapping event and combines
    the two into a single contiguous event.
    """
    i = 0
    while(i < (len(events)-1)):
        if events[i]['pid'] == events[i+1]['pid']:
            if (events[i]['_index']<= events[i+1]['_endex'] and events[i+1]['_index'] <= events[i]['_endex']):
                events[i] = {
                    '_id': ''.join(random.SystemRandom().choice(string.digits) for _ in range(8)),
                    'title': events[i]['title'],
                    'pid': events[i]['pid'],
                    'location': events[i]['location'],
                    'lcode': events[i]['lcode'],
                    '_index': min(events[i]['_index'], events[i+1]['_index']),
                    '_endex': max(events[i]['_endex'], events[i+1]['_endex']),
                    'start': index2time(min(events[i]['_index'], events[i+1]['_index'])),
                    'end': index2time(max(events[i]['_endex'], events[i+1]['_endex'])),
                    'dow': events[i]['dow'],
                    'textColor' : '#000000',
                    'backgroundColor' : events[i]['backgroundColor']
                }
                events.pop(i+1)
                i -= 1
        i += 1
    return events

def combineEvents(events):
    """
    Helper function for combining adjacent events on the calendar
    """
    combined_events = []
    for i in range(7):
        fullDay = deepcopy([e for e in events if e['dow'][0] == i])
        print(len(fullDay))
        if len(fullDay) > 0:
            fullDay.sort(key=lambda k: k['_index'])
            fullDay.sort(key=lambda k: k['pid'])
            combined_events.extend(findOverlap(fullDay))
    return combined_events

def HSVtoRGB(hue, sat, val):
    """
    Helper function for converting HSV color value to hex RGB.
    """
    h_i = int(hue*6.0)
    f = (hue * 6.0) - h_i
    p = val * (1 - sat)
    q = val * (1 - (f * sat))
    t = val * (1 - ((1 - f) * sat))
    if h_i == 0:
        r, g, b = val, t, p
    elif h_i == 1:
        r, g, b = q, val, p
    elif h_i == 2:
        r, g, b = p, val, t
    elif h_i == 3:
        r, g, b = p, q, val
    elif h_i == 4:
        r, g, b = t, p, val
    else:
        r, g, b = val, p, q
    rgb = [r, g, b]
    return "#%s" % "".join([hex(int(c*256))[2:] for c in rgb])

@schedule_app.route("/api/schedule/<code>/data", methods=["GET"])
@login_required
@decorators.requires_admin
def schedule_data(code):
    """
    Modifies the schedule referred to by SID
    """

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
                                            'title': str(u.first_name + " " + u.last_name[0] + "."),
                                            'pid': int(pid),
                                            'location': str(l.name),
                                            'lcode': l.code,
                                            '_index': i,
                                            '_endex': i+1,
                                            'start': index2time(i),
                                            'end': index2time(i+1),
                                            'dow': [{"sun":0,"mon":1,"tue":2,"wed":3,"thu":4,"fri":5,"sat":6}[day]],
                                            'textColor' : '#000000',
                                            'backgroundColor' : u.color
                                        }
                                    )
                                    id_counter += 1
            events = combineEvents(events)
            return Response(json.dumps(events), mimetype='application/json')

        else:
            return responses.invalid(url_for("schedule", code=code), "METHOD not supported.")
    else:
        return responses.invalid(url_for("schedule", code=code), "Schedule ID not found")

@schedule_app.route("/api/schedule/<code>/json", methods=["GET"])
@login_required
@decorators.requires_admin
def schedule_json(code):
    """
    Returns the schedule referred to by SID
    """

    s = models.Schedule.objects().get(sid=code)
    if s:
        events = []
        id_counter = 1
        if request.method == "GET":
            return Response(s.to_json(), mimetype='application/json')
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

        if np_arr is not None and user.can_schedule:
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

    new_schedule = models.Schedule()
    new_schedule.created_on = datetime.datetime.utcnow()
    new_schedule.data = loc_return_list
    new_schedule.sid = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(4))
    new_schedule.save()

    return jsonify(loc_return_list)
