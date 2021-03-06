# Writing Center Scheduler
# Fall 2016
# 
# Written by
# * Brandon Davis (davisba@cs.unc.edu)

import os
import uuid

# For the local environment
ADMIN_PID = 720430213 # A user to test admin function on local dev
NOADMIN_PID = 3 # A user to test non-admin function on local dev
LOCAL = False if os.getenv("OPENSHIFT_MONGODB_DB_HOST", False) else True
SSO_LOGOUT_URL = "https://sso.unc.edu/idp/logout.jsp"

SECRET_KEY = "local" if LOCAL else '1c9dedc4-3f3d-4709-8330-8ab064af9be8' # Regenerate the Secret key at startup in prod.
TIMESLOT_SIZE_MIN = 30
TIMESLOTS_PER_DAY = 48
DEFAULT_DESIRED_HOURS = 8
DEFAULT_OPEN = "8:30"
DEFAULT_CLOSE = "19:00"

# Database config
DB_NAME = "wss"
DB_HOST = os.getenv("OPENSHIFT_MONGODB_DB_HOST", "localhost")
DB_PORT = int(os.getenv("OPENSHIFT_MONGODB_DB_PORT", 27017))
DB_USERNAME = os.getenv("OPENSHIFT_MONGODB_DB_USERNAME", "local")
DB_PASS = os.getenv("OPENSHIFT_MONGODB_DB_PASSWORD", "default")

# Default to NOT available
DEFAULT_AVAILABILITY = {
    "sun": [0 for i in range(TIMESLOTS_PER_DAY)],
    "mon": [0 for i in range(TIMESLOTS_PER_DAY)],
    "tue": [0 for i in range(TIMESLOTS_PER_DAY)],
    "wed": [0 for i in range(TIMESLOTS_PER_DAY)],
    "thu": [0 for i in range(TIMESLOTS_PER_DAY)],
    "fri": [0 for i in range(TIMESLOTS_PER_DAY)],
    "sat": [0 for i in range(TIMESLOTS_PER_DAY)],
}

# For the scheduler
MAX_WORKERS_PER_SLOT = 2
MAX_WORKER_RUN = 4 # hours
