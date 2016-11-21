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

def global_np_to_json_dict(np_arr):
    """
    Given a 7 wide by N long np array, return a json dict.
    """
    rtrn = {
        "sun":[],
        "mon":[],
        "tue":[],
        "wed":[],
        "thu":[],
        "fri":[],
        "sat":[]
    }
    for row in np_arr:
        rtrn["sun"].append([None if f is 0 else f for f in row[0].tolist()])
        rtrn["mon"].append([None if f is 0 else f for f in row[1].tolist()])
        rtrn["tue"].append([None if f is 0 else f for f in row[2].tolist()])
        rtrn["wed"].append([None if f is 0 else f for f in row[3].tolist()])
        rtrn["thu"].append([None if f is 0 else f for f in row[4].tolist()])
        rtrn["fri"].append([None if f is 0 else f for f in row[5].tolist()])
        rtrn["sat"].append([None if f is 0 else f for f in row[6].tolist()])
    return rtrn


class GlobalConfig(Document):
    active_schedule = StringField(required=True)

    @staticmethod
    def get():  
        gc = GlobalConfig.objects().first()
        
        if gc == None:
            gc = GlobalConfig()
            gc.active_schedule = Schedule.objects().first().sid
            gc.save()
        
        return gc


class Location(Document):
    name = StringField(required=True)
    code = IntField(unique=True)
    open_at = StringField(required=True)
    close_at = StringField(required=True)
    requirements = DictField()
    resolution_minutes = IntField()
    enabled = BooleanField()
    type_code = IntField()

    def init(self, 
            name="Unknown Location",
            open_at=config.DEFAULT_OPEN,
            close_at=config.DEFAULT_CLOSE,
            code=-1, # -1 should never happen
            type_code=0 # 0 means anybody
        ):

        self.name = name
        self.code = code
        self.open_at = open_at
        self.close_at = close_at
        self.resolution_minutes = config.TIMESLOT_SIZE_MIN
        self.requirements = config.DEFAULT_AVAILABILITY
        self.type_code = type_code

    def to_np_arr(self):
        return global_to_np_arr(self.requirements)

    def update(self, payload):
        """
        Updates the user based on the provided payload
        """
        # if len(self.open_at.split(':')) > 1:
        #     self.open_at = self.open_at.split(':')[0]
        #     self.close_at = self.close_at.split(':')[0]
        
        payload.pop("_id", None)
        keys = payload.keys()
        payload['requirements'] = self.sanitize_location_payload(payload['requirements'])
        if all(hasattr(self, key) for key in keys):
            for key in payload.keys():
                setattr(self, key, payload[key])
            self.save()
            return True
        return False

    def sanitize_location_payload(self, payload):
        keys = payload.keys()
        length = 24 * (60 // self.resolution_minutes) # hours * slots per hour
        for slot in range(length):
            for key in keys:
                if slot < int(self.open_at):
                    payload[key][slot] = 0
                if slot > int(self.close_at):
                    payload[key][slot] = 0
        return payload


class Schedule(Document):
    """
    Represents a final or partially final schedule.
    over all locations.
    """
    # TODO
    sid = StringField(required=True, unique=True)
    data = ListField()
    created_on = DateTimeField()

class User(Document):
    last_name = StringField(required=True)
    first_name = StringField(required=True)
    pid = IntField(unique=True)
    email = EmailField()
    typecode = StringField()
    availability = DictField()
    resolution_minutes = IntField()

    updatable_fields = ["last_name", "first_name", "email", "availability"]

    def init(self,
            first_name="Tar",
            last_name="Heel",
            pid=-1, # -1 should never happen
            email="unknown@unc.edu",
            typecode="011"
        ):

        self.last_name = last_name
        self.first_name = first_name
        self.pid = pid
        self.email = email
        self.typecode = typecode # An N digit number.
            # (0/1)XXXX... determines not admin/admin
            # X(0/1)XXX... determines new/returning
            # XX(0/1)XX... determines active/inactive
        self.resolution_minutes = config.TIMESLOT_SIZE_MIN
        self.availability = config.DEFAULT_AVAILABILITY

    def update(self, payload):
        """
        Updates the user based on the provided payload
        """
        # print(payload)
        payload.pop("_id", None)
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
        payload.pop("_id", None)
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
    def can_schedule(self):
        return self.typecode[2] == "1"

    @property
    def is_anonymous(self):
        return False