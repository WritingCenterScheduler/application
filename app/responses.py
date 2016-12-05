# Writing Center Scheduler
# Fall 2016
# 
# Written by
# * Brandon Davis (davisba@cs.unc.edu)
#

import json
from flask import Response

def invalid(uri, reason):
    r = {}
    r["status"] = "fail"
    r["reason"] = str(reason)
    r["type"] = "invalid"
    r["uri"] = uri
    return Response(json.dumps(r),  mimetype='application/json')

def success(uri, stype):
    r = {
        "status": "success",
        "type": stype,
        "uri": uri,
    }
    return Response(json.dumps(r), mimetype='application/json')

def user_created(uri, pid):
    r = {}
    r["status"] = "success"
    r["type"] = "user created"
    r["uri"] = uri
    r["pid"] = pid
    return Response(json.dumps(r),  mimetype='application/json')

def loc_created(uri, creator, code):
    r = {}
    r["status"] = "success"
    r["type"] = "location created"
    r["uri"] = uri
    r["creator"] = creator
    return Response(json.dumps(r),  mimetype='application/json')

def loc_updated(uri, code):
    r = {}
    r["status"] = "success"
    r["type"] = "location updated"
    r["uri"] = uri
    r["code"] = code
    return Response(json.dumps(r),  mimetype='application/json')

def user_updated(uri, pid):
    r = {}
    r["status"] = "success"
    r["type"] = "user updated"
    r["uri"] = uri
    r["pid"] = pid
    return Response(json.dumps(r),  mimetype='application/json')

def schedule_updated(uri, code):
    r = {}
    r["status"] = "success"
    r["type"] = "schedule updated"
    r["uri"] = uri
    r["code"] = code
    return Response(json.dumps(r),  mimetype='application/json')

def illegal(reason):
    r = {}
    r["status"] = "fail"
    r["type"] = "illegal"
    r["reason"] = reason
    return Response(json.dumps(r), mimetype='application/json')

def not_implemented(uri):
    r = {}
    r["status"] = "fail"
    r["uri"] = uri
    r["type"] = "Not Implemented"
    r["reason"] = "Not Implemented"
    return Response(json.dumps(r), mimetype='application/json')

def bad_method(uri, method):
    r = {}
    r["status"] = "fail"
    r["uri"] = uri
    r["type"] = "Bad Method"
    r["reason"] = str(method) + " not supported"
    return Response(json.dumps(r), mimetype='application/json')
