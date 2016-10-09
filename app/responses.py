import json
from flask import Response

def invalid(uri, reason):
    r = {}
    r["status"] = "failed"
    r["reason"] = str(reason)
    r["type"] = "invalid"
    r["uri"] = uri
    return Response(json.dumps(r),  mimetype='application/json')

def user_created(uri, pid):
    r = {}
    r["status"] = "success"
    r["uri"] = uri
    r["pid"] = pid
    return Response(json.dumps(r),  mimetype='application/json')