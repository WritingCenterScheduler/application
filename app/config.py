import os
import uuid

SECRET_KEY = uuid.uuid4()
TIMESLOT_SIZE_MIN = 30
TIMESLOTS_PER_DAY = 48
DEFAULT_OPEN = "8:30"
DEFAULT_CLOSE = "19:00"

# Database config
DB_NAME = "wss"
DB_HOST = os.getenv("OPENSHIFT_MONGODB_DB_HOST", "localhost")
DB_PORT = os.getenv("OPENSHIFT_MONGODB_DB_PORT", 27017)
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

DEFAULT_TIMESLOT_NEED = {
    "a": 0,
    "s1": 0,
    "s2": 1,
}

DEFAULT_LOCATION_REQUIREMENTS = {
    "sun": [DEFAULT_TIMESLOT_NEED for i in range(TIMESLOTS_PER_DAY)],
    "mon": [DEFAULT_TIMESLOT_NEED for i in range(TIMESLOTS_PER_DAY)],
    "tue": [DEFAULT_TIMESLOT_NEED for i in range(TIMESLOTS_PER_DAY)],
    "wed": [DEFAULT_TIMESLOT_NEED for i in range(TIMESLOTS_PER_DAY)],
    "thu": [DEFAULT_TIMESLOT_NEED for i in range(TIMESLOTS_PER_DAY)],
    "fri": [DEFAULT_TIMESLOT_NEED for i in range(TIMESLOTS_PER_DAY)],
    "sat": [DEFAULT_TIMESLOT_NEED for i in range(TIMESLOTS_PER_DAY)],
}