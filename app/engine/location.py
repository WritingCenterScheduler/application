import numpy as np
import datetime
from . import config
from .user import User as User
from .employee import Employee as Employee

class Location:

    def __init__(self,
        name="Location",
        typecode="1",
        scalarWeight=2,
        requirements=None):

        self.name = name
        self.type = typecode
        self.scalarWeight = scalarWeight
        self.requirements = requirements
        self.pre_requirements = np.copy(self.requirements)
        self.total_cost = 0
        self.cost = None # A numpy array
        self.schedule = None  # A 3D array
        self.need = None # A numpy arrays

    def initialize_dimensions(self, width, height, depth):
        self.schedule = np.zeros((width, height, depth))
        self.cost = np.zeros((width, height))

    def greatest_need(self):
        """
        returns the value of the timeslot with the greatest need (LOWEST NUMBER)
        Return tuple: (need value, coordinates, self)
        """
        if (self.need is None):
            raise TypeError("self.need is None, did you calculate_need()?")
        else:
            coords = []
            needs = []
            ceiling = np.amax(self.need)
            while np.amin(self.need) <= ceiling :
                coord = np.unravel_index(np.argmin(self.need), self.need.shape)
                coords.append(coord)
                self.need[coord[0]][coord[1]] = ceiling + 1
            return coords, self

    def schedule_employee(self, e, t):
        if self.requirements[t[0]][t[1]] > 0:
            if self.schedule[t[0]][t[1]][0] == 0:
                self.schedule[t[0]][t[1]][0] = e.pid
                e.schedule_at(t)
                self.requirements[t[0]][t[1]] -= 1
                return True
            elif self.schedule[t[0]][t[1]][1] == 0:
                self.schedule[t[0]][t[1]][1] = e.pid
                e.schedule_at(t)
                self.requirements[t[0]][t[1]] -= 1
                return True
        return False

    def reset(self):
        self.requirements = self.pre_requirements
        self.schedule = np.zeros(self.schedule.shape)
        self.cost = np.zeros((len(self.schedule), len(self.schedule[0])))
        self.total_cost = 0
        self.need = None
