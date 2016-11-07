import numpy as np
import datetime, random
from . import config
from .user import User as User
from .employee import Employee as Employee
from .location import Location as Location

class ScheduleManager:

    # Most important number, how often a schedule fails to be generated when one is available
    # If a spot/chunk of slots has only one person available, schedule that person at that slot and FREEZE
    # If the need is lower than the availability, go ahead and FREEZE
    # Without replacement may speed things up (May take that back)
    # Make sure that people aren't scheduled across locations, or double scheduled

    def __init__(self,
        shifts_per_day=48,
        shift_length_minutes=30,
        shift_start_time="08:00"):
        """
        :param shifts_per_day: the number of shifts in a given day.
        :param shift_length_minutes: the length of a shift in minutes.
        :param shift_start_time: A 24hour time when all shifts start.
            HH:MM (00:00 through 23:59)
        """
        self.locations = []
        self.candidates = []
        self.cost = 0
        self.shifts_per_day = shifts_per_day
        self.shift_length_minutes = shift_length_minutes
        self.shift_start_time = shift_start_time

    def add_candidate(self, candidate):
        self.candidates.append(candidate)

    def sort_candidates_by_total_availability(self):
        """
        Sorts the candidates in place by total availability in reverse order.
        :return: None
        """
        self.candidates.sort(key=lambda x: x.total_availability, reverse=True)

    def sort_candidates_by_return_status(self):
        """
        Sorts the possible candidates in place by returning status.
        :return: None
        """
        self.candidates.sort(key=lambda x: x.is_returner())

    def search_PID(self, PID):
        """
        returns employee with specifided PID else none
        """
        for p in self.candidates:
            if p.pid == PID :
                return p
        return None

    def add_location(self, loc):
        """
        Adds a location to the list of locations
        """

        # TODO: VERIFY that the location's timeslots and need align with...
        #   shifts per day, shift_length_minutes, shift_start_time
        width = len(loc.requirements)
        height = len(loc.requirements[0])
        loc.initialize_dimensions(width, height, 2)
        self.locations.append(loc)

    def calculate_need(self):
        """
        Function based on timeslots and availability of possible candidtates
        need (at each timeslot) = Sigma(candidate availability * scalar) - timeslot_need
        timeslot need = Sigma(timeslot.requirements * timeslot.scalar_weight)
        """

        for l in self.locations:
            all_candidate_availability = l.requirements * 0

            for c in self.candidates:

                c_available = c.availability
                c_available[c_available>0] = 1
                c_available[c_available<0] = 0

                all_candidate_availability += c_available * config.scalars[c.scalar_type]

            timeslot_need = l.requirements * 0

            timeslot_need += l.requirements * l.scalarWeight

            l.need = all_candidate_availability - timeslot_need

    def greatest_need(self):
        """
        returns the values of the timeslots with the greatest needs (LOWEST NUMBER) across all locations
        Return tuple: (coordinates, self)
        """
        all_location_needs = []
        for l in self.locations:
            if (l.need is None):
                raise TypeError("self.need is None, did you calculate_need()?")
            else:
                ceiling = np.amax(l.need)
                while np.amin(l.need) <= ceiling:
                    coord = np.unravel_index(np.argmin(l.need), l.need.shape)
                    need = np.amin(l.need)
                    l.need[coord[0]][coord[1]] = ceiling + 1
                    all_location_needs.append((need, coord, l))
        all_location_needs.sort(key=lambda x: x[0], reverse=False)
        return all_location_needs

    def run_schedule(self):
        """
        The main part of the algorithm.
        """
        self.calculate_need()
        needs = self.greatest_need()
        if needs:
            for n in needs:
                available_candidates = []
                for c in self.candidates:
                    if c.is_available_at(n[1]) and int(c.typecode[1]) >= int(n[2].type) and n[2].requirements[n[1][0]][n[1][1]] > 0:
                        available_candidates.append(c)
                if available_candidates: # if list is not empty
                    if(n[2].requirements[n[1][0]][n[1][1]] > 0):
                        c = random.choice(available_candidates)
                        n[2].schedule_employee(c, n[1])
                self.calculate_need()
                needs = self.greatest_need()
        for l in self.locations:
            for i in range(len(l.requirements)):
                for j in range(len(l.requirements[0])):
                    available_candidates = []
                    for c in self.candidates:
                        if l.requirements[i][j] > 0 and c.is_available_at((i,j)) and int(c.typecode[1]) >= int(l.type):
                            available_candidates.append(c)
                        if available_candidates: # if list is not empty
                            while(l.requirements[i][j] > 0):
                                c = random.choice(available_candidates)
                                l.schedule_employee(c, (i,j))
                                available_candidates.remove(c)
        self.calculate_need()
        self.compute_schedule_optimality()

    def location_cost(self, l):
        """
        Computes the cost incurred from having a less than optimal schedule
        """
        if l.schedule is None:
            raise TypeError('<location.schedule> array is uninitialized.')
        for i in range(len(l.schedule)):
            for j in range(len(l.schedule[i])):
                for k in range(len(l.schedule[i][j])):
                    if l.schedule[i][j][k] != 0:
                        e = self.search_PID(int(l.schedule[i][j][k]))
                        if (j > 0 and k > 0) and (l.schedule[i][j-1][k] == l.schedule[i][j][k] or l.schedule[i][j-1][k-1] == l.schedule[i][j][k] or l.schedule[i][j-1][k] == l.schedule[i][j][k-1] or l.schedule[i][j-1][k-1] == l.schedule[i][j][k-1]):
                            # print (l.schedule[1][1][0])
                            # print (l.schedule[2][1][0])
                            pass
                        elif (j > 0 and k > 0) and (l.schedule[i][j-1][k] != 0 or l.schedule[i][j-1][k-1] != 0):
                            print ("cost incurred ")
                            l.cost[i][j] = l.cost[i][j] + (e.pre_availability[i][j] % 2) * 20
                        if (l.schedule[i][j-1][k] == 0) and l.requirements[i][j] > 0:
                            l.cost[i][j] = l.cost[i][j] + l.requirements[i][j] * 40
        l.total_cost = np.sum(l.cost)

    def compute_schedule_optimality(self):
        """
        Using self.locations, decide how optimal the schedule is.
        """
        if not self.locations:
            raise ValueError('<scheduleManager.locations> array is empty')
        for l in self.locations:
            self.location_cost(l)
            self.cost += l.total_cost
