from .user import User as User
import numpy as np

class Employee(User):

    def __init__(self, availability, **kwargs):
        self.availability = availability # A numpy array
        self.pre_availability = np.copy(self.availability)
        super(Employee, self).__init__(**kwargs)
        self.schedule = np.zeros(self.availability.shape)
        self.schedule_locations = [[None for i in range(self.availability.shape[1])] for i in range(self.availability.shape[0])]
        self.total_availability = self.calculate_total_availability()
        self.scheduled_hours = 0.0

    def calculate_total_availability(self):
        """
        Updates the total availability of an employee.
        The total availability is defined as the value indicating an employee's
        overall availability to work. An employee who can work at many different
        times throughout the week will have a higher total availability than an
        employee who has limited availability throughout the week.
        :return: Integer representing total availability
        """
        # A 1-D array of employee preferences of each scalar type
        availability_frequencies = np.zeros(3)
        for slot in self.availability.flat:
            availability_frequencies[slot] += 1
        return (availability_frequencies[2] * 2) + availability_frequencies[1]

    def is_available_at(self, timeslot, location):
        """
        Returns true or false depending on whether employee is available to be scheduled at a specific timeslot
        :return: Boolean
        """
        l = len(self.availability)
        x, y = timeslot
        return ((self.schedule_locations[(x+1)%l][y] == location) or (self.schedule_locations[(x+1)%l][y] == None)) and ((self.schedule_locations[(x-1)%l][y] == location) or (self.schedule_locations[(x-1)%l][y] == None)) and (self.availability[x][y] > 0)

    def reset(self):
        """
        Resets the availability of an employee to what they originally specified before any scheduling has occurred
        """
        self.availability = self.pre_availability
        self.schedule = np.zeros(self.availability.shape)
        self.total_availability = self.calculate_total_availability()
        self.schedule_locations = [[None for i in range(self.availability.shape[1])] for i in range(self.availability.shape[0])]

    def schedule_at(self, timeslot, location):
        """
        Tells the employee to consider itself scheduled at the timeslot.
        Should update any internal state necessary, especially it's availability
        :param timeslot: Consider itself scheduled at timeslot
        :return: none
        """
        if self.is_available_at(timeslot, location):
            # unpack timeslot
            x, y = timeslot
            self.schedule[x][y] = 1
            self.total_availability -= self.availability[x][y]
            self.availability[x][y] = 0
            self.scheduled_hours += 0.5
