from mongoengine import *
from . import config

# Setup the mongo connection
connect(config.DB_NAME,
    username=config.DB_USERNAME,
    password=config.DB_PASS,
    host=config.DB_HOST,
    port=config.DB_PORT)

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