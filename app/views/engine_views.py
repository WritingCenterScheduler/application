import json
import numpy as np
# import flask
from flask import jsonify, Response, request, render_template
from flask_login import current_user, login_required
# import from init
from app import schedule_app, load_user
# import Mongo Exceptions
from mongoengine import MultipleObjectsReturned, DoesNotExist, NotUniqueError
# import local libraries
from .. import models, responses, decorators, config

from app.engine.scheduleManager import ScheduleManager
from app.engine.user import User
from app.engine.employee import Employee
from app.engine.location import Location

@schedule_app.route("/engine/run", methods=["GET"])
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

        candidate = Employee(user.to_np_arr(), 
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
        sm.add_location(l)

    for candidate in schedulable_users:
        sm.add_candidate(candidate)

    # width = 7 # Days per week
    # height = config.TIMESLOTS_PER_DAY

    # for l in sm.locations:
    #     l.initialize_dimensions(width, height, 2)
    #     l.calculate_need()


    # # return np.array_str(sm.locations[0].need)

    # for l in sm.locations:
    #     l.schedule_greatest_need()
    #     l.schedule_greatest_need()


    # for c in sm.candidates:
    #     print(c.pre_availability)
    #     print(c.schedule)

    sm.run_schedule()
    
    for l in sm.locations:
        print(l.requirements)
        # print(l.schedule)

    return np.array_str(sm.locations[0].schedule.astype(int))