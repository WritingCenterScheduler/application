import json
from flask import Response

def invalid(uri, reason):
    r = {}
    r["status"] = "fail"
    r["reason"] = str(reason)
    r["type"] = "invalid"
    r["uri"] = uri
    return Response(json.dumps(r),  mimetype='application/json')

def user_created(uri, pid):
    r = {}
    r["status"] = "success"
    r["type"] = "user created"
    r["uri"] = uri
    r["pid"] = pid
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
