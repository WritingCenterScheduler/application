from mongoengine import *
import numpy as np
from . import config

# Setup the mongo connection
connect(config.DB_NAME,
    username=config.DB_USERNAME,
    password=config.DB_PASS,
    host=config.DB_HOST,
    port=config.DB_PORT)

def global_to_np_arr(json_avail):
    """
    Turns the object into a NP arr for scheduling
    """
    # height = timeslots_per_day
    # width = 7 days per week
    avail = np.zeros(shape=(config.TIMESLOTS_PER_DAY, 7))

    for i in range(config.TIMESLOTS_PER_DAY):   
        newrow = [
            json_avail["sun"][i],
            json_avail["mon"][i],
            json_avail["tue"][i],
            json_avail["wed"][i],
            json_avail["thu"][i],
            json_avail["fri"][i],
            json_avail["sat"][i],
        ]
        avail[i] = newrow
    return avail

class Location(Document):
    name = StringField(required=True)
    code = IntField(unique=True)
    open_at = StringField(required=True)
    close_at = StringField(required=True)
    requirements = DictField()
    resolution_minutes = IntField()

    def init(self, 
            name="Unknown Location",
            open_at=config.DEFAULT_OPEN,
            close_at=config.DEFAULT_CLOSE,
            code=-1 # -1 should never happen
        ):

        self.name = name
        self.code = code
        self.open_at = open_at
        self.close_at = close_at
        self.resolution_minutes = config.TIMESLOT_SIZE_MIN
        self.requirements = config.DEFAULT_LOCATION_REQUIREMENTS

    def to_np_arr(self):
        return global_to_np_arr(self.requirements)

class Schedule(Document):
    """
    Represents a final or partially final schedule.
    over all locations.
    """
    # TODO
    name = StringField(required=True)

class User(Document):
    last_name = StringField(required=True)
    first_name = StringField(required=True)
    pid = IntField(unique=True)
    email = EmailField()
    typecode = StringField()
    availability = DictField()
    resolution_minutes = IntField()

    def init(self,
            first_name="Tar",
            last_name="Heel",
            pid=-1, # -1 should never happen
            email="unknown@unc.edu",
            onyen="unknown",
            typecode="000"
        ):

        self.last_name = last_name
        self.first_name = first_name
        self.pid = pid
        self.email = email
        self.onyen = onyen
        self.typecode = typecode # An N digit number.
            # (0/1)XXXX... determines not admin/admin
            # X(0/1)XXX... determines new/returning
            # XX(0/1)XX... determines something else...?
        self.resolution_minutes = config.TIMESLOT_SIZE_MIN
        self.availability = config.DEFAULT_AVAILABILITY

    def update(self, payload):
        """
        Updates the user based on the provided payload
        """
        if self.is_payload_safe(payload):
            for key in payload.keys():
                setattr(self, key, payload[key])
            self.save()
            return True
        return False

    def is_payload_safe(self, payload):
        """
        Makes sure the payload is safe
        """
        keys = payload.keys()
        return all(hasattr(self, key) for key in keys)

    def to_np_arr(self):
        return global_to_np_arr(self.availability)

    @property
    def is_admin(self):
        return self.typecode[0] == "1"

    @property
    def scalar_type(self):
        return self.typecode[1]

    @property
    def is_returner(self):
        return self.typecode[1] == "1"

    def get_id(self):
        return self.pid

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False