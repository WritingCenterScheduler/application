# Writing Center Scheduler
# Fall 2016
# 
# Written by
# * Brandon Davis (davisba@cs.unc.edu)
#

from functools import wraps
from flask_login import current_user
from . import responses

def requires_admin(f):
    @wraps(f)
    def requires_admin_wrapper(*args, **kwargs):

        if current_user.is_admin:
            return f(*args, **kwargs)
        else:
            return responses.illegal("Requires Admin")

    return requires_admin_wrapper