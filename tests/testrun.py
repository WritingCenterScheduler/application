import unittest, copy, random
import numpy as np
from app.engine.scheduleManager import ScheduleManager as ScheduleManager
from app.engine.user import User as User
from app.engine.employee import Employee as Employee
from app.engine.location import Location as Location

class TestRun(unittest.TestCase):

    def setUp(self):
        import sampledata
        self.sm = ScheduleManager()

        # Create Test Employees
        self.tc1 = "010"
        e1av = copy.deepcopy(sampledata.e1av)
        e2av = copy.deepcopy(sampledata.e2av)
        e3av = copy.deepcopy(sampledata.e3av)
        e4av = copy.deepcopy(sampledata.e4av)
        self.candidate1 = Employee(e1av, typecode=self.tc1, pid=1)
        self.candidate2 = Employee(e2av, typecode=self.tc1, pid=2)
        self.candidate3 = Employee(e3av, typecode=self.tc1, pid=3)
        self.candidate4 = Employee(e4av, typecode=self.tc1, pid=4)

        # Create Test Locations
        self.location1 = Location(typecode=sampledata.loc1["type"], scalarWeight=sampledata.loc1["scalar_weight"], requirements=sampledata.loc1["requirements"])

        self.location2 = Location(typecode=sampledata.loc2["type"], scalarWeight=sampledata.loc2["scalar_weight"], requirements=sampledata.loc2["requirements"])

        # Add employee to location and location to schedule manager
        self.sm.add_candidate(self.candidate1)
        self.sm.add_candidate(self.candidate2)
        self.sm.add_candidate(self.candidate3)
        self.sm.add_candidate(self.candidate4)
        self.sm.add_location(self.location1)
        self.sm.add_location(self.location2)

    def tearDown(self):
        del self.sm
        del self.candidate1
        del self.candidate2
        del self.candidate3
        del self.candidate4
        del self.location1
        del self.tc1

    def test_make(self):
        self.assertTrue(isinstance(self.sm, ScheduleManager))

    def test_calculate_need(self):
        """
        Tests the population of a Location object's need array, which contains
        the weighted "need" value of each timeslot. The weighted "need" value of
        a timeslot denotes the priority that it will be given while scheduling.
        """

        # Call the calculate_need() function for a location in schedule_manager
        # This should populate the need array for the Location object
        self.sm.calculate_need()
        for l in self.sm.locations:
            self.assertIsNotNone(l.need)

    def test_initialize_location_schedule(self):
        """
        Tests the initialization of the dimensions of the Location object's
        schedule array.
        """

        # Call the initialize_dimensions() function for the location
        # This should initialize the dimensions of the schedule to match the
        # dimensions of the timeslot requirements
        width = len(self.sm.locations[0].requirements)
        height = len(self.sm.locations[0].requirements[0])
        self.sm.locations[0].initialize_dimensions(width, height, 2)

        self.assertEqual(len(self.sm.locations[0].schedule), width)
        self.assertEqual(len(self.sm.locations[0].schedule[0]), height)
        self.assertEqual(len(self.sm.locations[0].schedule[0][0]), 2)

    def test_schedule_employee(self):
        """
        Tests an Employee object's schedule_at(timeslot) function where timeslot
        is a tuple containing a timeslot's coordinates to be scheduled. Should
        remove the scheduled timeslot from the employee's availability array and
        add that timeslot to their schedule array
        """
        timeslot1 = (0,0) # A time when the employee is unavailable
        timeslot2 = (1,1) # A time when the employee is available

        pre_schedule = np.copy(self.candidate1.schedule)
        pre_availability = np.copy(self.candidate1.pre_availability)

        # Attempt to schedule where employee is unavailable
        self.candidate1.schedule_at(timeslot1)
        self.assertNotEqual(self.candidate1.schedule[0][0], 1)

        # Attempt to schedule where employee is available
        self.candidate1.schedule_at(timeslot2)
        self.assertEqual(self.candidate1.schedule[1][1], 1)

        self.assertEqual(self.candidate1.schedule[0][0], pre_schedule[0][0])
        # Different as result of successful scheduling, employee schedule modified
        self.assertNotEqual(self.candidate1.schedule[1][1], pre_schedule[1][1])

        self.assertEqual(self.candidate1.availability[0][0], pre_availability[0][0])
        # Different as result of successful scheduling, employee availability modified
        self.assertNotEqual(self.candidate1.availability[1][1], pre_availability[1][1])

    def test_location_greatest_need(self):
        """
        Tests Location object's greatest_need() function for correct return type
        """
        # Call the calculate_need() function for a location in schedule_manager
        # This should populate the need array for the Location object
        self.sm.calculate_need()

        # Call the greatest_need() function, which returns integer, tuple, self
        timeslots, loc = self.location1.greatest_need()

        # Test whether locations evaluate to same object
        self.assertIs(self.location1, loc)

        # Test that timeslot is a list of tuples tuple, and not a list of flattned coordinates
        self.assertTrue(isinstance(timeslots, list))
        self.assertTrue(isinstance(timeslots[0], tuple))

    def test_all_greatest_need(self):
        """
        Tests schedule manager's greatest_need function for correct return type
        """
        self.sm.calculate_need()
        needs = self.sm.greatest_need()
        self.assertIsNotNone(needs)
        for i in range(10):
            x = random.randint(0, len(needs)-2)
            self.assertTrue(needs[x][0] <= needs[x+1][0])

    def test_run_schedule(self):
        self.sm.run_schedule()
        print ("The COST of this schedule is: " + str(self.sm.cost))
        for l in self.sm.locations:
            a = np.zeros((len(l.schedule), len(l.schedule[0])))
            b = np.zeros(a.shape)
            for i in range(len(l.schedule)):
                for j in range(len(l.schedule[0])):
                    a[i][j] = l.schedule[i][j][0]
                    b[i][j] = l.schedule[i][j][1]
            print("\nThe scheduled employees are:")
            print (a)
            print (b)
            print("The location's remaining requirements are:")
            print (l.requirements)
            filler_candidates = []
            for i in range(len(l.requirements)):
                for j in range(len(l.requirements[0])):
                    for c in self.sm.candidates:
                        if c.is_available_at((i,j)) and l.requirements[i][j] > 0:
                            filler_candidates.append("Candidate PID = " + str(c.pid) + " can fill timeslot (" + str(i) + "," + str(j) + ")")
            if filler_candidates:
                print("The remaining spots can be filled by the following candidates:")
                for c in filler_candidates: print(c)
            else:
                print("There are no available candidates that can fill the remaining timeslots.")
            print (l.total_cost)
            print (l.cost)
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
